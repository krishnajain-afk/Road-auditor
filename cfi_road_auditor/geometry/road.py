"""Road geometry analytics from the GPS track and IRC design relationships.

* Horizontal curve radius: algebraic circle fit (Kasa) over a sliding window of projected (x,y) points.
* Gradient: smoothed dz/ds from altitude (phone barometric/GNSS altitude is noisy; we use a 50 m window
  and report uncertainty).
* Stopping sight distance per IRC:66 / IRC:73:  SSD = 0.278 V t + V^2 / (254 (f +/- g)) with t = 2.5 s
  and f per IRC table (0.40 at 20-30 km/h down to 0.35 at >= 80 km/h).
* Design speed defaults per IRC:86 (urban) and IRC:73 (rural) by road class and terrain.
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..schemas import GeoPoint, RoadClass, Terrain

# IRC:73-1980 Table 2 ruling design speeds (km/h) by terrain, IRC:86-2018 for urban roads.
DESIGN_SPEED: Dict[RoadClass, Dict[Terrain, float]] = {
    RoadClass.EXPRESSWAY: {Terrain.PLAIN: 120, Terrain.ROLLING: 100, Terrain.MOUNTAINOUS: 80, Terrain.STEEP: 80},
    RoadClass.NATIONAL_HIGHWAY: {Terrain.PLAIN: 100, Terrain.ROLLING: 80, Terrain.MOUNTAINOUS: 50, Terrain.STEEP: 40},
    RoadClass.STATE_HIGHWAY: {Terrain.PLAIN: 100, Terrain.ROLLING: 80, Terrain.MOUNTAINOUS: 50, Terrain.STEEP: 40},
    RoadClass.MAJOR_DISTRICT_ROAD: {Terrain.PLAIN: 80, Terrain.ROLLING: 65, Terrain.MOUNTAINOUS: 40, Terrain.STEEP: 30},
    RoadClass.OTHER_DISTRICT_ROAD: {Terrain.PLAIN: 65, Terrain.ROLLING: 50, Terrain.MOUNTAINOUS: 30, Terrain.STEEP: 25},
    RoadClass.VILLAGE_ROAD: {Terrain.PLAIN: 50, Terrain.ROLLING: 40, Terrain.MOUNTAINOUS: 25, Terrain.STEEP: 25},
    RoadClass.URBAN_ARTERIAL: {t: 80 for t in Terrain},
    RoadClass.URBAN_SUB_ARTERIAL: {t: 60 for t in Terrain},
    RoadClass.URBAN_COLLECTOR: {t: 50 for t in Terrain},
    RoadClass.URBAN_LOCAL: {t: 30 for t in Terrain},
}

# IRC:66 / IRC:73 longitudinal friction coefficients for SSD
_F_TABLE = [(30, 0.40), (40, 0.38), (50, 0.37), (65, 0.36), (80, 0.35), (100, 0.35), (120, 0.35)]
# IRC:38 / IRC:73 minimum radius (m) for ruling design speed, plain/rolling e=0.07, f=0.15
_MIN_RADIUS = {20: 15, 25: 20, 30: 30, 35: 45, 40: 60, 50: 90, 60: 130, 65: 155, 80: 230, 100: 360, 120: 520}


def design_speed_for(rc: RoadClass, terrain: Terrain = Terrain.PLAIN) -> float:
    return DESIGN_SPEED[rc][terrain]


def friction_for(v_kmph: float) -> float:
    for v, f in _F_TABLE:
        if v_kmph <= v:
            return f
    return 0.35


def stopping_sight_distance(v_kmph: float, grade_pct: float = 0.0, t_react: float = 2.5) -> float:
    f = friction_for(v_kmph)
    g = grade_pct / 100.0
    return 0.278 * v_kmph * t_react + (v_kmph ** 2) / (254.0 * max(0.05, f + g))


def min_curve_radius(v_kmph: float, e_max: float = 0.07, f: float = 0.15) -> float:
    """R_min = V^2 / (127 (e + f)); IRC:38 uses e_max 0.07 rural, 0.04 urban/snow-bound, f 0.15."""
    return (v_kmph ** 2) / (127.0 * (e_max + f))


def irc_min_radius_table(v_kmph: float) -> float:
    keys = sorted(_MIN_RADIUS)
    for k in keys:
        if v_kmph <= k:
            return _MIN_RADIUS[k]
    return _MIN_RADIUS[keys[-1]]


# ------------------------------------------------------------------ projections
def project_track(track: Sequence[GeoPoint]) -> np.ndarray:
    """Local equirectangular projection (metres) - adequate over a few km."""
    if not track:
        return np.zeros((0, 2))
    lat0 = math.radians(track[0].lat)
    R = 6371008.8
    xy = np.array([[(math.radians(p.lon) - math.radians(track[0].lon)) * R * math.cos(lat0),
                    (math.radians(p.lat) - math.radians(track[0].lat)) * R] for p in track])
    return xy


def fit_circle(xy: np.ndarray) -> Tuple[float, float, float]:
    """Kasa algebraic circle fit. Returns (xc, yc, r)."""
    x, y = xy[:, 0], xy[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    b = x ** 2 + y ** 2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    xc, yc, c = sol
    r = math.sqrt(max(1e-9, c + xc ** 2 + yc ** 2))
    return float(xc), float(yc), float(r)


def resample_track(xy: np.ndarray, step_m: float = 5.0) -> Tuple[np.ndarray, np.ndarray]:
    seg = np.r_[0, np.cumsum(np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1])))]
    if seg[-1] < step_m * 3:
        return xy, seg
    s = np.arange(0, seg[-1], step_m)
    return np.c_[np.interp(s, seg, xy[:, 0]), np.interp(s, seg, xy[:, 1])], s


def curve_radius_from_track(track: Sequence[GeoPoint], window_m: float = 60.0, step_m: float = 5.0,
                            max_radius: float = 5000.0, min_heading_change_deg: float = 6.0) -> List[Tuple[float, float, float]]:
    """Returns [(chainage_m, radius_m, confidence)] per resampled point. Straight -> radius = max_radius."""
    xy = project_track(track)
    if len(xy) < 5:
        return []
    rs, s = resample_track(xy, step_m)
    n_half = max(2, int(window_m / step_m / 2))
    out = []
    for i in range(len(rs)):
        a, b = max(0, i - n_half), min(len(rs), i + n_half + 1)
        if b - a < 5 or i < n_half or i >= len(rs) - n_half:   # incomplete windows at the track ends are unreliable
            out.append((float(s[i]), max_radius, 0.2))
            continue
        w = rs[a:b]
        try:
            # significance: net heading change across the window must exceed what residual GNSS noise can fake
            h0 = math.atan2(w[2, 1] - w[0, 1], w[2, 0] - w[0, 0]); h1 = math.atan2(w[-1, 1] - w[-3, 1], w[-1, 0] - w[-3, 0])
            dth = abs((h1 - h0 + math.pi) % (2 * math.pi) - math.pi)
            if dth < math.radians(min_heading_change_deg):
                out.append((float(s[i]), max_radius, 0.6))
                continue
            xc, yc, r = fit_circle(w)
            resid = np.abs(np.hypot(w[:, 0] - xc, w[:, 1] - yc) - r)
            conf = float(max(0.1, 1.0 - resid.mean() / 2.0))
            r = min(r, max_radius)
        except Exception:
            r, conf = max_radius, 0.1
        out.append((float(s[i]), float(r), conf))
    return out


def gradient_from_track(track: Sequence[GeoPoint], window_m: float = 50.0) -> List[Tuple[float, float, float]]:
    """[(chainage, gradient_pct, confidence)] from altitude; confidence is low (phone altitude noisy)."""
    pts = [p for p in track if p.alt_m is not None]
    if len(pts) < 5:
        return []
    xy = project_track(pts)
    s = np.r_[0, np.cumsum(np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1])))]
    z = np.array([p.alt_m for p in pts])
    out = []
    for i in range(len(s)):
        m = (s >= s[i] - window_m / 2) & (s <= s[i] + window_m / 2)
        if m.sum() < 3 or (s[m].max() - s[m].min()) < window_m * 0.5:
            continue
        k = np.polyfit(s[m], z[m], 1)[0]
        out.append((float(s[i]), float(100 * k), 0.35))
    return out


def heading_change_hotspots(track: Sequence[GeoPoint], thresh_deg: float = 25.0, window_m: float = 30.0):
    """Sharp heading changes -> candidate junction / sharp curve locations."""
    xy = project_track(track)
    if len(xy) < 5:
        return []
    rs, s = resample_track(xy, 5.0)
    hd = np.degrees(np.arctan2(np.diff(rs[:, 1]), np.diff(rs[:, 0])))
    n = max(1, int(window_m / 5))
    out = []
    for i in range(n, len(hd) - n):
        d = (hd[i + n] - hd[i - n] + 180) % 360 - 180
        if abs(d) >= thresh_deg:
            out.append((float(s[i]), float(d)))
    # merge neighbours
    merged = []
    for ch, d in out:
        if merged and ch - merged[-1][0] < window_m:
            if abs(d) > abs(merged[-1][1]):
                merged[-1] = (ch, d)
        else:
            merged.append((ch, d))
    return merged


def speed_profile(track: Sequence[GeoPoint]) -> List[Tuple[float, float]]:
    xy = project_track(track)
    s = np.r_[0, np.cumsum(np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1])))] if len(xy) > 1 else np.zeros(len(xy))
    return [(float(s[i]), float((p.speed_mps or 0) * 3.6)) for i, p in enumerate(track)]
