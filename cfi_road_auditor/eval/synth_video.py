"""Synthetic survey drive: a 1 km corridor with known assets, rendered frame by frame from a moving camera, written as
an MP4 plus a GPX track. Exercises the full video pipeline (frame extraction, GPS sync, chainage, temporal fusion,
spacing rules) with exact ground truth for end-to-end evaluation.
"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import cv2
import numpy as np

from .synth import SceneSpec, render

EARTH = 6371008.8


@dataclass
class Corridor:
    length_m: float = 600.0
    speed_kmph: float = 30.0
    fps: float = 10.0
    lane_width_m: float = 3.5
    n_lanes: int = 2
    zebras: List[float] = field(default_factory=lambda: [120.0, 420.0])          # chainage of near edge
    stop_lines: List[float] = field(default_factory=lambda: [117.0])
    humps: List[Tuple[float, bool]] = field(default_factory=lambda: [(260.0, True), (520.0, False)])
    potholes: List[Tuple[float, float, float, float]] = field(default_factory=lambda: [(60.0, 0.9, 0.6, 0.5), (300.0, -1.2, 0.8, 0.6), (305.0, 1.5, 0.4, 0.4), (480.0, 0.3, 0.5, 0.5)])
    signs: List[Tuple[str, float, float]] = field(default_factory=lambda: [("cautionary", 80.0, 4.5), ("mandatory", 200.0, -4.4), ("cautionary", 225.0, 4.5), ("stop", 410.0, 4.5)])
    signals: List[Tuple[float, float]] = field(default_factory=lambda: [(125.0, 4.3)])
    poles: List[Tuple[float, float]] = field(default_factory=lambda: [(50.0, -5.2), (150.0, -5.2), (250.0, -5.2), (350.0, -5.2), (450.0, -5.2), (550.0, -5.2)])
    curve: Tuple[float, float, float] = (330.0, 420.0, 120.0)   # chainage start/end and radius of a horizontal curve (GPS only)
    cam_height_m: float = 1.35
    pitch_deg: float = 3.0
    lat0: float = 18.5204
    lon0: float = 73.8567
    seed: int = 7


def _frame_spec(c: Corridor, ch: float, horizon: float = 45.0) -> SceneSpec:
    """Everything within `horizon` metres ahead of chainage `ch` becomes a SceneSpec in camera-relative coordinates."""
    s = SceneSpec(seed=c.seed, lane_width_m=c.lane_width_m, n_lanes=c.n_lanes, cam_height_m=c.cam_height_m, pitch_deg=c.pitch_deg,
                  dashed=True, yellow_centre=False, noise=7.0)
    for z in c.zebras:
        if 2.0 < z - ch < horizon:
            s.zebra_at_m = z - ch; s.zebra_length_m = 3.0; break
    for z in c.stop_lines:
        if 2.0 < z - ch < horizon:
            s.stop_line_at_m = z - ch; break
    for z, marked in c.humps:
        if 2.0 < z - ch < horizon:
            s.hump_at_m = z - ch; s.hump_marked = marked; break
    s.potholes = [(lat, z - ch, w, l) for z, lat, w, l in c.potholes if 2.0 < z - ch < horizon]
    s.signs = [(k, lat, z - ch) for k, z, lat in c.signs if 3.0 < z - ch < horizon]
    for z, lat in c.signals:
        if 3.0 < z - ch < horizon:
            s.signal_at = (lat, z - ch); break
    s.poles = [(lat, z - ch) for z, lat in c.poles if 3.0 < z - ch < horizon]
    return s


def track_points(c: Corridor, dt: float) -> List[Tuple[float, float, float, float]]:
    """(t, lat, lon, chainage) following a straight line with one circular curve segment."""
    v = c.speed_kmph / 3.6
    pts = []
    x = y = 0.0; heading = 0.0
    t = 0.0; ch = 0.0
    cs, ce, R = c.curve
    step = v * dt
    while ch <= c.length_m:
        lat = c.lat0 + y / 111320.0
        lon = c.lon0 + x / (111320.0 * math.cos(math.radians(c.lat0)))
        pts.append((t, lat, lon, ch))
        if cs <= ch < ce:
            heading += step / R
        x += step * math.cos(heading); y += step * math.sin(heading)
        ch += step; t += dt
    return pts


def write_gpx(pts, path: str, start_iso: str = "2026-11-07T06:30:00Z"):
    from datetime import datetime, timedelta, timezone
    t0 = datetime(2026, 11, 7, 6, 30, 0, tzinfo=timezone.utc)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="CFI synth"><trk><name>synthetic survey</name><trkseg>']
    for t, lat, lon, ch in pts:
        ts = (t0 + timedelta(seconds=t)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        # add realistic GNSS noise (1.5 m sigma) so curve/gradient estimators are stressed
        n_lat = np.random.normal(0, 1.5) / 111320.0; n_lon = np.random.normal(0, 1.5) / 111320.0
        lines.append(f'<trkpt lat="{lat + n_lat:.7f}" lon="{lon + n_lon:.7f}"><ele>{560 + 0.02 * ch:.1f}</ele><time>{ts}</time></trkpt>')
    lines.append("</trkseg></trk></gpx>")
    with open(path, "w") as f:
        f.write("\n".join(lines))


def write_video(c: Corridor, out_dir: str, name: str = "synthetic_drive") -> Dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)
    np.random.seed(c.seed)
    dt = 1.0 / c.fps
    pts = track_points(c, dt)
    vp = os.path.join(out_dir, f"{name}.mp4")
    gp = os.path.join(out_dir, f"{name}.gpx")
    jp = os.path.join(out_dir, f"{name}.json")
    w, h = 1280, 720
    vw = cv2.VideoWriter(vp, cv2.VideoWriter_fourcc(*"mp4v"), c.fps, (w, h))
    for i, (t, lat, lon, ch) in enumerate(pts):
        spec = _frame_spec(c, ch)
        spec.seed = c.seed + i
        img, _, _ = render(spec)
        vw.write(img)
    vw.release()
    # media creation time must match the GPX clock for alignment: we re-mux with ffmpeg to set creation_time
    tmp = vp + ".tmp.mp4"
    os.replace(vp, tmp)
    os.system(f'ffmpeg -v quiet -y -i "{tmp}" -c copy -metadata creation_time="2026-11-07T06:30:00.000000Z" "{vp}"')
    os.remove(tmp)
    write_gpx(pts, gp)
    gt = {"corridor": {k: v for k, v in c.__dict__.items()}, "n_frames": len(pts)}
    with open(jp, "w") as f:
        json.dump(gt, f, indent=1, default=str)
    return {"video": vp, "gpx": gp, "gt": jp}


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "tests/fixtures/synth_video"
    print(write_video(Corridor(), out))
