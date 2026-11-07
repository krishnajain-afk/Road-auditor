import cv2
import numpy as np

from cfi_road_auditor.eval.synth import SceneSpec, render
from cfi_road_auditor.geometry.camera import IPM, build_camera, calibrate_pitch_from_frames, estimate_vanishing_point
from cfi_road_auditor.perception.classical import ClassicalDetector
from cfi_road_auditor.schemas import AssetType, FrameRef


def _scene(**kw):
    spec = SceneSpec(**kw)
    img, gt, cam = render(spec)
    return spec, img, gt, cam


def test_vanishing_point_recovers_pitch():
    for pitch in (1.5, 3.0, 5.5):
        spec, img, gt, true_cam = _scene(pitch_deg=pitch, seed=3)
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cam = build_camera(spec.width_px, spec.height_px, spec.hfov_deg, spec.cam_height_m, 2.0)
        cam = calibrate_pitch_from_frames([g], cam)
        assert abs(cam.pitch_deg - pitch) < 0.4, (pitch, cam.pitch_deg)


def test_classical_detects_zebra_stop_hump_and_measures():
    spec, img, gt, cam = _scene(zebra_at_m=12, zebra_stripe_m=0.5, stop_line_at_m=9.5, potholes=[(0.8, 9, 0.6, 0.5)],
                                signs=[("cautionary", 4.5, 18), ("stop", -4.4, 22)], signal_at=(4.2, 20), pitch_deg=3.0)
    det = ClassicalDetector(cam)
    dets = det.detect(img, FrameRef(index=0, t=0.0, path="x"), cam)
    by = {}
    for d in dets:
        by.setdefault(d.asset, []).append(d)
    z = by[AssetType.ZEBRA_CROSSING][0]
    assert abs(z.attributes["stripe_width_m"] - 0.5) < 0.1
    assert abs(z.attributes["forward_m"] - 12) < 1.0
    assert AssetType.STOP_LINE in by and abs(by[AssetType.STOP_LINE][0].attributes["forward_m"] - 9.5) < 1.0
    assert AssetType.POTHOLE in by
    p = by[AssetType.POTHOLE][0]
    assert abs(p.attributes["forward_m"] - 9) < 1.0 and abs(p.attributes["lateral_m"] - 0.8) < 0.5
    assert AssetType.SIGN_CAUTIONARY in by and AssetType.SIGN_STOP in by and AssetType.TRAFFIC_SIGNAL in by
    m = det.last_metrics
    assert abs(m["carriageway_width_m"] - 7.0) < 0.35
    assert m["lane_widths_m"] and abs(np.median(m["lane_widths_m"]) - 3.5) < 0.2
    # zebra scale hint ~ 1.0 when the height is right
    assert det.last_scale_hint is not None and abs(det.last_scale_hint - 1.0) < 0.1


def test_hump_not_confused_with_zebra():
    spec, img, gt, cam = _scene(hump_at_m=11, hump_marked=True, pitch_deg=3.0, seed=5)
    dets = ClassicalDetector(cam).detect(img, FrameRef(index=0, t=0.0, path="x"), cam)
    types = [d.asset for d in dets]
    assert AssetType.SPEED_HUMP in types and AssetType.ZEBRA_CROSSING not in types
    spec, img, gt, cam = _scene(zebra_at_m=11, pitch_deg=3.0, seed=6)
    dets = ClassicalDetector(cam).detect(img, FrameRef(index=0, t=0.0, path="x"), cam)
    types = [d.asset for d in dets]
    assert AssetType.ZEBRA_CROSSING in types and AssetType.SPEED_HUMP not in types
