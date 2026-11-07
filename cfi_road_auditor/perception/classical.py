"""Classical computer-vision detectors (no learned weights required).

These are the always-available Tier-A backends. Each is designed around the geometry defined by Indian
standards so that a positive detection also yields a *measurement* the rule engine can compare against
the code (e.g. zebra stripe width 500 mm per IRC:35, hump marking pattern per IRC:99).

All road-plane detectors operate in a bird's-eye-view (BEV) produced by geometry.camera.IPM so that
distances are metric. Sign/signal detectors operate in the perspective image above the horizon.
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from ..geometry.camera import IPM
from ..schemas import AssetType, BBox, CameraModel, Detection, FrameRef, Source
from . import colors as C
from .base import Detector


def _det(asset, label, conf, bbox, frame, attrs=None, polygon=None) -> Detection:
    return Detection(asset=asset, label=label, confidence=float(conf), bbox=bbox, polygon=polygon,
                     frame_index=frame.index, frame_t=frame.t, source=Source.CLASSICAL, attributes=attrs or {})


# ----------------------------------------------------------------------------- road surface
def drivable_mask(img: np.ndarray, ipm: IPM) -> np.ndarray:
    """Rough road-surface mask by seeded colour similarity from the lower-centre of the frame."""
    h, w = img.shape[:2]
    lab = cv2.cvtColor(cv2.GaussianBlur(img, (7, 7), 0), cv2.COLOR_BGR2LAB)
    y0, y1 = int(h * 0.80), int(h * 0.97)
    x0, x1 = int(w * 0.40), int(w * 0.60)
    seed = lab[y0:y1, x0:x1].reshape(-1, 3)
    mu, sd = seed.mean(0), seed.std(0) + 4
    d = np.abs(lab.astype(np.float32) - mu) / sd
    m = (d.max(axis=2) < 3.2).astype(np.uint8) * 255
    # road markings sit on the road: add white/yellow paint so a lane line does not split the surface
    paint = cv2.bitwise_or(C.white_mask(img), C.yellow_mask(img))
    m = cv2.bitwise_or(m, paint)
    hz = int(max(0, min(h - 1, ipm.horizon_row)))
    m[:hz, :] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    # keep the component connected to the seed
    n, lab_cc = cv2.connectedComponents(m)
    seed_lbl = lab_cc[(y0 + y1) // 2, (x0 + x1) // 2]
    if seed_lbl == 0:
        return m
    return (lab_cc == seed_lbl).astype(np.uint8) * 255


def carriageway_width_from_mask(mask: np.ndarray, ipm: IPM, z_probe=(6.0, 8.0, 10.0, 12.0, 15.0)) -> Optional[Tuple[float, float]]:
    """Width (m) of the drivable mask at several forward distances; returns (median width, confidence)."""
    h, w = mask.shape[:2]
    vals = []
    for z in z_probe:
        u, v = ipm.ground_to_pixel(0.0, z)
        vi = int(round(v))
        if not (0 <= vi < h):
            continue
        row = mask[vi]
        xs = np.where(row > 0)[0]
        if len(xs) < 10:
            continue
        # take the contiguous run containing the centre (or nearest)
        uc = int(round(u))
        runs = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1)
        run = min(runs, key=lambda r: abs(r.mean() - uc))
        wm = ipm.pixel_width_to_m(float(run[0]), float(run[-1]), float(vi))
        if wm:
            # if the run touches image borders the width is truncated -> unreliable
            if run[0] <= 2 or run[-1] >= w - 3:
                continue
            vals.append(wm)
    if len(vals) < 2:
        return None
    med = float(np.median(vals))
    spread = float(np.std(vals)) / (med + 1e-6)
    return med, float(max(0.2, 0.8 - spread))


# ----------------------------------------------------------------------------- markings in BEV
def _runs(binary_1d: np.ndarray) -> List[Tuple[int, int]]:
    """Start/end indices of True runs."""
    idx = np.where(binary_1d)[0]
    if len(idx) == 0:
        return []
    cuts = np.where(np.diff(idx) > 1)[0] + 1
    return [(int(r[0]), int(r[-1])) for r in np.split(idx, cuts)]


def detect_zebra(bev: np.ndarray, meta: Dict, frame: FrameRef, ipm: IPM) -> List[Detection]:
    """Zebra crossing: transverse band of longitudinal white stripes, period ~1.0 m (0.5 m stripe + 0.5 m gap)."""
    ppm = meta["px_per_m"]
    wm = C.white_mask(bev)
    H, W = wm.shape
    out: List[Detection] = []
    band_h = int(0.5 * ppm)  # analyse 0.5 m longitudinal slices
    rows_hit = []
    for y in range(0, H - band_h, band_h // 2):
        sl = wm[y:y + band_h].mean(axis=0) > 127  # lateral profile
        runs = _runs(sl)
        stripes = [(a, b) for a, b in runs if 0.25 * ppm <= (b - a + 1) <= 0.9 * ppm]
        if len(stripes) < 3:
            continue
        centres = np.array([(a + b) / 2 for a, b in stripes])
        gaps = np.diff(centres) / ppm
        ok = (gaps > 0.6) & (gaps < 1.5)
        # longest consecutive run of regular gaps
        best = 0; cur = 0
        for o in ok:
            cur = cur + 1 if o else 0
            best = max(best, cur)
        if best >= 2:  # >= 3 regularly spaced stripes
            rows_hit.append((y, stripes, float(np.median(gaps[ok])) if ok.any() else 1.0,
                             float(np.median([(b - a + 1) / ppm for a, b in stripes]))))
    if not rows_hit:
        return out
    # group consecutive slices into one crossing
    groups: List[List] = []
    for r in rows_hit:
        if groups and r[0] - groups[-1][-1][0] <= band_h:
            groups[-1].append(r)
        else:
            groups.append([r])
    for g in groups:
        y0 = g[0][0]; y1 = g[-1][0] + band_h
        length_m = (y1 - y0) / ppm
        if length_m < 1.2:  # stop lines / transverse bars are shorter than crossing width (min 2 m)
            continue
        xs = [s for r in g for s in r[1]]
        x0 = min(a for a, b in xs); x1 = max(b for a, b in xs)
        stripe_w = float(np.median([r[3] for r in g]))
        period = float(np.median([r[2] for r in g]))
        n_stripes = int(np.median([len(r[1]) for r in g]))
        lat0, z0 = IPM.bev_to_ground(x0, y1, meta)
        lat1, z1 = IPM.bev_to_ground(x1, y0, meta)
        # project back to image bbox
        u1, v1 = ipm.ground_to_pixel(lat0, z0); u2, v2 = ipm.ground_to_pixel(lat1, z1)
        u3, v3 = ipm.ground_to_pixel(lat0, z1); u4, v4 = ipm.ground_to_pixel(lat1, z0)
        bb = BBox(x1=min(u1, u3), y1=min(v1, v2, v3, v4), x2=max(u2, u4), y2=max(v1, v2, v3, v4))
        regularity = 1.0 - min(1.0, abs(period - 1.0))
        conf = float(min(0.95, 0.45 + 0.1 * min(n_stripes, 4) + 0.2 * regularity))
        out.append(_det(AssetType.ZEBRA_CROSSING, "zebra_crossing", conf, bb, frame, {
            "stripe_width_m": round(stripe_w, 2), "stripe_period_m": round(period, 2),
            "crossing_length_m": round(length_m, 2), "lateral_extent_m": round(abs(lat1 - lat0), 2),
            "n_stripes": n_stripes, "forward_m": round(z0, 1)}))
    return out


def detect_lane_lines(bev: np.ndarray, meta: Dict, frame: FrameRef, ipm: IPM,
                      exclude_rows: Optional[List[Tuple[int, int]]] = None) -> Tuple[List[Detection], Dict]:
    """Longitudinal lane / edge lines in BEV.

    Returns detections + {'lane_widths_m': [...], 'line_widths_m': [...], 'n_lines': n}.
    `exclude_rows` are BEV row bands occupied by transverse markings (zebra, stop line, hump) which would otherwise
    masquerade as short longitudinal lines. Line width is the median per-row run length (robust to blur).
    """
    ppm = meta["px_per_m"]
    wm = cv2.bitwise_or(C.white_mask(bev), C.yellow_mask(bev))
    H, W = wm.shape
    valid_rows = np.ones(H, bool)
    for a, b in exclude_rows or []:
        valid_rows[max(0, a):min(H, b)] = False
    if valid_rows.sum() < 0.3 * H:
        valid_rows[:] = True
    wmv = wm[valid_rows]
    col = (wmv > 0).mean(axis=0)
    thr = 0.12                            # dashed lines cover ~1/3 (1.5 m line / 4.5 m gap => 0.25..0.33)
    cand = col > thr
    runs = _runs(cand)
    lines = []
    ymask_full = C.yellow_mask(bev)
    for a, b in runs:
        wpx = b - a + 1
        if not (0.03 * ppm <= wpx <= 0.6 * ppm):   # 30 mm .. 600 mm wide columns (kerb paint up to 300)
            continue
        band = wmv[:, max(0, a - 2):min(W, b + 3)] > 0
        rows_with = band.any(axis=1)
        cov = float(rows_with.mean())
        # per-row run width (median) -> marking width
        widths = []
        for r in np.where(rows_with)[0][::2]:
            rr = _runs(band[r])
            if rr:
                widths.append(max(e - s_ + 1 for s_, e in rr))
        w_m = float(np.median(widths)) / ppm if widths else wpx / ppm
        if w_m > 0.45:
            continue
        ymask = ymask_full[:, a:b + 1].mean() > 40
        dashed = cov < 0.6
        # weighted centre
        xs = np.arange(max(0, a - 2), min(W, b + 3))
        wsum = band.sum(axis=0).astype(float)
        xc = float((xs * wsum).sum() / (wsum.sum() + 1e-6)) if wsum.sum() else (a + b) / 2
        lines.append({"x": xc, "w_m": w_m, "coverage": cov, "yellow": bool(ymask), "dashed": dashed})
    lines.sort(key=lambda d: d["x"])
    # merge lines closer than 0.35 m (double edge of one marking)
    merged = []
    for ln in lines:
        if merged and (ln["x"] - merged[-1]["x"]) / ppm < 0.35:
            if ln["coverage"] > merged[-1]["coverage"]:
                merged[-1] = ln
        else:
            merged.append(ln)
    lines = merged
    dets = []
    widths = []
    for i, ln in enumerate(lines):
        lat, _ = IPM.bev_to_ground(ln["x"], H / 2, meta)
        asset = AssetType.CENTRE_LINE if ln["yellow"] else AssetType.LANE_LINE
        u1, v1 = ipm.ground_to_pixel(lat - 0.1, meta["z_range"][0]); u2, v2 = ipm.ground_to_pixel(lat + 0.1, meta["z_range"][1])
        bb = BBox(x1=min(u1, u2), y1=min(v1, v2), x2=max(u1, u2), y2=max(v1, v2))
        dets.append(_det(asset, "lane_line", min(0.9, 0.4 + ln["coverage"]), bb, frame, {
            "line_width_m": round(ln["w_m"], 3), "dashed": ln["dashed"], "yellow": ln["yellow"],
            "lateral_m": round(lat, 2), "coverage": round(ln["coverage"], 2)}))
        if i > 0:
            gap = (ln["x"] - lines[i - 1]["x"]) / ppm
            # IRC:35 edge lines sit ~150 mm inside the carriageway edge: the outer lanes extend to the kerb/edge
            if i == 1 and not lines[0]["dashed"] and len(lines) >= 3:
                gap += 0.15
            if i == len(lines) - 1 and not ln["dashed"] and len(lines) >= 3:
                gap += 0.15
            if 2.0 <= gap <= 4.6:
                widths.append(round(gap, 2))
    return dets, {"lane_widths_m": widths, "line_widths_m": [round(l["w_m"], 3) for l in lines], "n_lines": len(lines)}


def detect_stop_line(bev: np.ndarray, meta: Dict, frame: FrameRef, ipm: IPM) -> List[Detection]:
    """Transverse solid white bar 0.2-0.6 m thick spanning >= 2.5 m laterally."""
    ppm = meta["px_per_m"]
    wm = C.white_mask(bev)
    H, W = wm.shape
    row = (wm > 0).mean(axis=1)
    runs = _runs(row > 0.35)
    out = []
    for a, b in runs:
        th = (b - a + 1) / ppm
        if 0.15 <= th <= 0.7:
            seg = wm[a:b + 1].mean(axis=0) > 127
            r = _runs(seg)
            if not r:
                continue
            longest = max(r, key=lambda t: t[1] - t[0])
            span = (longest[1] - longest[0] + 1) / ppm
            if span >= 2.5:
                lat0, z0 = IPM.bev_to_ground(longest[0], b, meta); lat1, z1 = IPM.bev_to_ground(longest[1], a, meta)
                u1, v1 = ipm.ground_to_pixel(lat0, z0); u2, v2 = ipm.ground_to_pixel(lat1, z1)
                bb = BBox(x1=min(u1, u2), y1=min(v1, v2), x2=max(u1, u2), y2=max(v1, v2))
                out.append(_det(AssetType.STOP_LINE, "stop_line", 0.6, bb, frame,
                                {"thickness_m": round(th, 2), "span_m": round(span, 2), "forward_m": round(z0, 1)}))
    return out


def detect_speed_hump_markings(bev: np.ndarray, meta: Dict, frame: FrameRef, ipm: IPM,
                               zebra: Optional[List[Detection]] = None) -> List[Detection]:
    """Speed hump / rumble strip: transverse band with alternating yellow(white)/black chevrons (IRC:99).

    Zebra stripes (white, 1.0 m lateral period) look similar; humps are distinguished by the painted *black* gaps
    (much darker than the asphalt) and by not overlapping a detected zebra crossing."""
    ppm = meta["px_per_m"]
    ym = C.yellow_mask(bev); wm = C.white_mask(bev)
    H, W = ym.shape
    hsv_v = C.hsv(bev)[:, :, 2]
    road_v = float(np.median(hsv_v[:, int(W * 0.35):int(W * 0.65)]))
    zebra_rows = []
    for z in zebra or []:
        z0 = z.attributes.get("forward_m"); L = z.attributes.get("crossing_length_m", 3.0)
        if z0 is not None:
            zebra_rows.append((z0 - 1.0, z0 + L + 1.0))
    out = []
    for name, m in (("yellow", ym), ("white", wm)):
        row = (m > 0).mean(axis=1)
        runs = _runs(row > 0.12)
        for a, b in runs:
            th = (b - a + 1) / ppm
            if not (0.5 <= th <= 4.5):
                continue
            prof = m[a:b + 1].mean(axis=0) > 100
            r = _runs(prof)
            bars = [(s, e) for s, e in r if 0.15 * ppm <= (e - s + 1) <= 1.2 * ppm]
            if len(bars) < 4:
                continue
            centres = np.diff([(s + e) / 2 for s, e in bars]) / ppm
            if centres.size and np.std(centres) / (np.mean(centres) + 1e-6) < 0.45 and 0.3 <= np.median(centres) <= 1.6:
                # gaps between bars must be painted black (darker than asphalt), else it is a zebra / lane pattern
                gap_vals = [float(np.median(hsv_v[a:b + 1, e + 1:s2])) for (s1_, e), (s2, _) in zip(bars, bars[1:]) if s2 > e + 1]
                if not gap_vals or np.median(gap_vals) > road_v - 20:
                    continue
                lat0, z0 = IPM.bev_to_ground(bars[0][0], b, meta); lat1, z1 = IPM.bev_to_ground(bars[-1][1], a, meta)
                if any(lo <= z0 <= hi or lo <= z1 <= hi for lo, hi in zebra_rows):
                    continue
                u1, v1 = ipm.ground_to_pixel(lat0, z0); u2, v2 = ipm.ground_to_pixel(lat1, z1)
                bb = BBox(x1=min(u1, u2), y1=min(v1, v2), x2=max(u1, u2), y2=max(v1, v2))
                conf = 0.55 if name == "yellow" else 0.45
                asset = AssetType.SPEED_HUMP if th >= 1.0 else AssetType.RUMBLE_STRIP
                out.append(_det(asset, f"hump_marking_{name}", conf, bb, frame, {
                    "band_length_m": round(th, 2), "n_bars": len(bars), "forward_m": round(z0, 1), "marked": True}))
    return out


# ----------------------------------------------------------------------------- pavement defects
def detect_potholes_classical(img: np.ndarray, road_mask: np.ndarray, frame: FrameRef, ipm: IPM,
                              exclude_fwd: Optional[List[Tuple[float, float]]] = None,
                              half_width_m: Optional[float] = None) -> List[Detection]:
    """Dark, rough, compact blobs inside the road mask (fallback when no learned damage model is loaded).

    Candidate = darker than the *local* road surface (adaptive) AND rough (gradient energy well above asphalt) AND
    plausible metric size via IPM (0.15-3 m). Shadows are smooth (fail texture), wet patches are smooth, manholes are
    round + smooth, tar patches are smooth -> rejected. Precision is moderate; detections are flagged low-confidence.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    road = road_mask > 0
    if road.sum() < 0.02 * h * w:
        return []
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    road_med = int(np.median(blur[road]))
    paint = cv2.bitwise_or(C.white_mask(img), C.yellow_mask(img)) > 0
    filled = blur.copy(); filled[~road | paint] = road_med   # mask-aware local reference: kerbs, footpath and paint must not bias it
    local = cv2.medianBlur(filled, 31)
    rel = local.astype(np.int16) - blur.astype(np.int16)
    inner = cv2.erode(road_mask, np.ones((9, 9), np.uint8)) > 0   # stay clear of the road edge / kerb shadow
    dark = ((rel > 22) & inner).astype(np.uint8) * 255
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0); gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1)
    energy = cv2.blur(np.hypot(gx, gy), (7, 7))
    e_med = float(np.median(energy[road])) + 1e-6
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cnts, _ = cv2.findContours(dark, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 40:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        if bw > 0.5 * w or bh > 0.4 * h:
            continue
        if x <= 2 or y <= 2 or x + bw >= w - 3 or y + bh >= h - 3:   # truncated by the frame border: not measurable
            continue
        solidity = area / (cv2.contourArea(cv2.convexHull(c)) + 1e-6)
        if solidity < 0.5:
            continue
        gs = ipm.bbox_ground_size(x, y, x + bw, y + bh)
        if not gs:
            continue
        gw, gl, lat, fwd = gs
        if not (0.15 <= gw <= 3.0 and 0.1 <= gl <= 4.0 and 3.0 <= fwd <= 30.0):
            continue
        if not (0.2 <= gw / (gl + 1e-6) <= 5.0):     # metric aspect (perspective squashes far objects in pixels)
            continue
        if any(lo <= fwd <= hi for lo, hi in exclude_fwd or []):   # inside a zebra / hump / stop-line band
            continue
        if half_width_m and abs(lat) > half_width_m - 0.35:         # kerb shadow / edge drop, not a pothole
            continue
        e = float(energy[y:y + bh, x:x + bw].mean() / e_med)
        if e < 1.4:
            continue
        # island test: a pothole is surrounded by normal surface on (almost) all sides; a shadow edge is not
        mx, my = max(3, bw // 2), max(3, bh // 2)
        strips = [rel[max(0, y - my):y, x:x + bw], rel[y + bh:min(h, y + bh + my), x:x + bw],
                  rel[y:y + bh, max(0, x - mx):x], rel[y:y + bh, x + bw:min(w, x + bw + mx)]]
        if any(st.size == 0 for st in strips):
            continue
        normal = sum(1 for st in strips if float(np.median(st)) < 10)
        if normal < 3:
            continue
        inside = gray[y:y + bh, x:x + bw][dark[y:y + bh, x:x + bw] > 0]
        if inside.size and float(inside.std()) < 6:                   # uniform dark = shadow / wet / paint
            continue
        depth_contrast = float(rel[y:y + bh, x:x + bw].max())
        attrs = {"texture_ratio": round(e, 2), "contrast": round(depth_contrast, 1), "width_m": round(gw, 2), "length_m": round(gl, 2),
                 "forward_m": round(fwd, 1), "lateral_m": round(lat, 2)}
        conf = float(min(0.65, 0.25 + 0.08 * min(e, 4) + 0.003 * min(depth_contrast, 60)))
        out.append(_det(AssetType.POTHOLE, "pothole_classical", conf, BBox(x1=x, y1=y, x2=x + bw, y2=y + bh), frame, attrs))
    out.sort(key=lambda d: -d.confidence)
    return out[:12]


# ----------------------------------------------------------------------------- vertical elements
def _contour_shape(c) -> str:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    n = len(approx)
    area = cv2.contourArea(c)
    (x, y), r = cv2.minEnclosingCircle(c)
    circ = area / (math.pi * r * r + 1e-6)
    if n == 3:
        return "triangle"
    if n == 4:
        return "rect"
    if n == 8:
        return "octagon"
    if circ > 0.72:
        return "circle"
    return "other"


def detect_signs_by_colour(img: np.ndarray, frame: FrameRef, ipm: IPM) -> List[Detection]:
    """Colour+shape sign candidates (IRC:67): red ring = mandatory, red triangle = cautionary, solid red octagon = STOP,
    inverted triangle = give way, solid blue rect/circle = informatory / compulsory direction.

    Discrimination uses fill ratio (solid vs ring) + polygon shape; lit signal lamps (small, in dark housings) and
    sky patches are rejected explicitly."""
    h, w = img.shape[:2]
    hz = int(max(0, min(h, ipm.horizon_row)))
    top = img[: int(hz + 0.15 * h)]
    hsv_top = C.hsv(top)
    out = []
    for colour, m in (("red", C.red_mask(top)), ("blue", C.blue_mask(top))):
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 120:
                continue
            x, y, bw, bh = cv2.boundingRect(c)
            ar = bw / (bh + 1e-6)
            if not (0.5 <= ar <= 2.0) or bw > 0.3 * w or bh > 0.3 * h:
                continue
            if bw < 12:
                continue
            fill = float((m[y:y + bh, x:x + bw] > 0).mean())      # mask fraction (holes count), not contour area
            shape = _contour_shape(c)
            roi = hsv_top[y:y + bh, x:x + bw]
            white_in = float(((roi[:, :, 2] > 170) & (roi[:, :, 1] < 70)).mean())
            # lit lamp test: very bright core + dark housing around -> traffic signal, not a sign
            pad = max(2, bw // 2)
            ring = hsv_top[max(0, y - pad):y + bh + pad, max(0, x - pad):x + bw + pad]
            dark_frac = float((ring[:, :, 2] < 70).mean()) if ring.size else 0.0
            if colour == "red" and bw < 30 and white_in < 0.03 and dark_frac > 0.35 and float((roi[:, :, 2] > 200).mean()) > 0.5:
                continue   # lit lamp in a dark housing (traffic signal) - handled by detect_signal_heads
            if colour == "red":
                if shape == "triangle":
                    M = cv2.moments(c)
                    cy = M["m01"] / (M["m00"] + 1e-6)
                    asset, label, conf = (AssetType.SIGN_GIVE_WAY, "give_way", 0.5) if cy < y + bh / 2 else (AssetType.SIGN_CAUTIONARY, "cautionary_triangle", 0.55)
                elif fill >= 0.55 and white_in < 0.35 and shape in ("octagon", "circle", "rect", "other"):
                    # solid red plate with a little white text: STOP octagon
                    if white_in < 0.01 and bw < 24:
                        continue   # featureless small red blob (tail lamp, flag, cloth)
                    asset, label, conf = AssetType.SIGN_STOP, "stop_sign", 0.55
                elif fill < 0.55 and white_in >= 0.15 and shape in ("circle", "octagon", "other", "rect"):
                    # red ring with white centre: mandatory / prohibitory
                    asset, label, conf = AssetType.SIGN_MANDATORY, "mandatory_circle", 0.5
                else:
                    continue
            else:
                # sky / water rejection: real blue plates are saturated and not huge
                if float(roi[:, :, 1].mean()) < 140 or bh > 0.2 * h:
                    continue
                if shape in ("rect", "circle") and fill > 0.6:
                    asset, label, conf = AssetType.SIGN_INFORMATORY, "blue_sign", 0.45
                else:
                    continue
            rng = float(np.clip(ipm.range_from_width(bw, 0.75), 4, 80))   # IRC:67 medium plate 750 mm (600-900)
            attrs = {"colour": colour, "shape": shape, "fill": round(float(fill), 2), "forward_m": round(rng, 1), "plate_px": int(bw),
                     "lateral_m": round((x + bw / 2 - ipm.cam.cx) / ipm.cam.fx * rng, 2)}
            if bw >= 22 and rng <= 40:   # height from the plate's bottom edge is only reliable for near, well-resolved plates
                attrs["mounting_height_m"] = round(float(ipm.height_above_ground(y + bh, rng)), 2)
            out.append(_det(asset, label, conf, BBox(x1=x, y1=y, x2=x + bw, y2=y + bh), frame, attrs))
    return out[:10]


def detect_signal_heads(img: np.ndarray, frame: FrameRef, ipm: IPM) -> List[Detection]:
    """Lit red/amber/green lamps inside dark housings above the horizon."""
    h, w = img.shape[:2]
    hz = int(max(0, min(h, ipm.horizon_row)))
    top = img[: max(10, hz)]
    hsvi = C.hsv(top)
    bright = hsvi[:, :, 2] > 200
    sat = hsvi[:, :, 1] > 120
    out = []
    for colour, (lo, hi) in (("red", (0, 10)), ("red", (165, 180)), ("amber", (12, 32)), ("green", (45, 95))):
        hue = (hsvi[:, :, 0] >= lo) & (hsvi[:, :, 0] <= hi)
        m = (bright & sat & hue).astype(np.uint8) * 255
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 25 or area > 0.002 * h * w:
                continue
            (x, y), r = cv2.minEnclosingCircle(c)
            if area / (math.pi * r * r + 1e-6) < 0.6:
                continue
            x0, y0 = int(x - 2.5 * r), int(y - 2.5 * r); x1, y1 = int(x + 2.5 * r), int(y + 2.5 * r)
            x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(w, x1), min(top.shape[0], y1)
            ring = top[y0:y1, x0:x1]
            dark_frac = (C.hsv(ring)[:, :, 2] < 70).mean() if ring.size else 0
            if dark_frac < 0.25:  # lamps live in black housings
                continue
            out.append(_det(AssetType.TRAFFIC_SIGNAL, f"signal_{colour}", 0.5 + 0.3 * min(1.0, dark_frac),
                            BBox(x1=x0, y1=y0, x2=x1, y2=y1), frame, {"colour": colour}))
    return out[:6]


def detect_poles(img: np.ndarray, frame: FrameRef, ipm: IPM) -> List[Detection]:
    """Tall thin vertical structures (street-light / signal / utility poles, tree trunks).

    A pole is a narrow column that is darker than its left and right neighbourhood over a long vertical run
    crossing the horizon. We scan columns of a contrast map (centre minus side means, 7 px wide) above the horizon
    and keep runs longer than 18% of the image height, then group adjacent columns.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape
    hz = int(max(10, min(h - 10, ipm.horizon_row)))
    top = gray[:hz + int(0.08 * h)]
    k = 7
    centre = cv2.blur(top, (3, 9))
    left = np.roll(cv2.blur(top, (k, 9)), k, axis=1)
    right = np.roll(cv2.blur(top, (k, 9)), -k, axis=1)
    contrast = np.minimum(left - centre, right - centre)        # dark relative to BOTH sides
    cand = contrast > 18
    out = []
    cols = cand.mean(axis=0)
    min_run = int(0.18 * h)
    for a_, b_ in _runs(cols > 0.25):
        if (b_ - a_ + 1) > 0.03 * w:
            continue
        cx = (a_ + b_) / 2
        colmask = cand[:, a_:b_ + 1].any(axis=1)
        runs = _runs(colmask)
        if not runs:
            continue
        r0, r1 = max(runs, key=lambda r: r[1] - r[0])
        if (r1 - r0) < min_run or r1 < hz - 0.25 * h:   # must reach near / below the horizon
            continue
        # extend the base downward along the dark column into the perspective image to find the ground contact
        base = r1
        col = gray[:, int(cx)]
        while base + 1 < h and col[base + 1] < col[max(0, base - 5)] + 25 and base < hz + 0.45 * h:
            base += 1
        attrs = {"height_px": float(base - r0), "width_px": float(b_ - a_ + 1)}
        g = ipm.pixel_to_ground(cx, base)
        if g is not None and 2.0 < g[1] < 80.0:
            attrs.update({"forward_m": round(g[1], 1), "lateral_m": round(g[0], 2)})
        out.append(_det(AssetType.POLE, "pole", 0.4, BBox(x1=a_ - 2, y1=r0, x2=b_ + 2, y2=base), frame, attrs))
    return out[:10]


def night_lighting_metrics(img: np.ndarray, ipm: IPM) -> Dict[str, float]:
    """Night-time proxies: road luminance, luminance uniformity (min/avg), bright point sources above horizon."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    hz = int(max(0, min(h - 1, ipm.horizon_row)))
    road = gray[hz:, int(w * 0.2): int(w * 0.8)]
    cols = road.mean(axis=0)
    rows = road.mean(axis=1)
    uni = float(min(cols.min() / (cols.mean() + 1e-6), rows.min() / (rows.mean() + 1e-6)))
    top = gray[:hz]
    srcs = 0
    if top.size:
        m = (top > 235).astype(np.uint8)
        n, _ = cv2.connectedComponents(m)
        srcs = max(0, n - 1)
    return {"road_luma": float(road.mean()), "luma_uniformity": uni, "point_sources": float(srcs),
            "overall_luma": float(gray.mean())}


# ----------------------------------------------------------------------------- kerb / median paint
def detect_painted_kerb(bev: np.ndarray, meta: Dict, frame: FrameRef, ipm: IPM) -> List[Detection]:
    """Black-white or black-yellow alternating kerb paint along the road edge/median (IRC:35 object marking)."""
    ppm = meta["px_per_m"]
    wm = C.white_mask(bev); ym = C.yellow_mask(bev); dk = C.dark_mask(bev, 45)
    H, W = wm.shape
    out = []
    for name, m in (("white", wm), ("yellow", ym)):
        col = (m > 0).mean(axis=0)
        for a, b in _runs(col > 0.25):
            if (b - a + 1) / ppm > 0.6:
                continue
            strip = m[:, a:b + 1].mean(axis=1) > 100
            dstrip = dk[:, a:b + 1].mean(axis=1) > 100
            r = _runs(strip)
            if len(r) < 3:
                continue
            seglen = np.array([(e - s + 1) / ppm for s, e in r])
            if 0.3 <= np.median(seglen) <= 1.5 and dstrip.mean() > 0.2:
                lat, _ = IPM.bev_to_ground((a + b) / 2, H / 2, meta)
                side = "left" if lat < 0 else "right"
                u1, v1 = ipm.ground_to_pixel(lat, meta["z_range"][0]); u2, v2 = ipm.ground_to_pixel(lat, meta["z_range"][1])
                out.append(_det(AssetType.KERB, f"painted_kerb_{name}", 0.5, BBox(x1=min(u1, u2) - 5, y1=min(v1, v2), x2=max(u1, u2) + 5, y2=max(v1, v2)),
                                frame, {"paint": f"black_{name}", "side": side, "lateral_m": round(lat, 2)}))
    return out


class ClassicalDetector(Detector):
    name = "classical_cv"

    def __init__(self, cam: CameraModel, enable_potholes: bool = True):
        self.cam = cam
        self.ipm = IPM(cam)
        self.enable_potholes = enable_potholes
        self.last_metrics: Dict[str, object] = {}
        self.last_scale_hint: Optional[float] = None

    def detect(self, img: np.ndarray, frame: FrameRef, cam: Optional[CameraModel] = None) -> List[Detection]:
        if cam is not None and cam is not self.cam:
            self.cam, self.ipm = cam, IPM(cam)
        dets: List[Detection] = []
        raw = img
        img = C.normalise_exposure(img)
        bev, meta = self.ipm.birdseye(img, x_range=(-9.0, 9.0), z_range=(4.0, 28.0), px_per_m=32.0)
        road = drivable_mask(img, self.ipm)
        cw = carriageway_width_from_mask(road, self.ipm)
        zebra = detect_zebra(bev, meta, frame, self.ipm)
        stops = detect_stop_line(bev, meta, frame, self.ipm)
        humps = detect_speed_hump_markings(bev, meta, frame, self.ipm, zebra)
        excl = []
        for d in zebra + stops + humps:
            z0 = d.attributes.get("forward_m")
            L = d.attributes.get("crossing_length_m") or d.attributes.get("band_length_m") or d.attributes.get("thickness_m") or 0.5
            if z0 is not None:
                r1 = int(meta["H"] - (z0 + L + 0.3 - meta["z_range"][0]) * meta["px_per_m"])
                r2 = int(meta["H"] - (z0 - 0.3 - meta["z_range"][0]) * meta["px_per_m"])
                excl.append((r1, r2))
        lane_dets, lane_info = detect_lane_lines(bev, meta, frame, self.ipm, excl)
        dets += lane_dets + zebra + stops + humps
        dets += detect_painted_kerb(bev, meta, frame, self.ipm)
        # carriageway width: prefer outermost longitudinal lines (edge lines / kerb paint) over the colour mask
        lats = sorted(d.attributes["lateral_m"] for d in lane_dets)
        cw_lines = None
        if len(lats) >= 2 and (lats[-1] - lats[0]) >= 4.5 and lats[0] < -1.0 and lats[-1] > 1.0:
            cw_lines = (lats[-1] - lats[0] + 0.3, 0.75)
        if cw_lines and (cw is None or abs(cw_lines[0] - cw[0]) > 0.5):
            cw = cw_lines
        if self.enable_potholes:
            bands = []
            for d in zebra + stops + humps:
                z0 = d.attributes.get("forward_m")
                L = d.attributes.get("crossing_length_m") or d.attributes.get("band_length_m") or d.attributes.get("thickness_m") or 0.5
                if z0 is not None:
                    bands.append((z0 - 0.7, z0 + L + 0.7))
            dets += detect_potholes_classical(img, road, frame, self.ipm, bands, (cw[0] / 2) if cw else None)
        # scale hint: IRC:35 zebra stripe period is 1.0 m (0.5 stripe + 0.5 gap) -> corrects unknown camera height
        hints = [d.attributes["stripe_period_m"] for d in zebra if d.attributes.get("n_stripes", 0) >= 4]
        self.last_scale_hint = (1.0 / float(np.median(hints))) if hints else None
        dets += detect_signs_by_colour(img, frame, self.ipm)
        dets += detect_signal_heads(img, frame, self.ipm)
        dets += detect_poles(img, frame, self.ipm)
        light = night_lighting_metrics(img, self.ipm)
        self.last_metrics = {"carriageway_width_m": cw[0] if cw else None, "carriageway_conf": cw[1] if cw else 0.0,
                             **lane_info, **light, "road_mask_frac": float((road > 0).mean()),
                             "scale_hint": self.last_scale_hint}
        for d in dets:
            d.attributes.setdefault("frame_metrics", {})
        return dets
