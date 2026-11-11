"""Command-line interface: cfi-audit <video|image> [--track file.gpx] [--road-class urban_arterial] ..."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from .config import AuditConfig, PerceptionConfig, SamplingConfig, CameraDefaults
from .schemas import RoadClass, Terrain


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cfi-audit", description="CFI Road Auditor - automated Road Safety Audit for Indian roads")
    ap.add_argument("media", help="video or image file")
    ap.add_argument("--track", help="GPS track (gpx/csv/srt/nmea/json)")
    ap.add_argument("--out", default="outputs/audit", help="output directory")
    ap.add_argument("--road-class", default="urban_arterial", choices=[r.value for r in RoadClass])
    ap.add_argument("--terrain", default="plain", choices=[t.value for t in Terrain])
    ap.add_argument("--design-speed", type=float)
    ap.add_argument("--posted-speed", type=float)
    ap.add_argument("--title", default="Road Safety Audit")
    ap.add_argument("--location", default="")
    ap.add_argument("--interval", type=float, default=1.0, help="frame interval seconds")
    ap.add_argument("--max-frames", type=int, default=600)
    ap.add_argument("--segment", type=float, default=50.0, help="segment length m")
    ap.add_argument("--reuse-frames", help="frames directory of a previous run of the same media (skips decoding)")
    ap.add_argument("--camera-height", type=float, default=1.3)
    ap.add_argument("--camera-pitch", type=float, default=2.0)
    ap.add_argument("--hfov", type=float, default=70.0)
    ap.add_argument("--weights", help="general YOLO weights")
    ap.add_argument("--damage-weights", help="road-damage YOLO weights")
    ap.add_argument("--sign-weights", help="traffic-sign YOLO weights")
    ap.add_argument("--no-classical", action="store_true")
    ap.add_argument("--vlm", action="store_true", help="run Claude vision checklist pass (needs ANTHROPIC_API_KEY)")
    ap.add_argument("--vlm-frames", type=int, default=24)
    ap.add_argument("--vlm-cache", help="directory with per-frame checklist JSON (offline / reviewed vision results)")
    ap.add_argument("--mode", default="drive", choices=["drive", "walk"], help="drive = vehicle camera; walk = auditor walking the footpath")
    ap.add_argument("--assumed-speed", type=float, default=30.0, help="km/h used for chainage when no GPS")
    ap.add_argument("-q", "--quiet", action="store_true")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.WARNING if a.quiet else logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    cfg = AuditConfig(
        road_class=RoadClass(a.road_class), terrain=Terrain(a.terrain), design_speed_kmph=a.design_speed, posted_speed_kmph=a.posted_speed,
        perception=PerceptionConfig(yolo_weights=a.weights, damage_weights=a.damage_weights, sign_weights=a.sign_weights,
                                    use_classical=not a.no_classical, use_vlm=a.vlm, vlm_max_frames=a.vlm_frames, vlm_cache_dir=a.vlm_cache),
        survey_mode=a.mode,
        sampling=SamplingConfig(frame_interval_s=a.interval, max_frames=a.max_frames, segment_length_m=a.segment, reuse_frames_dir=a.reuse_frames),
        camera=CameraDefaults(height_m=a.camera_height, pitch_deg=a.camera_pitch, hfov_deg=a.hfov),
        out_dir=Path(a.out), title=a.title, verbose=not a.quiet,
    )
    from .pipeline import audit
    rep = audit(a.media, cfg, a.track, context={"location": a.location, "assumed_speed_kmph": a.assumed_speed})
    s = rep.summary
    print(json.dumps({"report_id": rep.report_id, "score": s.overall_score, "stars": s.star_rating, "findings": s.n_findings,
                      "by_severity": s.n_by_severity, "coverage_pct": s.coverage_pct, "outputs": rep.outputs}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
