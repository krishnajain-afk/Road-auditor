"""Camera model + inverse perspective mapping (IPM).

Why: a phone camera gives pixels; an auditor needs metres (lane width, zebra stripe width, footpath width,
pothole size, distance of a sign ahead of a hazard). With a flat-road assumption and a known camera height
`h`, pitch `theta` and focal length `f`, every pixel below the horizon maps to a unique ground point:

    For pixel (u, v), with principal point (cx, cy):
        y_n = (v - cy) / fy ,  x_n = (u - cx) / fx          (normalised image coords)
        ray in camera frame: d = (x_n, y_n, 1)
        rotate by pitch about camera X axis: d' = R_x(theta) d
        ground intersection (camera at height h above plane y=h in camera-down convention):
            s = h / d'_y     (valid when d'_y > 0, i.e. below horizon)
            X_lat = s * d'_x ,  Z_fwd = s * d'_z

The horizon row is v_h = cy - fy * tan(theta). Everything above it has no ground intersection.

Focal length: fx = (W/2) / tan(HFOV/2). HFOV is taken from EXIF 35 mm-equivalent focal length
(HFOV = 2*atan(36/(2*f35))), a device table, or auto-estimated by vanishing point + a known lane width.
Accuracy: with calibrated pitch, lateral errors are ~2-4 % of range out to ~20 m; longitudinal errors grow
quadratically with range, so measurements are taken in the 5-20 m band ahead of the camera.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

import cv2
import numpy as np

from ..schemas import CameraModel

# 35 mm-equivalent focal lengths for common capture devices (main/wide camera, video mode crops ~10%).
DEVICE_F35 = {
    "iphone": 26.0, "pixel": 25.0, "samsung": 24.0, "oneplus": 24.0, "xiaomi": 24.0, "redmi": 25.0,
    "realme": 26.0, "vivo": 26.0, "oppo": 26.0, "nothing": 24.0, "motorola": 25.0,
    "gopro": 16.0, "dji osmo action": 15.0, "dji": 24.0, "insta360": 16.0, "ray-ban": 20.0, "meta": 20.0,
    "dashcam": 18.0,
}


def hfov_from_f35(f35: float, video_crop: float = 1.1) -> float:
    f = f35 * video_crop
    return math.degrees(2 * math.atan(36.0 / (2 * f)))


def guess_hfov(device_make: Optional[str], device_model: Optional[str], f35: Optional[float] = None,
               default_hfov: float = 70.0) -> Tuple[float, str]:
    if f35:
        return hfov_from_f35(f35, 1.0), "exif"
    key = f"{device_make or ''} {device_model or ''}".lower()
    for k, v in DEVICE_F35.items():
        if k in key:
            return hfov_from_f35(v), "device_db"
    return default_hfov, "default"


def build_camera(width: int, height: int, hfov_deg: float, height_m: float = 1.3, pitch_deg: float = 2.0,
                 source: str = "default", confidence: float = 0.5) -> CameraModel:
    fx = (width / 2) / math.tan(math.radians(hfov_deg) / 2)
    fy = fx
    return CameraModel(width_px=width, height_px=height, fx=fx, fy=fy, cx=width / 2, cy=height / 2,
                       height_m=height_m, pitch_deg=pitch_deg, hfov_deg=hfov_deg, source=source,
                       confidence=confidence)


class IPM:
    """Pixel <-> ground-plane mapping for a CameraModel (flat road assumption)."""

    def __init__(self, cam: CameraModel):
        self.cam = cam
        th = math.radians(cam.pitch_deg)
        self._c, self._s = math.cos(th), math.sin(th)

    @property
    def horizon_row(self) -> float:
        return self.cam.cy - self.cam.fy * math.tan(math.radians(self.cam.pitch_deg))

    def pixel_to_ground(self, u: float, v: float) -> Optional[Tuple[float, float]]:
        """Returns (lateral_m right+, forward_m) or None if above horizon."""
        xn = (u - self.cam.cx) / self.cam.fx
        yn = (v - self.cam.cy) / self.cam.fy
        # camera frame: x right, y down, z forward. Pitch down by theta rotates ray: y' = y cos + z sin, z' = -y sin + z cos
        # With pitch defined +ve looking DOWN, a ray at image centre (y=0,z=1) should hit ground ahead:
        yp = yn * self._c + 1.0 * self._s
        zp = -yn * self._s + 1.0 * self._c
        if yp <= 1e-6:
            return None
        s = self.cam.height_m / yp
        return (s * xn, s * zp)

    def ground_to_pixel(self, x: float, z: float) -> Tuple[float, float]:
        y = self.cam.height_m
        # inverse rotation (pitch up by theta): y_c = y cos - z sin ; z_c = y sin + z cos
        yc = y * self._c - z * self._s
        zc = y * self._s + z * self._c
        u = self.cam.cx + self.cam.fx * x / zc
        v = self.cam.cy + self.cam.fy * yc / zc
        return (u, v)

    def height_above_ground(self, v: float, forward_m: float) -> float:
        """Height (m) above the road plane of a point seen at image row v and known forward range."""
        a = (v - self.cam.cy) / self.cam.fy
        den = a * self._s - self._c
        if abs(den) < 1e-9:
            return 0.0
        return self.cam.height_m + forward_m * (self._s + a * self._c) / den

    def range_from_width(self, px_w: float, true_w_m: float) -> float:
        """Forward range of an object of known physical width from its pixel width."""
        return self.cam.fx * true_w_m / max(1.0, px_w)

    def pixel_width_to_m(self, u1: float, u2: float, v: float) -> Optional[float]:
        a, b = self.pixel_to_ground(u1, v), self.pixel_to_ground(u2, v)
        if a is None or b is None:
            return None
        return abs(b[0] - a[0])

    def bbox_ground_size(self, x1, y1, x2, y2) -> Optional[Tuple[float, float, float, float]]:
        """For an object lying on the road (pothole, marking): width, length, lateral offset, forward distance."""
        bl, br = self.pixel_to_ground(x1, y2), self.pixel_to_ground(x2, y2)
        tl = self.pixel_to_ground((x1 + x2) / 2, y1)
        if bl is None or br is None:
            return None
        w = abs(br[0] - bl[0])
        fwd = (bl[1] + br[1]) / 2
        length = (tl[1] - fwd) if tl is not None else w
        lat = (bl[0] + br[0]) / 2
        return (w, max(0.0, length), lat, fwd)

    def birdseye(self, img: np.ndarray, x_range=(-8.0, 8.0), z_range=(3.0, 30.0), px_per_m: float = 20.0):
        """Warp image to a top-down metric grid. Returns (bev, meta)."""
        W = int((x_range[1] - x_range[0]) * px_per_m)
        H = int((z_range[1] - z_range[0]) * px_per_m)
        src = []
        dst = []
        for x, z in ((x_range[0], z_range[0]), (x_range[1], z_range[0]), (x_range[1], z_range[1]), (x_range[0], z_range[1])):
            u, v = self.ground_to_pixel(x, z)
            src.append((u, v))
            dst.append(((x - x_range[0]) * px_per_m, H - (z - z_range[0]) * px_per_m))
        M = cv2.getPerspectiveTransform(np.float32(src), np.float32(dst))
        bev = cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_LINEAR)
        return bev, {"M": M, "x_range": x_range, "z_range": z_range, "px_per_m": px_per_m, "W": W, "H": H}

    @staticmethod
    def bev_to_ground(px: float, py: float, meta) -> Tuple[float, float]:
        x = meta["x_range"][0] + px / meta["px_per_m"]
        z = meta["z_range"][0] + (meta["H"] - py) / meta["px_per_m"]
        return x, z


# ------------------------------------------------------------------ auto-calibration
def estimate_vanishing_point(gray: np.ndarray) -> Optional[Tuple[float, float, float]]:
    """Vanishing point of road-parallel lines via Hough segments + cross-family intersection voting.

    Segments are split into two families by direction (bottom-left -> VP vs bottom-right -> VP). Only cross-family
    pairs are intersected, which removes the noisy near-parallel same-side intersections that otherwise dominate the vote.
    A VP is accepted only inside a plausible window (central 70 % horizontally, 15-75 % vertically).
    Returns (u, v, confidence) or None.
    """
    h, w = gray.shape[:2]
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 140)
    # add bright-marking edges (lane lines) which are weak in plain Canny on low-contrast asphalt
    _, bright = cv2.threshold(blur, int(min(250, blur.mean() + 1.5 * blur.std())), 255, cv2.THRESH_BINARY)
    edges = cv2.bitwise_or(edges, cv2.Canny(bright, 50, 150))
    edges[: int(h * 0.15), :] = 0
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=max(20, w // 16), maxLineGap=25)
    if lines is None or len(lines) < 4:
        return None
    left, right = [], []
    for x1, y1, x2, y2 in np.asarray(lines, dtype=np.float64).reshape(-1, 4):
        if y1 < y2:  # orient bottom -> top
            x1, y1, x2, y2 = x2, y2, x1, y1
        dx, dy = x2 - x1, y2 - y1
        ang = abs(math.degrees(math.atan2(-dy, abs(dx))))   # 0 = horizontal, 90 = vertical
        if not (12 < ang < 80):
            continue
        seg = (float(x1), float(y1), float(x2), float(y2), math.hypot(dx, dy))
        (left if dx > 0 else right).append(seg)
    if len(left) < 2 or len(right) < 2:
        return None
    rng = np.random.default_rng(0)
    pts = []
    n_pairs = min(4000, len(left) * len(right))
    for _ in range(n_pairs):
        a_ = left[rng.integers(0, len(left))]; b_ = right[rng.integers(0, len(right))]
        p_ = _intersect(a_, b_)
        if p_ is None:
            continue
        u, v = p_
        if 0.15 * w < u < 0.85 * w and 0.15 * h < v < 0.75 * h:
            pts.append((u, v, a_[4] * b_[4]))
    if len(pts) < 8:
        return None
    arr = np.array(pts)
    hb, xe, ye = np.histogram2d(arr[:, 0], arr[:, 1], bins=(40, 30), range=[[0.15 * w, 0.85 * w], [0.15 * h, 0.75 * h]], weights=arr[:, 2])
    k = np.unravel_index(np.argmax(hb), hb.shape)
    u = (xe[k[0]] + xe[k[0] + 1]) / 2
    v = (ye[k[1]] + ye[k[1] + 1]) / 2
    conf = float(hb.max() / (hb.sum() + 1e-9))
    near = arr[(np.abs(arr[:, 0] - u) < w * 0.04) & (np.abs(arr[:, 1] - v) < h * 0.04)]
    if len(near) >= 5:
        u = float(np.average(near[:, 0], weights=near[:, 2]))
        v = float(np.average(near[:, 1], weights=near[:, 2]))
    return (u, v, min(1.0, conf * 4))


def _intersect(a, b):
    x1, y1, x2, y2, _ = a
    x3, y3, x4, y4, _ = b
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-6:
        return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
    return px, py


def calibrate_pitch_from_frames(frames_gray: Sequence[np.ndarray], cam: CameraModel) -> CameraModel:
    """Median vanishing point over many frames -> pitch (and small yaw)."""
    vps = []
    for g in frames_gray:
        r = estimate_vanishing_point(g)
        if r and r[2] > 0.05:
            vps.append(r)
    if not vps or (len(vps) < 3 and len(frames_gray) >= 3):
        return cam
    arr = np.array(vps)
    u, v = float(np.median(arr[:, 0])), float(np.median(arr[:, 1]))
    pitch = math.degrees(math.atan2(cam.cy - v, cam.fy))
    yaw = math.degrees(math.atan2(u - cam.cx, cam.fx))
    # sanity: hand-held/dash phones sit within -5..+15 deg pitch
    if -6 <= pitch <= 18:
        return cam.model_copy(update={"pitch_deg": pitch, "yaw_deg": yaw, "source": cam.source + "+vp",
                                      "confidence": min(0.9, cam.confidence + 0.3)})
    return cam


def scale_from_known_width(ipm: IPM, u1: float, u2: float, v: float, known_m: float) -> Optional[float]:
    """Returns a corrected camera height so that pixel span (u1..u2 at row v) equals known_m."""
    w = ipm.pixel_width_to_m(u1, u2, v)
    if not w or w <= 0:
        return None
    return ipm.cam.height_m * known_m / w
