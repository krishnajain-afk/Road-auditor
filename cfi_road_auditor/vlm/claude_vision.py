"""Claude vision pass: an auditor-style checklist assessment of key frames.

Why: many IRC:SP:88 checklist items (footpath presence/width/obstruction, sign condition & legibility, barrier
condition, encroachment, drainage, school zone, work zone, signal working, median openings) are semantic
judgements that classical CV and COCO detectors cannot make. A vision-language model does them well when
given the checklist, the standard values and a strict JSON schema. The pass is optional (needs ANTHROPIC_API_KEY)
and its outputs are fused as Detections/metrics with source=VLM.

Frame budget: the pipeline sends at most `max_frames` frames (evenly spaced + frames with assets).
"""
from __future__ import annotations

import base64
import json
import logging
import os
from typing import Any, Dict, List, Optional

from ..schemas import AssetType, BBox, Detection, FrameRef, Source

log = logging.getLogger(__name__)

CHECKLIST_SCHEMA = {
    "footpath": {"present": "bool", "both_sides": "bool", "clear_width_m": "number|null", "obstructed": "bool", "kerb_height_m": "number|null", "continuous": "bool"},
    "carriageway": {"lanes_visible": "int", "lane_width_m": "number|null", "carriageway_width_m": "number|null", "divided": "bool", "median_type": "raised|painted|barrier|none", "median_opening_visible": "bool", "surface_condition": "good|fair|poor", "waterlogging": "bool", "edge_drop": "bool"},
    "markings": {"centre_line": "bool", "lane_lines": "bool", "edge_lines": "bool", "condition": "good|faded|absent", "zebra_crossing": "bool", "zebra_condition": "good|faded|absent|null", "stop_line": "bool", "arrows": "bool"},
    "signs": [{"type": "mandatory|cautionary|informatory|stop|give_way|speed_limit|pedestrian_crossing|speed_breaker|school|other", "text": "string|null", "condition": "good|faded|damaged|obscured", "mounting_height_m": "number|null", "side": "left|right|overhead"}],
    "signals": {"present": "bool", "working": "bool|null", "pedestrian_signal": "bool", "countdown": "bool"},
    "traffic_calming": {"speed_hump": "bool", "hump_marked": "bool|null", "hump_signed": "bool|null", "rumble_strip": "bool", "speed_table": "bool"},
    "roadside": {"crash_barrier": "bool", "barrier_condition": "good|damaged|blunt_end|null", "rigid_objects_near_edge": "bool", "trees_in_clear_zone": "bool", "guardrail_pedestrian": "bool", "street_lights": "bool", "poles_on_footpath": "bool"},
    "context": {"intersection": "bool", "intersection_type": "signalised|roundabout|unsignalised|none", "school_zone": "bool", "hospital_zone": "bool", "bus_stop": "bool", "bus_bay": "bool", "work_zone": "bool", "work_zone_signed": "bool|null", "night": "bool", "lighting_adequate": "bool|null", "weather": "clear|rain|fog|dusk"},
    "hazards": [{"type": "pothole|open_manhole|debris|encroachment|parked_vehicle|wrong_side_vehicle|animal|hawker|construction|drain_uncovered|other", "severity": "low|medium|high|critical", "where": "carriageway|footpath|shoulder", "bbox": "[x1,y1,x2,y2] in 0-1 normalised coords", "note": "string"}],
    "counts": {"pedestrians_on_carriageway": "int", "pedestrians_on_footpath": "int", "two_wheelers": "int", "cars": "int", "buses_trucks": "int", "autos": "int", "cyclists": "int", "animals": "int"},
    "auditor_notes": ["string"],
}

SYSTEM = """You are a certified Indian Road Safety Auditor (IRC:SP:88-2019) examining one survey frame from a
vehicle-mounted or hand-held camera. Assess only what is visible. Use Indian standards for judgement: footpath
clear width >= 1.8 m (IRC:103), lane 3.5 m (IRC:86/73), zebra stripes 0.5 m (IRC:35), sign bottom 2.0-2.5 m in
urban areas (IRC:67), hump 3.7 m x 0.1 m with black/white bands and advance sign (IRC:99), W-beam 0.71 m (IRC:119).
Estimate metres using cues: lane width ~3.5 m, car width ~1.8 m, motorcycle length ~2 m, kerb 0.15 m, sign plate
0.6-0.9 m, adult height 1.65 m. Return ONLY a JSON object following the schema exactly; use null when not
assessable. Never invent assets that are not visible. Bboxes are normalised [x1,y1,x2,y2] in 0-1."""


def _b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode()


class ClaudeVisionAuditor:
    def __init__(self, model: str = "claude-fable-5-1", api_key: Optional[str] = None, max_tokens: int = 2000):
        import anthropic  # type: ignore
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model
        self.max_tokens = max_tokens

    def assess_frame(self, frame: FrameRef, road_class: str) -> Optional[Dict[str, Any]]:
        prompt = (f"Road class: {road_class}. Frame time {frame.t:.1f}s" + (f", chainage {frame.chainage_m:.0f} m" if frame.chainage_m is not None else "") +
                  ".\nSchema:\n" + json.dumps(CHECKLIST_SCHEMA) + "\nRespond with JSON only.")
        try:
            msg = self.client.messages.create(
                model=self.model, max_tokens=self.max_tokens, system=SYSTEM,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": _b64(frame.path)}},
                    {"type": "text", "text": prompt}]}])
            txt = "".join(getattr(b, "text", "") for b in msg.content)
            txt = txt.strip()
            if txt.startswith("```"):
                txt = txt.strip("`")
                txt = txt[txt.find("{"):]
            return json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
        except Exception as e:
            log.warning("VLM frame %s failed: %s", frame.index, e)
            return None


def vlm_to_detections(frame: FrameRef, j: Dict[str, Any], w: int, h: int) -> List[Detection]:
    """Convert a checklist JSON into Detections (for fusion) - only for discrete assets."""
    out: List[Detection] = []
    def add(asset, label, conf=0.6, attrs=None, bbox=None):
        out.append(Detection(asset=asset, label=label, confidence=conf, bbox=bbox, frame_index=frame.index, frame_t=frame.t,
                             source=Source.VLM, attributes=attrs or {}))
    def nb(b):
        try:
            x1, y1, x2, y2 = b
            return BBox(x1=x1 * w, y1=y1 * h, x2=x2 * w, y2=y2 * h)
        except Exception:
            return None
    for s in j.get("signs", []) or []:
        t = s.get("type", "other")
        asset = {"mandatory": AssetType.SIGN_MANDATORY, "cautionary": AssetType.SIGN_CAUTIONARY, "informatory": AssetType.SIGN_INFORMATORY,
                 "stop": AssetType.SIGN_STOP, "give_way": AssetType.SIGN_GIVE_WAY, "speed_limit": AssetType.SIGN_SPEED_LIMIT,
                 "pedestrian_crossing": AssetType.SIGN_PEDESTRIAN_CROSSING, "speed_breaker": AssetType.SIGN_SPEED_BREAKER,
                 "school": AssetType.SIGN_SCHOOL}.get(t, AssetType.SIGN_UNKNOWN)
        add(asset, f"vlm_sign_{t}", 0.6, {"text": s.get("text"), "condition": s.get("condition"), "mounting_height_m": s.get("mounting_height_m"), "side": s.get("side")})
    sg = j.get("signals", {}) or {}
    if sg.get("present"):
        add(AssetType.TRAFFIC_SIGNAL, "vlm_signal", 0.65, {"working": sg.get("working"), "countdown": sg.get("countdown")})
        if sg.get("pedestrian_signal"):
            add(AssetType.PEDESTRIAN_SIGNAL, "vlm_ped_signal", 0.6)
    tc = j.get("traffic_calming", {}) or {}
    if tc.get("speed_hump"):
        add(AssetType.SPEED_HUMP, "vlm_hump", 0.6, {"marked": tc.get("hump_marked"), "signed": tc.get("hump_signed")})
    if tc.get("speed_table"):
        add(AssetType.SPEED_TABLE, "vlm_speed_table", 0.55)
    if tc.get("rumble_strip"):
        add(AssetType.RUMBLE_STRIP, "vlm_rumble", 0.5)
    mk = j.get("markings", {}) or {}
    if mk.get("zebra_crossing"):
        add(AssetType.ZEBRA_CROSSING, "vlm_zebra", 0.6, {"condition": mk.get("zebra_condition")})
    if mk.get("stop_line"):
        add(AssetType.STOP_LINE, "vlm_stop_line", 0.55)
    if mk.get("arrows"):
        add(AssetType.ARROW_MARKING, "vlm_arrow", 0.5)
    rs = j.get("roadside", {}) or {}
    if rs.get("crash_barrier"):
        add(AssetType.CRASH_BARRIER, "vlm_barrier", 0.6, {"condition": rs.get("barrier_condition")})
    if rs.get("guardrail_pedestrian"):
        add(AssetType.GUARDRAIL, "vlm_guardrail", 0.55)
    if rs.get("street_lights"):
        add(AssetType.STREET_LIGHT, "vlm_streetlight", 0.5)
    cx = j.get("context", {}) or {}
    if cx.get("school_zone"):
        add(AssetType.SCHOOL_ZONE, "vlm_school_zone", 0.6)
    if cx.get("work_zone"):
        add(AssetType.WORK_ZONE, "vlm_work_zone", 0.6, {"signed": cx.get("work_zone_signed")})
    if cx.get("bus_stop"):
        add(AssetType.BUS_STOP, "vlm_bus_stop", 0.55)
    if cx.get("bus_bay"):
        add(AssetType.BUS_BAY, "vlm_bus_bay", 0.55)
    if cx.get("intersection"):
        add(AssetType.INTERSECTION, "vlm_intersection", 0.6, {"type": cx.get("intersection_type")})
    if cx.get("intersection_type") == "roundabout":
        add(AssetType.ROUNDABOUT, "vlm_roundabout", 0.6)
    cw = j.get("carriageway", {}) or {}
    if cw.get("median_opening_visible"):
        add(AssetType.MEDIAN_OPENING, "vlm_median_opening", 0.55)
    if cw.get("median_type") in ("raised", "barrier"):
        add(AssetType.MEDIAN, "vlm_median", 0.55, {"type": cw.get("median_type")})
    if cw.get("waterlogging"):
        add(AssetType.WATERLOGGING, "vlm_waterlogging", 0.6)
    hz_map = {"pothole": AssetType.POTHOLE, "open_manhole": AssetType.OPEN_MANHOLE, "debris": AssetType.DEBRIS, "encroachment": AssetType.HAWKER_ENCROACHMENT,
              "hawker": AssetType.HAWKER_ENCROACHMENT, "parked_vehicle": AssetType.PARKED_VEHICLE, "wrong_side_vehicle": AssetType.WRONG_SIDE_VEHICLE,
              "animal": AssetType.ANIMAL, "construction": AssetType.CONSTRUCTION, "drain_uncovered": AssetType.DRAIN}
    for hz in j.get("hazards", []) or []:
        a = hz_map.get(hz.get("type"), AssetType.UNKNOWN)
        if a == AssetType.UNKNOWN:
            continue
        conf = {"critical": 0.75, "high": 0.7, "medium": 0.6, "low": 0.5}.get(hz.get("severity"), 0.55)
        add(a, f"vlm_{hz.get('type')}", conf, {"where": hz.get("where"), "note": hz.get("note"), "vlm_severity": hz.get("severity")}, nb(hz.get("bbox")) if hz.get("bbox") else None)
    return out


def vlm_to_metrics(j: Dict[str, Any]) -> Dict[str, float]:
    """Per-frame scalar metrics (prefixed vlm_) merged into segment metrics by the road model."""
    m: Dict[str, float] = {}
    fp = j.get("footpath", {}) or {}
    if "present" in fp and fp["present"] is not None:
        m["vlm_footpath_present"] = 1.0 if fp["present"] else 0.0
        if fp.get("clear_width_m") is not None:
            m["vlm_footpath_width_m"] = float(fp["clear_width_m"])
        if fp.get("obstructed") is not None:
            m["vlm_footpath_obstructed"] = 1.0 if fp["obstructed"] else 0.0
        if fp.get("kerb_height_m") is not None:
            m["vlm_kerb_height_m"] = float(fp["kerb_height_m"])
    cw = j.get("carriageway", {}) or {}
    if cw.get("lane_width_m") is not None:
        m["vlm_lane_width_vlm_m"] = float(cw["lane_width_m"])
    if cw.get("carriageway_width_m") is not None:
        m["vlm_carriageway_width_vlm_m"] = float(cw["carriageway_width_m"])
    cx = j.get("context", {}) or {}
    if cx.get("intersection") is not None:
        m["vlm_intersection_present"] = 1.0 if cx["intersection"] else 0.0
    if cx.get("lighting_adequate") is not None:
        m["vlm_lighting_adequate"] = 1.0 if cx["lighting_adequate"] else 0.0
    c = j.get("counts", {}) or {}
    for k in ("pedestrians_on_carriageway", "two_wheelers", "cars", "cyclists", "animals", "autos"):
        if c.get(k) is not None:
            m[f"vlm_{k}_vlm"] = float(c[k])
    mk = j.get("markings", {}) or {}
    if mk.get("condition"):
        m["vlm_markings_faded"] = 1.0 if mk["condition"] in ("faded", "absent") else 0.0
    return m
