"""Synthetic road-scene generator with exact ground truth.

Renders a metric top-down road "texture" (asphalt noise, lane lines, zebra, stop line, hump bands, potholes, kerbs)
then projects it through the same pinhole camera model used by the pipeline (so IPM errors are measured, not hidden).
Adds sky/roadside, vertical signs (red triangle/circle, blue rect, STOP octagon), a traffic-signal head and poles.
Outputs a frame + ground-truth JSON. Used by the evaluation harness to measure detection recall/precision and
measurement error (lane width, stripe width, pothole size) against known values.
"""
from __future__ import annotations

import json
import math
import os
import random
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from ..geometry.camera import IPM, build_camera
from ..schemas import CameraModel


@dataclass
class SceneSpec:
    width_px: int = 1280
    height_px: int = 720
    hfov_deg: float = 70.0
    cam_height_m: float = 1.3
    pitch_deg: float = 3.0
    lane_width_m: float = 3.5
    n_lanes: int = 2
    line_width_m: float = 0.10
    dashed: bool = True
    yellow_centre: bool = False
    zebra_at_m: Optional[float] = None          # forward distance of near edge
    zebra_length_m: float = 3.0
    zebra_stripe_m: float = 0.5
    zebra_gap_m: float = 0.5
    stop_line_at_m: Optional[float] = None
    stop_line_thick_m: float = 0.3
    hump_at_m: Optional[float] = None
    hump_len_m: float = 3.7
    hump_marked: bool = True
    potholes: List[Tuple[float, float, float, float]] = field(default_factory=list)   # (lat, fwd, w, l)
    signs: List[Tuple[str, float, float]] = field(default_factory=list)                 # (kind, lateral_m, forward_m)
    signal_at: Optional[Tuple[float, float]] = None
    poles: List[Tuple[float, float]] = field(default_factory=list)
    night: bool = False
    noise: float = 8.0
    seed: int = 0
    asphalt_gray: int = 95
    shadow: bool = False


def render(spec: SceneSpec) -> Tuple[np.ndarray, Dict, CameraModel]:
    rng = np.random.default_rng(spec.seed)
    cam = build_camera(spec.width_px, spec.height_px, spec.hfov_deg, spec.cam_height_m, spec.pitch_deg, "synthetic", 1.0)
    ipm = IPM(cam)
    # --- metric ground texture: x in [-15,15], z in [0,60], 25 px/m
    ppm = 25
    X0, X1, Z0, Z1 = -15.0, 15.0, 0.0, 60.0
    GW, GH = int((X1 - X0) * ppm), int((Z1 - Z0) * ppm)
    road_w = spec.lane_width_m * spec.n_lanes
    g = np.full((GH, GW, 3), 60, np.uint8)  # roadside (dark earth)
    g[:] = (70, 90, 60) if not spec.night else (20, 25, 18)
    def gx(x): return int((x - X0) * ppm)
    def gz(z): return int(GH - (z - Z0) * ppm)
    asphalt = spec.asphalt_gray if not spec.night else 35
    g[:, gx(-road_w / 2):gx(road_w / 2)] = asphalt
    # asphalt noise
    noise = rng.normal(0, spec.noise, (GH, GW)).astype(np.int16)
    g = np.clip(g.astype(np.int16) + noise[:, :, None], 0, 255).astype(np.uint8)
    white = (235, 235, 235) if not spec.night else (160, 160, 160)
    yellow = (40, 200, 230) if not spec.night else (30, 120, 140)
    # kerbs (0.25 m light strip) both sides
    g[:, gx(-road_w / 2 - 0.25):gx(-road_w / 2)] = (150, 150, 150)
    g[:, gx(road_w / 2):gx(road_w / 2 + 0.25)] = (150, 150, 150)
    # footpath
    g[:, gx(-road_w / 2 - 2.0):gx(-road_w / 2 - 0.25)] = (120, 125, 130)
    g[:, gx(road_w / 2 + 0.25):gx(road_w / 2 + 2.0)] = (120, 125, 130)
    gt: Dict = {"lane_width_m": spec.lane_width_m, "n_lanes": spec.n_lanes, "line_width_m": spec.line_width_m, "assets": []}
    # lane lines
    lw = spec.line_width_m
    for i in range(1, spec.n_lanes):
        x = -road_w / 2 + i * spec.lane_width_m
        col = yellow if (spec.yellow_centre and i == spec.n_lanes // 2) else white
        if spec.dashed and not (spec.yellow_centre and i == spec.n_lanes // 2):
            z = 0.0
            while z < Z1:
                g[gz(min(Z1, z + 1.5)):gz(z), gx(x - lw / 2):gx(x + lw / 2)] = col
                z += 4.5
        else:
            g[:, gx(x - lw / 2):gx(x + lw / 2)] = col
        gt["assets"].append({"type": "lane_line", "lateral_m": x, "width_m": lw})
    # edge lines
    for x in (-road_w / 2 + 0.15, road_w / 2 - 0.15):
        g[:, gx(x - 0.075):gx(x + 0.075)] = white
        gt["assets"].append({"type": "lane_line", "lateral_m": x, "width_m": 0.15, "edge": True})
    # zebra
    if spec.zebra_at_m is not None:
        z0, z1 = spec.zebra_at_m, spec.zebra_at_m + spec.zebra_length_m
        x = -road_w / 2 + 0.3
        n = 0
        while x + spec.zebra_stripe_m <= road_w / 2 - 0.3:
            g[gz(z1):gz(z0), gx(x):gx(x + spec.zebra_stripe_m)] = white
            x += spec.zebra_stripe_m + spec.zebra_gap_m; n += 1
        gt["assets"].append({"type": "zebra_crossing", "forward_m": z0, "length_m": spec.zebra_length_m, "stripe_width_m": spec.zebra_stripe_m, "n_stripes": n})
    if spec.stop_line_at_m is not None:
        z0 = spec.stop_line_at_m
        g[gz(z0 + spec.stop_line_thick_m):gz(z0), gx(-road_w / 2 + 0.2):gx(road_w / 2 - 0.2)] = white
        gt["assets"].append({"type": "stop_line", "forward_m": z0, "thickness_m": spec.stop_line_thick_m})
    if spec.hump_at_m is not None:
        z0, z1 = spec.hump_at_m, spec.hump_at_m + spec.hump_len_m
        if spec.hump_marked:
            x = -road_w / 2
            k = 0
            while x < road_w / 2:
                g[gz(z1):gz(z0), gx(x):gx(min(road_w / 2, x + 0.5))] = yellow if k % 2 == 0 else (30, 30, 30)
                x += 0.5; k += 1
        else:
            g[gz(z1):gz(z0), gx(-road_w / 2):gx(road_w / 2)] = max(0, asphalt - 15)
        gt["assets"].append({"type": "speed_hump", "forward_m": z0, "length_m": spec.hump_len_m, "marked": spec.hump_marked})
    for (lat, fwd, w, l) in spec.potholes:
        cx, cz = gx(lat), gz(fwd + l / 2)
        axes = (max(2, int(w / 2 * ppm)), max(2, int(l / 2 * ppm)))
        # broken, ragged edge: irregular polygon around the ellipse
        pts = []
        for k in range(24):
            a = 2 * math.pi * k / 24
            r = rng.uniform(0.85, 1.15)
            pts.append([int(cx + axes[0] * r * math.cos(a)), int(cz + axes[1] * r * math.sin(a))])
        base = int(rng.integers(22, 45))
        cv2.fillPoly(g, [np.array(pts)], (base, base + 2, base + 4))
        # interior: dark with coarse aggregate speckle and a lighter far rim (sun-lit broken edge)
        for _ in range(int(axes[0] * axes[1] / 6) + 3):
            a = rng.uniform(0, 2 * math.pi); r = rng.uniform(0, 0.9)
            px = int(cx + axes[0] * r * math.cos(a)); pz = int(cz + axes[1] * r * math.sin(a))
            cv2.circle(g, (px, pz), 1, (int(rng.integers(15, 90)),) * 3, -1)
        cv2.ellipse(g, (cx, cz), (axes[0], axes[1]), 0, 200, 340, (int(asphalt * 1.25),) * 3, max(1, int(ppm * 0.04)))
        gt["assets"].append({"type": "pothole", "lateral_m": lat, "forward_m": fwd, "width_m": w, "length_m": l})
    if spec.shadow:
        cv2.rectangle(g, (gx(-road_w / 2), gz(22)), (gx(road_w / 2 - 1.0), gz(14)), (int(asphalt * 0.55),) * 3, -1)
    # --- perspective projection of the ground texture: build image by inverse mapping each pixel to ground
    H, W = spec.height_px, spec.width_px
    img = np.zeros((H, W, 3), np.uint8)
    sky = (210, 170, 120) if not spec.night else (25, 15, 10)
    img[:] = sky
    hz = int(max(0, ipm.horizon_row))
    vs, us = np.mgrid[0:H, 0:W].astype(np.float32)
    xn = (us - cam.cx) / cam.fx; yn = (vs - cam.cy) / cam.fy
    c, s_ = math.cos(math.radians(cam.pitch_deg)), math.sin(math.radians(cam.pitch_deg))
    yp = yn * c + s_; zp = -yn * s_ + c
    valid = yp > 1e-4
    sc = np.where(valid, cam.height_m / np.where(valid, yp, 1), 0)
    Xg = sc * xn; Zg = sc * zp
    mapx = ((Xg - X0) * ppm).astype(np.float32); mapy = (GH - (Zg - Z0) * ppm).astype(np.float32)
    mapx[~valid] = -1; mapy[~valid] = -1
    ground = cv2.remap(g, mapx, mapy, cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=sky)
    img = np.where(valid[:, :, None], ground, img).astype(np.uint8)
    # buildings strip above horizon
    img[max(0, hz - int(0.12 * H)):hz, :] = (90, 100, 110) if not spec.night else (15, 15, 20)
    # --- vertical objects (drawn at projected position/scale)
    def draw_at(lat, fwd, base_h, top_h, fn):
        u0, v0 = ipm.ground_to_pixel(lat, fwd)
        # pixel height of a vertical span uses fy / distance (approx for small pitch)
        zc = cam.height_m * s_ + fwd * c
        ppm_v = cam.fy / zc
        fn(int(u0), int(v0), ppm_v)
    for kind, lat, fwd in spec.signs:
        def fn(u, v, k, kind=kind):
            size = int(0.75 * k)            # 750 mm plate (IRC:67 medium)
            top = int(v - 2.1 * k - size)   # bottom edge 2.1 m above ground
            cv2.line(img, (u, v), (u, top + size), (80, 80, 80), max(1, int(0.06 * k)))
            cy = top + size // 2
            if kind == "cautionary":
                pts = np.array([[u, top], [u - size // 2, top + size], [u + size // 2, top + size]])
                cv2.fillPoly(img, [pts], (0, 0, 230)); cv2.fillPoly(img, [np.array([[u, top + int(size * 0.18)], [u - int(size * 0.34), top + int(size * 0.88)], [u + int(size * 0.34), top + int(size * 0.88)]])], (245, 245, 245))
            elif kind == "mandatory":
                cv2.circle(img, (u, cy), size // 2, (0, 0, 230), -1); cv2.circle(img, (u, cy), int(size * 0.36), (245, 245, 245), -1)
                cv2.putText(img, "40", (u - int(size * 0.26), cy + int(size * 0.14)), cv2.FONT_HERSHEY_SIMPLEX, size / 90.0, (20, 20, 20), max(1, size // 30))
            elif kind == "stop":
                r = size // 2
                pts = np.array([[u + int(r * math.cos(math.radians(22.5 + 45 * i))), cy + int(r * math.sin(math.radians(22.5 + 45 * i)))] for i in range(8)])
                cv2.fillPoly(img, [pts], (0, 0, 230)); cv2.putText(img, "STOP", (u - int(size * 0.42), cy + int(size * 0.12)), cv2.FONT_HERSHEY_SIMPLEX, size / 95.0, (245, 245, 245), max(1, size // 25))
            elif kind == "informatory":
                cv2.rectangle(img, (u - size // 2, top), (u + size // 2, top + size), (220, 120, 0), -1)
        draw_at(lat, fwd, 0, 0, fn)
        gt["assets"].append({"type": f"sign_{kind}", "lateral_m": lat, "forward_m": fwd})
    if spec.signal_at:
        lat, fwd = spec.signal_at
        def fn(u, v, k):
            w = int(0.35 * k); h3 = int(1.0 * k)
            top = int(v - 3.0 * k - h3)
            cv2.line(img, (u, v), (u, top + h3), (60, 60, 60), max(2, int(0.1 * k)))
            cv2.rectangle(img, (u - w // 2, top), (u + w // 2, top + h3), (15, 15, 15), -1)
            r = max(2, int(0.12 * k))
            cv2.circle(img, (u, top + h3 // 6), r, (0, 0, 255), -1)
            cv2.circle(img, (u, top + h3 // 2), r, (40, 40, 40), -1)
            cv2.circle(img, (u, top + 5 * h3 // 6), r, (40, 40, 40), -1)
        draw_at(lat, fwd, 0, 0, fn)
        gt["assets"].append({"type": "traffic_signal", "lateral_m": lat, "forward_m": fwd})
    for lat, fwd in spec.poles:
        def fn(u, v, k):
            cv2.line(img, (u, v), (u, int(v - 8.0 * k)), (70, 70, 75), max(2, int(0.2 * k)))
            if spec.night:
                cv2.circle(img, (u + int(1.5 * k), int(v - 7.8 * k)), max(3, int(0.3 * k)), (200, 240, 255), -1)
        draw_at(lat, fwd, 0, 0, fn)
        gt["assets"].append({"type": "pole", "lateral_m": lat, "forward_m": fwd})
    if spec.night:
        img = (img.astype(np.float32) * 0.55).astype(np.uint8)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    gt["camera"] = cam.model_dump()
    gt["spec"] = asdict(spec)
    return img, gt, cam


def write_scene(spec: SceneSpec, out_dir: str, name: str) -> Tuple[str, str]:
    os.makedirs(out_dir, exist_ok=True)
    img, gt, cam = render(spec)
    ip = os.path.join(out_dir, f"{name}.jpg"); jp = os.path.join(out_dir, f"{name}.json")
    cv2.imwrite(ip, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
    with open(jp, "w") as f:
        json.dump(gt, f, indent=1)
    return ip, jp


def random_spec(seed: int) -> SceneSpec:
    r = random.Random(seed)
    n_lanes = r.choice([2, 2, 3, 4])
    lane_w = r.choice([2.75, 3.0, 3.25, 3.5, 3.5, 3.75])
    road_w = n_lanes * lane_w
    spec = SceneSpec(seed=seed, n_lanes=n_lanes, lane_width_m=lane_w, line_width_m=r.choice([0.10, 0.15]), dashed=r.random() < 0.7,
                     yellow_centre=r.random() < 0.3, pitch_deg=r.uniform(1.0, 6.0), cam_height_m=r.uniform(1.15, 1.5), noise=r.uniform(5, 12),
                     night=r.random() < 0.15, shadow=r.random() < 0.3, asphalt_gray=r.randint(80, 120))
    if r.random() < 0.5:
        spec.zebra_at_m = r.uniform(8, 18); spec.zebra_length_m = r.choice([2.0, 3.0, 4.0]); spec.zebra_stripe_m = r.choice([0.4, 0.5, 0.5, 0.6])
        if r.random() < 0.6:
            spec.stop_line_at_m = spec.zebra_at_m - r.uniform(2.0, 3.0)
    if spec.zebra_at_m is None and r.random() < 0.35:
        spec.hump_at_m = r.uniform(8, 16); spec.hump_marked = r.random() < 0.7
    for _ in range(r.choice([0, 0, 1, 1, 2, 3])):
        spec.potholes.append((r.uniform(-road_w / 2 + 0.6, road_w / 2 - 0.6), r.uniform(6, 18), r.uniform(0.3, 1.0), r.uniform(0.3, 0.9)))
    for _ in range(r.choice([0, 1, 1, 2])):
        spec.signs.append((r.choice(["cautionary", "mandatory", "stop", "informatory"]), r.choice([-1, 1]) * (road_w / 2 + r.uniform(0.6, 1.5)), r.uniform(10, 30)))
    if r.random() < 0.3:
        spec.signal_at = (road_w / 2 + r.uniform(0.5, 1.5), r.uniform(15, 30))
    for _ in range(r.choice([0, 1, 2])):
        spec.poles.append((r.choice([-1, 1]) * (road_w / 2 + r.uniform(0.8, 2.0)), r.uniform(10, 40)))
    return spec
