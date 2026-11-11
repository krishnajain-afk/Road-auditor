"""Ultralytics YOLO adapters.

Three weight roles are supported, each optional:
  * general: COCO-trained (yolov8n/s, yolo11n/s) -> road users, traffic lights, stop signs, animals, benches...
  * damage : RDD2022-style weights (classes D00 longitudinal crack, D10 transverse crack, D20 alligator, D40 pothole,
             plus optional D43 crosswalk blur, D44 white line blur, D50 manhole) -> pavement condition
  * sign   : traffic-sign detector (Indian/GTSDB/Mapillary classes) -> IRC:67 sign inventory
Class names are mapped to AssetType through COCO_MAP / RDD_MAP / SIGN_MAP; unknown names fall back to UNKNOWN.
"""
from __future__ import annotations

import os
from typing import Dict, List, Optional

import numpy as np

from ..schemas import AssetType, BBox, CameraModel, Detection, FrameRef, Source
from .base import Detector

COCO_MAP: Dict[str, AssetType] = {
    "person": AssetType.PEDESTRIAN, "bicycle": AssetType.CYCLIST, "car": AssetType.CAR,
    "motorcycle": AssetType.MOTORCYCLE, "bus": AssetType.BUS, "truck": AssetType.TRUCK,
    "traffic light": AssetType.TRAFFIC_SIGNAL, "stop sign": AssetType.SIGN_STOP, "fire hydrant": AssetType.BOLLARD,
    "bench": AssetType.BUS_STOP, "cow": AssetType.ANIMAL, "dog": AssetType.ANIMAL, "horse": AssetType.ANIMAL,
    "sheep": AssetType.ANIMAL, "elephant": AssetType.ANIMAL, "cat": AssetType.ANIMAL,
    "parking meter": AssetType.PARKED_VEHICLE, "umbrella": AssetType.HAWKER_ENCROACHMENT,
    "potted plant": AssetType.MEDIAN,
}
RDD_MAP: Dict[str, AssetType] = {
    "D00": AssetType.CRACK_LONGITUDINAL, "D10": AssetType.CRACK_TRANSVERSE, "D20": AssetType.CRACK_ALLIGATOR,
    "D40": AssetType.POTHOLE, "D43": AssetType.ZEBRA_CROSSING, "D44": AssetType.LANE_LINE, "D50": AssetType.MANHOLE,
    "pothole": AssetType.POTHOLE, "Pothole": AssetType.POTHOLE, "potholes": AssetType.POTHOLE,
    "longitudinal crack": AssetType.CRACK_LONGITUDINAL, "transverse crack": AssetType.CRACK_TRANSVERSE,
    "alligator crack": AssetType.CRACK_ALLIGATOR, "crack": AssetType.CRACK_LONGITUDINAL, "patch": AssetType.PATCH,
    "manhole": AssetType.MANHOLE, "open manhole": AssetType.OPEN_MANHOLE, "speed bump": AssetType.SPEED_HUMP,
    "speedbump": AssetType.SPEED_HUMP, "speed breaker": AssetType.SPEED_HUMP, "waterlogging": AssetType.WATERLOGGING,
}
SIGN_MAP: Dict[str, AssetType] = {
    # Indian Expressway Traffic Sign Dataset (cfi_signs.pt) class names
    "Ahead only": AssetType.SIGN_MANDATORY, "Bump": AssetType.SIGN_SPEED_BREAKER, "Car Speed 100": AssetType.SIGN_SPEED_LIMIT,
    "Danger": AssetType.SIGN_CAUTIONARY, "Go Slow": AssetType.SIGN_CAUTIONARY, "Lane sign": AssetType.SIGN_INFORMATORY,
    "Left Curve": AssetType.SIGN_CAUTIONARY, "No Passing": AssetType.SIGN_MANDATORY, "No Stopping": AssetType.SIGN_MANDATORY,
    "No U Turn": AssetType.SIGN_MANDATORY, "No Waiting": AssetType.SIGN_MANDATORY, "Phone": AssetType.SIGN_INFORMATORY,
    "Right Curve": AssetType.SIGN_CAUTIONARY, "Speed 100": AssetType.SIGN_SPEED_LIMIT, "Speed 30": AssetType.SIGN_SPEED_LIMIT,
    "Speed 50": AssetType.SIGN_SPEED_LIMIT, "Speed 80": AssetType.SIGN_SPEED_LIMIT, "Steep decent": AssetType.SIGN_CAUTIONARY,
    "Truck Speed 80": AssetType.SIGN_SPEED_LIMIT, "Tunnel": AssetType.SIGN_INFORMATORY, "Work in Progress": AssetType.SIGN_CAUTIONARY,
    "stop": AssetType.SIGN_STOP, "give way": AssetType.SIGN_GIVE_WAY, "yield": AssetType.SIGN_GIVE_WAY,
    "speed limit": AssetType.SIGN_SPEED_LIMIT, "pedestrian crossing": AssetType.SIGN_PEDESTRIAN_CROSSING,
    "school": AssetType.SIGN_SCHOOL, "speed breaker": AssetType.SIGN_SPEED_BREAKER, "hump": AssetType.SIGN_SPEED_BREAKER,
    "mandatory": AssetType.SIGN_MANDATORY, "cautionary": AssetType.SIGN_CAUTIONARY, "warning": AssetType.SIGN_CAUTIONARY,
    "informatory": AssetType.SIGN_INFORMATORY, "information": AssetType.SIGN_INFORMATORY,
    "traffic light": AssetType.TRAFFIC_SIGNAL, "traffic signal": AssetType.TRAFFIC_SIGNAL,
}


def _map_label(label: str, table: Dict[str, AssetType], default: AssetType) -> AssetType:
    if label in table:
        return table[label]
    low = label.lower()
    for k, v in table.items():
        if k.lower() in low:
            return v
    return default


class YoloDetector(Detector):
    def __init__(self, weights: str, role: str = "general", conf: float = 0.25, iou: float = 0.5,
                 imgsz: int = 640, device: str = "cpu"):
        from ultralytics import YOLO  # lazy import (heavy)
        if not os.path.exists(weights):
            raise FileNotFoundError(weights)
        self.model = YOLO(weights)
        self.role = role
        self.name = f"yolo_{role}"
        self.conf, self.iou, self.imgsz, self.device = conf, iou, imgsz, device
        self.names = self.model.names
        self.table = {"general": COCO_MAP, "damage": RDD_MAP, "sign": SIGN_MAP}.get(role, COCO_MAP)
        self.default = {"general": AssetType.UNKNOWN, "damage": AssetType.POTHOLE, "sign": AssetType.SIGN_UNKNOWN}.get(role, AssetType.UNKNOWN)
        self.is_seg = getattr(self.model, "task", "") == "segment"

    def warmup(self) -> None:
        self.model.predict(np.zeros((320, 320, 3), np.uint8), verbose=False, imgsz=320, device=self.device)

    def detect(self, img: np.ndarray, frame: FrameRef, cam: Optional[CameraModel] = None) -> List[Detection]:
        res = self.model.predict(img, conf=self.conf, iou=self.iou, imgsz=self.imgsz, device=self.device, verbose=False)
        out: List[Detection] = []
        if not res:
            return out
        r = res[0]
        if r.boxes is None:
            return out
        polys = None
        if self.is_seg and r.masks is not None:
            polys = r.masks.xy
        for i, b in enumerate(r.boxes):
            cls = int(b.cls.item()); conf = float(b.conf.item())
            label = str(self.names.get(cls, cls)) if isinstance(self.names, dict) else str(self.names[cls])
            asset = _map_label(label, self.table, self.default)
            if asset == AssetType.UNKNOWN and self.role == "general":
                continue  # COCO classes irrelevant to road audit
            x1, y1, x2, y2 = [float(v) for v in b.xyxy[0].tolist()]
            poly = [(float(p[0]), float(p[1])) for p in polys[i]] if polys is not None and i < len(polys) else None
            attrs = {"model": self.name}
            if self.role == "general" and label in ("bench", "fire hydrant", "umbrella", "potted plant", "parking meter"):
                conf *= 0.6      # proxy classes (bench~bus stop, hydrant~bollard, umbrella~hawker): weak evidence on their own
                attrs["proxy_class"] = label
            if self.role == "sign":
                attrs["text"] = label
                digits = "".join(ch for ch in label if ch.isdigit())
                if asset == AssetType.SIGN_SPEED_LIMIT and digits:
                    attrs["speed_limit_kmph"] = int(digits)
            out.append(Detection(asset=asset, label=label, confidence=conf, bbox=BBox(x1=x1, y1=y1, x2=x2, y2=y2),
                                 polygon=poly, frame_index=frame.index, frame_t=frame.t, source=Source.YOLO, attributes=attrs))
        return out
