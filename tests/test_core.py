import math
import numpy as np
import pytest

from cfi_road_auditor.geometry.camera import IPM, build_camera
from cfi_road_auditor.geometry.road import curve_radius_from_track, irc_min_radius_table, stopping_sight_distance
from cfi_road_auditor.ingest.gps import haversine_m, parse_iso6709, sync_track_to_frames
from cfi_road_auditor.rules.engine import RuleEngine
from cfi_road_auditor.schemas import FrameRef, GeoPoint, RoadClass, RoadModel, Segment, Asset, AssetType, Likelihood, Severity
from cfi_road_auditor.scoring.risk import risk_from, summarise


def test_ipm_roundtrip():
    cam = build_camera(1280, 720, 70, 1.3, 3.0)
    ipm = IPM(cam)
    for x, z in ((0, 10), (-3.5, 8), (2.0, 25)):
        u, v = ipm.ground_to_pixel(x, z)
        g = ipm.pixel_to_ground(u, v)
        assert g is not None and abs(g[0] - x) < 1e-6 and abs(g[1] - z) < 1e-6
    assert ipm.pixel_to_ground(640, 10) is None  # above horizon


def test_height_above_ground():
    cam = build_camera(1280, 720, 70, 1.3, 3.0)
    ipm = IPM(cam)
    # a point 2.1 m high at 20 m: project then recover
    z = 20.0; H = 2.1
    c, s = math.cos(math.radians(3)), math.sin(math.radians(3))
    yc = (cam.height_m - H) * c - z * s; zc = (cam.height_m - H) * s + z * c
    v = cam.cy + cam.fy * yc / zc
    assert abs(ipm.height_above_ground(v, z) - H) < 1e-6


def test_curve_radius_fit():
    R = 150.0
    pts = []
    for i in range(60):
        th = i * 5.0 / R
        pts.append(GeoPoint(lat=18.5 + (R * math.sin(th)) / 111320.0, lon=73.8 + (R * (1 - math.cos(th))) / (111320.0 * math.cos(math.radians(18.5))), t=float(i)))
    out = curve_radius_from_track(pts)
    mid = [r for ch, r, c in out if 100 < ch < 200]
    assert mid and abs(np.median(mid) - R) / R < 0.08


def test_irc_tables():
    assert irc_min_radius_table(60) == 130
    assert 70 < stopping_sight_distance(60) < 100   # IRC:66 SSD at 60 km/h ~ 80-90 m


def test_gps_parsing_and_sync():
    assert parse_iso6709("+18.5204+073.8567+560.000/")[:2] == (18.5204, 73.8567)
    track = [GeoPoint(lat=18.5, lon=73.8, t=0.0), GeoPoint(lat=18.5009, lon=73.8, t=10.0)]
    frames = [FrameRef(index=i, t=float(i * 5), path="x") for i in range(3)]
    sync_track_to_frames(frames, track)
    assert frames[1].chainage_m == pytest.approx(haversine_m(18.5, 73.8, 18.5009, 73.8) / 2, rel=0.01)


def test_risk_matrix():
    assert risk_from(Severity.CRITICAL, Likelihood.FREQUENT)[0] == 16
    assert risk_from(Severity.LOW, Likelihood.IMPROBABLE)[0] == 2


def test_rule_engine_zebra_without_sign():
    rm = RoadModel(road_class=RoadClass.URBAN_ARTERIAL, length_m=300)
    rm.segments = [Segment(segment_id="S001", start_m=0, end_m=300, metrics={"lane_width_m": 3.4, "carriageway_width_m": 7.0, "n_lines": 2})]
    rm.assets = [Asset(asset_id="A1", asset=AssetType.ZEBRA_CROSSING, chainage_m=120, confidence=0.9, attributes={"stripe_width_m": 0.3, "crossing_length_m": 3.0}),
                 Asset(asset_id="A2", asset=AssetType.POTHOLE, chainage_m=40, confidence=0.8, size_m=(0.7, 0.5))]
    f, c = RuleEngine().evaluate(rm)
    ids = {x.rule_id for x in f}
    assert {"MRK-001", "MRK-003", "MRK-004", "PAV-001"} <= ids
    pav = next(x for x in f if x.rule_id == "PAV-001")
    assert pav.severity == Severity.CRITICAL          # 0.7 m wide pothole
    s = summarise(rm, f, c)
    assert 0 <= s.overall_score <= 100 and s.coverage_pct > 0
