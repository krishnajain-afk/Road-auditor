"""Build the chainage-indexed RoadModel from frames, detections, assets and per-frame metrics."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Sequence

import numpy as np

from .geometry.road import curve_radius_from_track, design_speed_for, gradient_from_track, heading_change_hotspots
from .schemas import (Asset, AssetType, CameraModel, Detection, FrameRef, GeoPoint, Measurement, MediaMeta,
                      RoadClass, RoadModel, Segment, Terrain)


def _median(vals):
    vals = [v for v in vals if v is not None and not (isinstance(v, float) and np.isnan(v))]
    return float(np.median(vals)) if vals else None


def build_road_model(
    media: MediaMeta, frames: List[FrameRef], track: List[GeoPoint], cam: CameraModel,
    detections: Sequence[Detection], assets: List[Asset], frame_metrics: Dict[int, Dict],
    moving_counts: Dict[int, Dict[str, int]], road_class: RoadClass, terrain: Terrain,
    design_speed: Optional[float], posted_speed: Optional[float], segment_len: float = 50.0,
    context: Optional[Dict] = None,
) -> RoadModel:
    rm = RoadModel(road_class=road_class, terrain=terrain, design_speed_kmph=design_speed or design_speed_for(road_class, terrain),
                   posted_speed_kmph=posted_speed, track=list(track), frames=frames, assets=assets, camera=cam, media=media,
                   context=context or {})
    chs = [f.chainage_m for f in frames if f.chainage_m is not None]
    length = max(chs) if chs else 0.0
    rm.length_m = float(length)

    # ---------------- measurements from per-frame metrics
    meas: List[Measurement] = []
    for fr in frames:
        m = frame_metrics.get(fr.index, {})
        ch = fr.chainage_m or 0.0
        if m.get("carriageway_width_m"):
            meas.append(Measurement(name="carriageway_width_m", value=float(m["carriageway_width_m"]), unit="m", chainage_m=ch,
                                    confidence=float(m.get("carriageway_conf", 0.4)), method="ipm", frame_index=fr.index, geo=fr.geo))
        for lw in m.get("lane_widths_m", []) or []:
            meas.append(Measurement(name="lane_width_m", value=float(lw), unit="m", chainage_m=ch, confidence=0.55, method="ipm",
                                    frame_index=fr.index, geo=fr.geo))
        for lw in m.get("line_widths_m", []) or []:
            meas.append(Measurement(name="marking_line_width_m", value=float(lw), unit="m", chainage_m=ch, confidence=0.5, method="ipm",
                                    frame_index=fr.index, geo=fr.geo))
        if m.get("footpath_width_m"):
            meas.append(Measurement(name="footpath_width_m", value=float(m["footpath_width_m"]), unit="m", chainage_m=ch, confidence=0.5,
                                    method="ipm", frame_index=fr.index, geo=fr.geo))
            meas.append(Measurement(name="footpath_present", value=1.0, unit="", chainage_m=ch, confidence=0.5, method="ipm", frame_index=fr.index, geo=fr.geo))
        if "road_luma" in m:
            meas.append(Measurement(name="road_luma", value=float(m["road_luma"]), unit="0-255", chainage_m=ch, confidence=0.6,
                                    method="photometric", frame_index=fr.index, geo=fr.geo))
            meas.append(Measurement(name="luma_uniformity", value=float(m["luma_uniformity"]), unit="ratio", chainage_m=ch,
                                    confidence=0.5, method="photometric", frame_index=fr.index, geo=fr.geo))
        for k, v in m.items():
            if k.startswith("vlm_") and isinstance(v, (int, float)):
                meas.append(Measurement(name=k[4:], value=float(v), unit="", chainage_m=ch, confidence=0.6, method="vlm",
                                        frame_index=fr.index, geo=fr.geo))
    # ---------------- GPS derived geometry
    if len(track) >= 5:
        for ch, r, c in curve_radius_from_track(track):
            meas.append(Measurement(name="curve_radius_m", value=r, unit="m", chainage_m=ch, confidence=c, method="gps"))
        for ch, g, c in gradient_from_track(track):
            meas.append(Measurement(name="gradient_pct", value=g, unit="%", chainage_m=ch, confidence=c, method="gps"))
        for p in track:
            if p.speed_mps is not None:
                pass
    rm.measurements = meas

    # ---------------- segments
    n_seg = max(1, int(np.ceil((length + 1e-6) / segment_len))) if length > 0 else 1
    segs: List[Segment] = []
    for i in range(n_seg):
        s0, s1 = i * segment_len, min(length, (i + 1) * segment_len) if length > 0 else segment_len
        seg = Segment(segment_id=f"S{i + 1:03d}", start_m=float(s0), end_m=float(s1))
        fidx = [f.index for f in frames if f.chainage_m is not None and s0 <= f.chainage_m < s1 + (1e-6 if i == n_seg - 1 else 0)]
        if not fidx and length == 0:
            fidx = [f.index for f in frames]
        seg.frame_indices = fidx
        fr_by = {f.index: f for f in frames}
        geos = [fr_by[j].geo for j in fidx if fr_by[j].geo]
        if geos:
            seg.start_geo, seg.end_geo = geos[0], geos[-1]
        # metrics
        by_name: Dict[str, List[float]] = defaultdict(list)
        for mm in meas:
            if s0 - 1e-6 <= mm.chainage_m <= s1 + 1e-6 or (length == 0):
                by_name[mm.name].append(mm.value)
        for k, v in by_name.items():
            if k == "curve_radius_m":
                seg.metrics[k] = float(np.min(v))          # sharpest curve governs
            elif k == "gradient_pct":
                seg.metrics[k] = float(np.max(np.abs(v)))
            elif k == "lane_width_m":
                seg.metrics[k] = float(np.percentile(v, 25))   # conservative: narrowest typical lane
                seg.metrics["lane_width_median_m"] = float(np.median(v))
            else:
                seg.metrics[k] = float(np.median(v))
        # asset counts
        for a in assets:
            if s0 - 1e-6 <= a.chainage_m <= s1 + 1e-6 or length == 0:
                seg.counts[a.asset.value] = seg.counts.get(a.asset.value, 0) + 1
        # moving road user exposure (mean per frame)
        mv: Dict[str, List[int]] = defaultdict(list)
        for j in fidx:
            c = moving_counts.get(j, {})
            for k in ("pedestrian", "cyclist", "motorcycle", "car", "bus", "truck", "animal", "auto_rickshaw"):
                mv[k].append(c.get(k, 0))
        for k, v in mv.items():
            if v:
                seg.metrics[f"{k}_per_frame"] = float(np.mean(v))
                seg.counts[f"{k}_max"] = int(np.max(v))
        night = [fr_by[j].is_night for j in fidx if fr_by[j].is_night is not None]
        seg.flags["is_night"] = bool(night and np.mean(night) > 0.5)
        seg.flags["has_zebra"] = seg.counts.get("zebra_crossing", 0) > 0
        seg.flags["has_signal"] = any(a.asset == AssetType.TRAFFIC_SIGNAL and a.confidence >= 0.6 and a.attributes.get("n_frames", 1) >= 2
                                      and (s0 - 1e-6 <= a.chainage_m <= s1 + 1e-6 or length == 0) for a in assets)
        seg.flags["has_stop_line"] = seg.counts.get("stop_line", 0) > 0
        seg.flags["has_hump"] = seg.counts.get("speed_hump", 0) > 0
        seg.flags["has_footpath"] = bool(seg.metrics.get("footpath_present", 0) > 0.5) if "footpath_present" in seg.metrics else False
        seg.flags["footpath_assessed"] = "footpath_present" in seg.metrics
        seg.flags["is_intersection"] = seg.flags["has_signal"] or seg.flags["has_stop_line"] or bool(seg.metrics.get("intersection_present", 0) > 0.5)
        segs.append(seg)
    # junction hints from GPS heading changes
    if len(track) >= 5:
        for ch, d in heading_change_hotspots(track):
            for seg in segs:
                if seg.start_m <= ch < seg.end_m:
                    seg.flags["sharp_heading_change"] = True
                    seg.metrics["heading_change_deg"] = float(abs(d))
    rm.segments = segs
    return rm
