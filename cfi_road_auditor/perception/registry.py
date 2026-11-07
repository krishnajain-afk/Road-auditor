"""Tiered detector loading: use whatever weights exist, always keep the classical fallbacks."""
from __future__ import annotations

import logging
import os
from typing import List, Optional

from ..config import MODELS_DIR, PerceptionConfig
from ..schemas import CameraModel
from .base import Detector

log = logging.getLogger(__name__)

WELL_KNOWN = {
    "general": ["yolo11s.pt", "yolov8s.pt", "yolo11n.pt", "yolov8n.pt"],
    "damage": ["rdd_yolov8.pt", "rdd2022_yolov8s.pt", "road_damage.pt", "pothole.pt", "cfi_damage.pt"],
    "sign": ["indian_signs.pt", "traffic_signs.pt", "cfi_signs.pt"],
}


def _resolve(path: Optional[str], role: str) -> Optional[str]:
    if path:
        if os.path.exists(path):
            return path
        cand = MODELS_DIR / path
        if cand.exists():
            return str(cand)
        log.warning("weights not found: %s", path)
    for name in WELL_KNOWN[role]:
        cand = MODELS_DIR / name
        if cand.exists():
            return str(cand)
    return None


def build_detectors(cfg: PerceptionConfig, cam: CameraModel) -> List[Detector]:
    dets: List[Detector] = []
    for role, w in (("general", cfg.yolo_weights), ("damage", cfg.damage_weights), ("sign", cfg.sign_weights)):
        p = _resolve(w, role)
        if p:
            try:
                from .yolo import YoloDetector
                conf = cfg.yolo_conf if role != "damage" else max(0.2, cfg.yolo_conf)
                dets.append(YoloDetector(p, role=role, conf=conf, iou=cfg.yolo_iou, imgsz=cfg.yolo_imgsz, device=cfg.device))
                log.info("loaded %s detector from %s", role, p)
            except Exception as e:  # pragma: no cover
                log.warning("could not load %s weights %s: %s", role, p, e)
    if cfg.use_classical:
        from .classical import ClassicalDetector
        has_damage = any(getattr(d, "role", "") == "damage" for d in dets)
        dets.append(ClassicalDetector(cam, enable_potholes=not has_damage))
    return dets
