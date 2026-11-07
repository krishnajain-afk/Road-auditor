"""Evaluation harness: synthetic scenes with exact ground truth -> detection P/R per class + measurement errors.

Usage: python -m cfi_road_auditor.eval.harness --n 60 --out outputs/eval
Matching: a GT asset is matched if a detection of the same class lies within a class-specific tolerance in ground
coordinates (forward +/- 3 m, lateral +/- 1.5 m) or, for lane lines, lateral +/- 0.4 m. Measurement errors are
reported as mean absolute error and the fraction within tolerance (IRC-relevant tolerances: lane width 0.15 m,
stripe width 0.1 m, crossing length 0.5 m, pothole width 0.2 m, sign mounting height 0.3 m).
"""
from __future__ import annotations

import argparse
import json
import os
import time
from collections import defaultdict
from typing import Dict, List

import cv2
import numpy as np

from ..geometry.camera import IPM, build_camera, calibrate_pitch_from_frames
from ..perception.classical import ClassicalDetector
from ..perception.fusion import fuse, localise
from ..schemas import FrameRef
from .synth import SceneSpec, random_spec, render

CLASSES = ["zebra_crossing", "stop_line", "speed_hump", "pothole", "sign", "traffic_signal", "lane_line", "pole"]
TOL = {"height_m": 0.1, "lane_width_m": 0.15, "line_width_m": 0.06, "stripe_width_m": 0.10, "crossing_length_m": 0.5, "pothole_width_m": 0.2,
       "pothole_forward_m": 1.0, "mounting_height_m": 0.3, "pitch_deg": 0.5, "carriageway_width_m": 0.3}


def _cls(name: str) -> str:
    return "sign" if name.startswith("sign_") else ("lane_line" if name in ("lane_line", "centre_line", "edge_line") else name)


def evaluate(n: int, out_dir: str, seed0: int = 1000, use_yolo: bool = False, calibrate: bool = True, known_height: bool = False) -> Dict:
    os.makedirs(out_dir, exist_ok=True)
    tp = defaultdict(int); fp = defaultdict(int); fn = defaultdict(int)
    errs: Dict[str, List[float]] = defaultdict(list)
    per_scene = []
    t0 = time.time()
    for i in range(n):
        spec = random_spec(seed0 + i)
        img, gt, true_cam = render(spec)
        fr = FrameRef(index=0, t=0.0, path=os.path.join(out_dir, f"scene_{i:03d}.jpg"), chainage_m=0.0)
        cv2.imwrite(fr.path, img)
        # the pipeline does not know the true pitch/height: start from defaults and self-calibrate
        cam = build_camera(spec.width_px, spec.height_px, spec.hfov_deg, spec.cam_height_m if known_height else 1.3, 2.0, "default", 0.4)
        if calibrate:
            cam = calibrate_pitch_from_frames([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)], cam)
        errs["pitch_deg"].append(abs(cam.pitch_deg - spec.pitch_deg))
        det = ClassicalDetector(cam)
        dets = det.detect(img, fr, cam)
        if calibrate and not known_height and det.last_scale_hint and 0.6 < det.last_scale_hint < 1.6:
            cam = cam.model_copy(update={"height_m": cam.height_m * det.last_scale_hint})
            det = ClassicalDetector(cam)
            dets = det.detect(img, fr, cam)
        errs["height_m"].append(abs(cam.height_m - spec.cam_height_m))
        m = det.last_metrics
        ipm = IPM(cam)
        for d in dets:
            localise(d, fr, ipm)
        # ---- carriageway / lane width
        road_w = spec.lane_width_m * spec.n_lanes
        if m.get("carriageway_width_m"):
            errs["carriageway_width_m"].append(abs(m["carriageway_width_m"] - road_w))
        if m.get("lane_widths_m"):
            errs["lane_width_m"].append(abs(float(np.median(m["lane_widths_m"])) - spec.lane_width_m))
        else:
            errs["lane_width_missing"].append(1.0)
        for lw in m.get("line_widths_m", []):
            errs["line_width_m"].append(abs(lw - spec.line_width_m))
        # ---- matching
        # unmarked humps have no paint signature: not detectable by the marking detector (needs VLM / profile) -> excluded
        gts = [g for g in gt["assets"] if not (g["type"] == "speed_hump" and not g.get("marked", True))]
        used = set()
        for g in gts:
            c = _cls(g["type"])
            best = None; bd = 1e9
            for j, d in enumerate(dets):
                if j in used or _cls(d.asset.value) != c:
                    continue
                if c == "lane_line":
                    dist = abs(d.attributes.get("lateral_m", 99) - g["lateral_m"])
                    ok = dist < 0.4
                else:
                    fwd = d.attributes.get("forward_m", d.ground_xy_m[1] if d.ground_xy_m else None)
                    lat = d.attributes.get("lateral_m", d.ground_xy_m[0] if d.ground_xy_m else None)
                    if fwd is None:
                        continue
                    dist = abs(fwd - g["forward_m"])
                    tol_f = 3.0 if c not in ("sign", "traffic_signal", "pole") else 8.0
                    tol_l = 1.0 if c == "pothole" else (3.0 if c in ("sign", "traffic_signal", "pole") else 1.5)
                    ok = dist < tol_f and (lat is None or g.get("lateral_m") is None or abs(lat - g["lateral_m"]) < tol_l)
                if ok and dist < bd:
                    best, bd = j, dist
            if best is None:
                fn[c] += 1
                continue
            used.add(best); tp[c] += 1
            d = dets[best]
            if c == "zebra_crossing":
                errs["stripe_width_m"].append(abs(d.attributes["stripe_width_m"] - g["stripe_width_m"]))
                errs["crossing_length_m"].append(abs(d.attributes["crossing_length_m"] - g["length_m"]))
                errs["zebra_forward_m"].append(abs(d.attributes["forward_m"] - g["forward_m"]))
            elif c == "pothole":
                errs["pothole_width_m"].append(abs(d.attributes.get("width_m", 0) - g["width_m"]))
                errs["pothole_forward_m"].append(abs(d.attributes.get("forward_m", 0) - g["forward_m"]))
            elif c == "sign":
                if "mounting_height_m" in d.attributes:
                    errs["mounting_height_m"].append(abs(d.attributes["mounting_height_m"] - 2.1))
                errs["sign_forward_m"].append(abs(d.attributes["forward_m"] - g["forward_m"]))
                if d.asset.value != g["type"]:
                    errs["sign_type_mismatch"].append(1.0)
                else:
                    errs["sign_type_mismatch"].append(0.0)
            elif c == "stop_line":
                errs["stop_thickness_m"].append(abs(d.attributes["thickness_m"] - spec.stop_line_thick_m))
            elif c == "speed_hump":
                errs["hump_marked_correct"].append(1.0 if bool(d.attributes.get("marked")) == bool(g["marked"]) else 0.0)
        for j, d in enumerate(dets):
            if j not in used:
                c = _cls(d.asset.value)
                if c in CLASSES:
                    fp[c] += 1
        per_scene.append({"seed": spec.seed, "n_gt": len(gts), "n_det": len(dets), "night": spec.night})
    res = {"n_scenes": n, "runtime_s": round(time.time() - t0, 1), "classes": {}, "measurements": {}}
    for c in CLASSES:
        P = tp[c] / max(1, tp[c] + fp[c]); R = tp[c] / max(1, tp[c] + fn[c])
        res["classes"][c] = {"tp": tp[c], "fp": fp[c], "fn": fn[c], "precision": round(P, 3), "recall": round(R, 3),
                             "f1": round(2 * P * R / max(1e-9, P + R), 3)}
    for k, v in errs.items():
        arr = np.array(v)
        if k.endswith("_mismatch") or k.endswith("_correct") or k.endswith("_missing"):
            res["measurements"][k] = {"n": len(arr), "rate": round(float(arr.mean()), 3)}
        else:
            tol = TOL.get(k)
            res["measurements"][k] = {"n": len(arr), "mae": round(float(arr.mean()), 3), "p90": round(float(np.percentile(arr, 90)), 3),
                                      **({"within_tol": round(float((arr <= tol).mean()), 3), "tol": tol} if tol else {})}
    with open(os.path.join(out_dir, "metrics.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--out", default="outputs/eval")
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--no-calib", action="store_true")
    ap.add_argument("--known-height", action="store_true", help="camera height supplied by the user (measured mount)")
    a = ap.parse_args()
    res = evaluate(a.n, a.out, a.seed, calibrate=not a.no_calib, known_height=a.known_height)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
