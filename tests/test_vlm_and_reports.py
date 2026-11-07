import json
import os

from cfi_road_auditor.schemas import AssetType, FrameRef
from cfi_road_auditor.vlm.claude_vision import vlm_to_detections, vlm_to_metrics, CHECKLIST_SCHEMA


SAMPLE = {
    "footpath": {"present": True, "both_sides": False, "clear_width_m": 1.2, "obstructed": True, "kerb_height_m": 0.15, "continuous": False},
    "carriageway": {"lanes_visible": 2, "lane_width_m": 3.3, "carriageway_width_m": 6.8, "divided": False, "median_type": "none",
                    "median_opening_visible": False, "surface_condition": "fair", "waterlogging": True, "edge_drop": False},
    "markings": {"centre_line": True, "lane_lines": False, "edge_lines": False, "condition": "faded", "zebra_crossing": True,
                 "zebra_condition": "faded", "stop_line": False, "arrows": False},
    "signs": [{"type": "speed_limit", "text": "40", "condition": "good", "mounting_height_m": 2.2, "side": "left"},
              {"type": "cautionary", "text": None, "condition": "obscured", "mounting_height_m": None, "side": "right"}],
    "signals": {"present": True, "working": False, "pedestrian_signal": False, "countdown": False},
    "traffic_calming": {"speed_hump": True, "hump_marked": False, "hump_signed": False, "rumble_strip": False, "speed_table": False},
    "roadside": {"crash_barrier": False, "barrier_condition": None, "rigid_objects_near_edge": True, "trees_in_clear_zone": False,
                 "guardrail_pedestrian": False, "street_lights": True, "poles_on_footpath": True},
    "context": {"intersection": True, "intersection_type": "signalised", "school_zone": True, "hospital_zone": False, "bus_stop": True,
                "bus_bay": False, "work_zone": False, "work_zone_signed": None, "night": False, "lighting_adequate": None, "weather": "clear"},
    "hazards": [{"type": "open_manhole", "severity": "critical", "where": "carriageway", "bbox": [0.4, 0.6, 0.5, 0.7], "note": "cover missing"},
                {"type": "hawker", "severity": "medium", "where": "footpath", "bbox": [0.0, 0.5, 0.2, 0.9], "note": "stall"}],
    "counts": {"pedestrians_on_carriageway": 3, "pedestrians_on_footpath": 2, "two_wheelers": 5, "cars": 2, "buses_trucks": 0, "autos": 1, "cyclists": 0, "animals": 1},
    "auditor_notes": ["Footpath blocked by hawkers forcing pedestrians onto carriageway"],
}


def test_vlm_conversion_and_metrics():
    fr = FrameRef(index=3, t=3.0, path="x", chainage_m=90.0)
    dets = vlm_to_detections(fr, SAMPLE, 1280, 720)
    types = {d.asset for d in dets}
    assert {AssetType.SIGN_SPEED_LIMIT, AssetType.SIGN_CAUTIONARY, AssetType.TRAFFIC_SIGNAL, AssetType.SPEED_HUMP, AssetType.ZEBRA_CROSSING,
            AssetType.OPEN_MANHOLE, AssetType.HAWKER_ENCROACHMENT, AssetType.SCHOOL_ZONE, AssetType.BUS_STOP, AssetType.WATERLOGGING,
            AssetType.INTERSECTION, AssetType.STREET_LIGHT} <= types
    hump = next(d for d in dets if d.asset == AssetType.SPEED_HUMP)
    assert hump.attributes["marked"] is False
    sig = next(d for d in dets if d.asset == AssetType.TRAFFIC_SIGNAL)
    assert sig.attributes["working"] is False
    mh = next(d for d in dets if d.asset == AssetType.OPEN_MANHOLE)
    assert mh.bbox is not None and abs(mh.bbox.x1 - 0.4 * 1280) < 1e-6
    m = vlm_to_metrics(SAMPLE)
    assert m["vlm_footpath_present"] == 1.0 and m["vlm_footpath_width_m"] == 1.2 and m["vlm_footpath_obstructed"] == 1.0
    assert m["vlm_intersection_present"] == 1.0
    json.dumps(CHECKLIST_SCHEMA)  # schema must be serialisable for the prompt


def test_end_to_end_image_outputs(tmp_path):
    from cfi_road_auditor.config import AuditConfig, PerceptionConfig
    from cfi_road_auditor.pipeline import audit
    from cfi_road_auditor.eval.synth import SceneSpec, write_scene
    ip, _ = write_scene(SceneSpec(zebra_at_m=12, stop_line_at_m=9.5, potholes=[(0.8, 9, 0.6, 0.5)], signs=[("cautionary", 4.5, 18)]), str(tmp_path), "s")
    cfg = AuditConfig(perception=PerceptionConfig(use_classical=True, yolo_weights="__none__"), out_dir=tmp_path / "out", verbose=False)
    cfg.perception.yolo_weights = None
    rep = audit(ip, cfg)
    assert rep.outputs.get("html") and rep.outputs.get("json") and rep.outputs.get("dxf") and rep.outputs.get("xlsx")
    assert any(a.asset == AssetType.ZEBRA_CROSSING for a in rep.road_model.assets)
    assert rep.checklist and len(rep.checklist) == 66
    assert rep.summary.n_findings >= 1
