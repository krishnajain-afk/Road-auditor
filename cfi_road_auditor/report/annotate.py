"""Draw detections / findings onto frames for evidence."""
from __future__ import annotations

import os
from typing import Dict, List, Optional

import cv2

from ..schemas import Asset, Finding, Severity

COLORS = {Severity.CRITICAL: (0, 0, 255), Severity.HIGH: (0, 100, 255), Severity.MEDIUM: (0, 200, 255),
          Severity.LOW: (0, 200, 0), Severity.INFO: (200, 200, 200)}


def annotate_finding(f: Finding, out_dir: str) -> Optional[str]:
    if not f.evidence or not f.evidence[0].frame_path or not os.path.exists(f.evidence[0].frame_path):
        return None
    ev = f.evidence[0]
    img = cv2.imread(ev.frame_path)
    if img is None:
        return None
    col = COLORS[f.severity]
    if ev.bbox:
        b = ev.bbox
        cv2.rectangle(img, (int(b.x1), int(b.y1)), (int(b.x2), int(b.y2)), col, 3)
    label = f"{f.finding_id}  {f.title[:48]}"
    cv2.rectangle(img, (0, 0), (min(img.shape[1], 12 * len(label) + 20), 34), (0, 0, 0), -1)
    cv2.putText(img, label, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.65, col, 2, cv2.LINE_AA)
    cv2.putText(img, f"Ch. {f.chainage_m:.0f} m | {f.severity.value.upper()} | risk {f.risk_score}", (10, img.shape[0] - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, f"{f.finding_id}.jpg")
    cv2.imwrite(p, img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return p


def annotate_assets_frame(frame_path: str, assets: List[Asset], out_path: str) -> Optional[str]:
    img = cv2.imread(frame_path)
    if img is None:
        return None
    for a in assets:
        if a.bbox_in_best_frame:
            b = a.bbox_in_best_frame
            cv2.rectangle(img, (int(b.x1), int(b.y1)), (int(b.x2), int(b.y2)), (255, 160, 0), 2)
            cv2.putText(img, f"{a.asset.value} {a.confidence:.2f}", (int(b.x1), max(12, int(b.y1) - 4)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 160, 0), 1, cv2.LINE_AA)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return out_path
