"""Batch audit: run several media files with one configuration and write a combined index (JSON + Markdown).

Usage: python -m cfi_road_auditor.batch --out outputs/batch --mode walk --road-class urban_arterial video1.MOV video2.MOV ...
Each media file gets its own sub-directory with the full report set; batch_index.json / batch_index.md summarise them.
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

from .config import AuditConfig, CameraDefaults, PerceptionConfig, SamplingConfig
from .schemas import RoadClass, Terrain


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cfi-batch")
    ap.add_argument("media", nargs="+")
    ap.add_argument("--out", default="outputs/batch")
    ap.add_argument("--mode", default="drive", choices=["drive", "walk"])
    ap.add_argument("--road-class", default="urban_arterial", choices=[r.value for r in RoadClass])
    ap.add_argument("--terrain", default="plain", choices=[t.value for t in Terrain])
    ap.add_argument("--posted-speed", type=float)
    ap.add_argument("--camera-height", type=float, default=1.3)
    ap.add_argument("--camera-pitch", type=float, default=2.0)
    ap.add_argument("--hfov", type=float, default=70.0)
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("--max-frames", type=int, default=600)
    ap.add_argument("--assumed-speed", type=float, default=30.0)
    ap.add_argument("--vlm", action="store_true")
    ap.add_argument("--vlm-cache-root", help="directory containing <media_stem>/ sub-folders of per-frame checklist JSON")
    ap.add_argument("--title-prefix", default="Road Safety Audit")
    ap.add_argument("--location", default="")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("ezdxf").setLevel(logging.WARNING)
    from .pipeline import audit
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows: List[Dict] = []
    for m in a.media:
        stem = Path(m).stem
        cache = str(Path(a.vlm_cache_root) / stem) if a.vlm_cache_root and (Path(a.vlm_cache_root) / stem).exists() else None
        cfg = AuditConfig(
            survey_mode=a.mode, road_class=RoadClass(a.road_class), terrain=Terrain(a.terrain), posted_speed_kmph=a.posted_speed,
            perception=PerceptionConfig(use_vlm=a.vlm, vlm_cache_dir=cache),
            sampling=SamplingConfig(frame_interval_s=a.interval, max_frames=a.max_frames),
            camera=CameraDefaults(height_m=a.camera_height, pitch_deg=a.camera_pitch, hfov_deg=a.hfov),
            out_dir=out / stem, title=f"{a.title_prefix} - {stem}", verbose=False)
        try:
            rep = audit(m, cfg, None, {"location": a.location, "assumed_speed_kmph": a.assumed_speed})
            s = rep.summary
            rows.append({"media": m, "report_id": rep.report_id, "score": s.overall_score, "stars": s.star_rating, "findings": s.n_findings,
                         "by_severity": s.n_by_severity, "length_m": round(s.length_m), "coverage_pct": s.coverage_pct,
                         "checklist": s.checklist_counts, "top_risks": s.top_risks, "outputs": rep.outputs, "status": "ok"})
        except Exception as e:  # keep going
            logging.exception("audit failed for %s", m)
            rows.append({"media": m, "status": "failed", "error": str(e)})
    (out / "batch_index.json").write_text(json.dumps(rows, indent=1, default=str))
    lines = [f"# Batch audit index ({len(rows)} media)", "", "| Media | Length | Score | Findings (C/H/M/L) | Coverage | Report |", "|---|---|---|---|---|---|"]
    for r in rows:
        if r.get("status") != "ok":
            lines.append(f"| {Path(r['media']).name} | - | failed | {r.get('error', '')[:60]} | - | - |"); continue
        b = r["by_severity"]
        lines.append(f"| {Path(r['media']).name} | {r['length_m']} m | {r['score']} | {r['findings']} ({b.get('critical', 0)}/{b.get('high', 0)}/{b.get('medium', 0)}/{b.get('low', 0)}) | {r['coverage_pct']}% | {r['outputs'].get('pdf', '')} |")
    (out / "batch_index.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
