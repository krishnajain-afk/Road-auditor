"""Temporal fusion: many per-frame detections -> de-duplicated, chainage-referenced Assets.

Strategy (works for sparse 1 fps sampling where IoU tracking fails):
  1. Project each detection to ground (IPM) when it is a road-plane object; estimate chainage =
     frame chainage + forward distance.  For vertical objects use frame chainage + a nominal range.
  2. Cluster per AssetType along chainage with a type-specific gate (e.g. 8 m for potholes, 25 m for signs,
     40 m for zebra crossings) and lateral side agreement.
  3. Asset confidence = 1 - prod(1 - conf_i) capped, boosted by the number of frames in which it was seen.
Moving objects (vehicles, pedestrians, animals) are not de-duplicated into assets; they are counted per segment.
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Dict, List, Optional, Sequence

import numpy as np

from ..geometry.camera import IPM
from ..schemas import Asset, AssetType, CameraModel, Detection, FrameRef, Source

ROAD_PLANE = {AssetType.POTHOLE, AssetType.CRACK_LONGITUDINAL, AssetType.CRACK_TRANSVERSE, AssetType.CRACK_ALLIGATOR,
              AssetType.PATCH, AssetType.ZEBRA_CROSSING, AssetType.STOP_LINE, AssetType.SPEED_HUMP, AssetType.RUMBLE_STRIP,
              AssetType.MANHOLE, AssetType.OPEN_MANHOLE, AssetType.WATERLOGGING, AssetType.DEBRIS, AssetType.LANE_LINE,
              AssetType.CENTRE_LINE, AssetType.EDGE_LINE, AssetType.GIVE_WAY_MARKING, AssetType.ARROW_MARKING,
              AssetType.HATCHING, AssetType.YELLOW_BOX, AssetType.KERB}
MOVING = {AssetType.PEDESTRIAN, AssetType.CYCLIST, AssetType.MOTORCYCLE, AssetType.CAR, AssetType.AUTO_RICKSHAW,
          AssetType.BUS, AssetType.TRUCK, AssetType.ANIMAL, AssetType.WRONG_SIDE_VEHICLE}
GATE_M = defaultdict(lambda: 15.0, {
    AssetType.POTHOLE: 6.0, AssetType.CRACK_LONGITUDINAL: 10.0, AssetType.CRACK_TRANSVERSE: 6.0, AssetType.CRACK_ALLIGATOR: 10.0,
    AssetType.ZEBRA_CROSSING: 30.0, AssetType.STOP_LINE: 25.0, AssetType.SPEED_HUMP: 25.0, AssetType.RUMBLE_STRIP: 20.0,
    AssetType.TRAFFIC_SIGNAL: 40.0, AssetType.SIGN_STOP: 30.0, AssetType.SIGN_MANDATORY: 30.0, AssetType.SIGN_CAUTIONARY: 30.0,
    AssetType.SIGN_INFORMATORY: 30.0, AssetType.SIGN_UNKNOWN: 30.0, AssetType.POLE: 15.0, AssetType.STREET_LIGHT: 20.0,
    AssetType.LANE_LINE: 1e9, AssetType.CENTRE_LINE: 1e9, AssetType.KERB: 60.0, AssetType.MANHOLE: 6.0,
})
NOMINAL_RANGE_M = 15.0   # for objects we cannot project (above horizon)
MIN_OBS_FOR_ASSET = {AssetType.POTHOLE: 1, AssetType.ZEBRA_CROSSING: 1}


def localise(det: Detection, frame: FrameRef, ipm: IPM) -> None:
    """Fill det.ground_xy_m / ground_size_m / chainage_m / geo in place."""
    if det.bbox is None:
        det.chainage_m = frame.chainage_m
        det.geo = frame.geo
        return
    fwd = NOMINAL_RANGE_M
    if det.asset in ROAD_PLANE:
        gs = ipm.bbox_ground_size(det.bbox.x1, det.bbox.y1, det.bbox.x2, det.bbox.y2)
        if gs:
            w, l, lat, fwd = gs
            det.ground_xy_m = (lat, fwd)
            det.ground_size_m = (w, l)
    else:
        g = ipm.pixel_to_ground(det.bbox.cx, det.bbox.y2)
        if g and 1.0 < g[1] < 80.0:
            det.ground_xy_m = g
            fwd = g[1]
    if "forward_m" in det.attributes:
        fwd = float(det.attributes["forward_m"])
    elif det.asset in (AssetType.TRAFFIC_SIGNAL,) and det.bbox is not None:
        fwd = float(np.clip(ipm.range_from_width(det.bbox.w, 0.35), 5, 80))   # signal head ~300-350 mm wide
        det.attributes["forward_m"] = round(fwd, 1)
    elif det.asset in (AssetType.SIGN_STOP, AssetType.SIGN_UNKNOWN) and det.bbox is not None:
        fwd = float(np.clip(ipm.range_from_width(det.bbox.w, 0.75), 4, 80))
        det.attributes["forward_m"] = round(fwd, 1)
        det.attributes.setdefault("mounting_height_m", round(ipm.height_above_ground(det.bbox.y2, fwd), 2))
    if det.asset in (AssetType.POLE, AssetType.STREET_LIGHT, AssetType.TREE) and "lateral_m" in det.attributes:
        half = float(frame_half_width(frame)) if frame_half_width(frame) else 3.5
        det.attributes["lateral_offset_m"] = round(max(0.0, abs(float(det.attributes["lateral_m"])) - half), 2)
    det.chainage_m = (frame.chainage_m or 0.0) + fwd
    det.geo = frame.geo


_FRAME_HALF: Dict[int, float] = {}


def set_frame_half_widths(frame_metrics: Dict[int, Dict]) -> None:
    _FRAME_HALF.clear()
    for k, m in frame_metrics.items():
        w = m.get("carriageway_width_m")
        if w:
            _FRAME_HALF[k] = float(w) / 2


def frame_half_width(frame: FrameRef) -> Optional[float]:
    return _FRAME_HALF.get(frame.index)


def _side(det: Detection, cam: CameraModel) -> str:
    if det.ground_xy_m is not None:
        lat = det.ground_xy_m[0]
        return "left" if lat < -1.0 else ("right" if lat > 1.0 else "centre")
    if det.bbox is None:
        return "centre"
    return "left" if det.bbox.cx < cam.width_px * 0.4 else ("right" if det.bbox.cx > cam.width_px * 0.6 else "centre")


def fuse(detections: Sequence[Detection], frames: Dict[int, FrameRef], cam: CameraModel) -> List[Asset]:
    ipm = IPM(cam)
    by_type: Dict[AssetType, List[Detection]] = defaultdict(list)
    for d in detections:
        fr = frames.get(d.frame_index)
        if fr is None:
            continue
        if d.chainage_m is None:
            localise(d, fr, ipm)
        if d.asset in MOVING:
            continue
        by_type[d.asset].append(d)
    assets: List[Asset] = []
    counter = 0
    for atype, dets in by_type.items():
        dets.sort(key=lambda d: d.chainage_m or 0.0)
        gate = GATE_M[atype]
        clusters: List[List[Detection]] = []
        for d in dets:
            placed = False
            for cl in clusters[-6:]:
                last = cl[-1]
                same_side = _side(d, cam) == _side(last, cam) or atype in (AssetType.ZEBRA_CROSSING, AssetType.STOP_LINE, AssetType.SPEED_HUMP, AssetType.RUMBLE_STRIP)
                if abs((d.chainage_m or 0) - (last.chainage_m or 0)) <= gate and same_side:
                    cl.append(d); placed = True; break
            if not placed:
                clusters.append([d])
        for cl in clusters:
            counter += 1
            best = max(cl, key=lambda d: d.confidence)
            fr = frames.get(best.frame_index)
            p_miss = float(np.prod([1 - min(0.95, d.confidence) for d in cl]))
            n_frames = len({d.frame_index for d in cl})
            conf = 1 - p_miss
            if n_frames >= 2:
                conf = min(0.99, conf + 0.05 * (n_frames - 1))
            # single low-confidence classical pothole observations are kept but flagged
            attrs: Dict = {"n_frames": n_frames}
            for d in cl:
                for k, v in d.attributes.items():
                    if k in ("frame_metrics", "model"):
                        continue
                    attrs.setdefault(k, v)
            # median of numeric measured attributes
            for k in list(attrs):
                vals = [d.attributes.get(k) for d in cl if isinstance(d.attributes.get(k), (int, float))]
                if len(vals) >= 2:
                    attrs[k] = float(np.median(vals))
            sizes = [d.ground_size_m for d in cl if d.ground_size_m]
            size = tuple(float(np.median([s[i] for s in sizes])) for i in (0, 1)) if sizes else None
            ch = float(np.median([d.chainage_m or 0 for d in cl]))
            sources = sorted({d.source for d in cl}, key=lambda s: s.value)
            assets.append(Asset(
                asset_id=f"A{counter:04d}", asset=atype, chainage_m=ch,
                chainage_end_m=(ch + size[1]) if size and atype == AssetType.ZEBRA_CROSSING else None,
                geo=best.geo, side=_side(best, cam), confidence=float(conf), n_observations=len(cl),
                best_frame_index=best.frame_index, best_frame_path=fr.path if fr else None,
                bbox_in_best_frame=best.bbox, size_m=size, attributes=attrs, sources=sources))
    assets.sort(key=lambda a: a.chainage_m)
    for i, a in enumerate(assets, 1):
        a.asset_id = f"A{i:04d}"
    return assets


def count_moving_per_frame(detections: Sequence[Detection]) -> Dict[int, Dict[str, int]]:
    out: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for d in detections:
        if d.asset in MOVING:
            out[d.frame_index][d.asset.value] += 1
    return out
