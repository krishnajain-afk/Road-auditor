"""End-to-end orchestration: media -> frames -> perception -> fusion -> road model -> rules -> report."""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np

from . import __version__
from .config import AuditConfig
from .geometry.camera import build_camera, calibrate_pitch_from_frames, guess_hfov
from .ingest.gps import estimate_chainage_without_gps, load_track, sync_track_to_frames, track_from_video
from .ingest.media import extract_frames, probe_media
from .perception.fusion import count_moving_per_frame, fuse
from .perception.registry import build_detectors
from .report.builder import build_report, write_all_outputs
from .roadmodel import build_road_model
from .rules.engine import RuleEngine
from .schemas import AuditReport, Detection, FrameRef, GeoPoint
from .scoring.risk import summarise

log = logging.getLogger("cfi")
logging.getLogger("ezdxf").setLevel(logging.WARNING)

# which AssetTypes each backend can emit - used by the rule engine to report 'not assessed' honestly
CLASSICAL_ASSETS = {"zebra_crossing", "stop_line", "lane_line", "centre_line", "speed_hump", "rumble_strip", "kerb", "pothole",
                    "sign_mandatory", "sign_cautionary", "sign_stop", "sign_give_way", "sign_informatory", "traffic_signal", "pole"}
COCO_ASSETS = {"pedestrian", "cyclist", "car", "motorcycle", "bus", "truck", "traffic_signal", "sign_stop", "animal", "bollard", "bus_stop"}
DAMAGE_ASSETS = {"pothole", "crack_longitudinal", "crack_transverse", "crack_alligator", "manhole", "patch"}
SIGN_ASSETS = {"sign_mandatory", "sign_cautionary", "sign_informatory", "sign_stop", "sign_give_way", "sign_speed_limit",
               "sign_pedestrian_crossing", "sign_speed_breaker", "sign_school", "sign_unknown"}
VLM_ASSETS = {a.value for a in __import__("cfi_road_auditor.schemas", fromlist=["AssetType"]).AssetType}


def detectable_assets(detector_names, vlm_used: bool) -> Dict[str, bool]:
    caps = set()
    for n in detector_names:
        if n == "classical_cv":
            caps |= CLASSICAL_ASSETS
        elif n == "yolo_general":
            caps |= COCO_ASSETS
        elif n == "yolo_damage":
            caps |= DAMAGE_ASSETS
        elif n == "yolo_sign":
            caps |= SIGN_ASSETS
    if vlm_used:
        caps |= VLM_ASSETS
    return {c: True for c in caps}

STANDARDS = ["IRC:SP:88-2019 (RSA Manual)", "IRC:35-2015 (Road Markings)", "IRC:67-2022 (Road Signs)", "IRC:103-2012 (Pedestrian Facilities)",
             "IRC:86-2018 (Urban Roads Geometric Design)", "IRC:73-1980 (Rural Roads Geometric Design)", "IRC:99-2018 (Traffic Calming)",
             "IRC:93-1985 (Traffic Signals)", "IRC:38-1988 (Horizontal Curves)", "IRC:SP:41-1994 (At-grade Intersections)",
             "IRC:82-2015 (Maintenance of Bituminous Surfaces)", "IRC:119-2015 (Crash Barriers)", "IRC:SP:55-2014 (Work Zones)",
             "IRC:80-1981 (Bus Bays)", "IRC:SP:12-2015 (Parking)", "IS 1944 (Street Lighting)", "MoRTH S.O.1522(E) 2018 (Speed limits)",
             "MV (Amendment) Act 2019 S.198A"]


def audit(media_path: str, cfg: AuditConfig, track_path: Optional[str] = None, context: Optional[Dict] = None) -> AuditReport:
    t0 = time.time()
    out_dir = Path(cfg.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = out_dir / "frames"
    # 1. media + frames
    media = probe_media(media_path)
    log.info("media: %s %dx%d %.1fs", media.kind, media.width, media.height, media.duration_s)
    track: List[GeoPoint] = []
    if track_path:
        track = load_track(track_path, media)
    if not track:
        track = track_from_video(media)
    log.info("track points: %d", len(track))
    frames = _load_frame_manifest(cfg, media) or extract_frames(media, str(frames_dir), interval_s=cfg.sampling.frame_interval_s,
                                                                   max_frames=cfg.sampling.max_frames, resize_long_edge=cfg.sampling.resize_long_edge)
    _save_frame_manifest(frames_dir, cfg, media, frames)
    if len(track) >= 2:
        frames = sync_track_to_frames(frames, track)
    else:
        frames = estimate_chainage_without_gps(frames, assumed_speed_kmph=float((context or {}).get("assumed_speed_kmph", 30.0)))
    if not frames:
        raise RuntimeError("no frames extracted")
    # 2. camera model
    fw, fh = (cv2.imread(frames[0].path).shape[1::-1])
    exif = (media.extra or {}).get("exif", {}) if media.kind == "image" else {}
    hfov, src = guess_hfov(media.device_make, media.device_model, exif.get("focal_35mm"), cfg.camera.hfov_deg)
    cam = build_camera(fw, fh, hfov, height_m=cfg.camera.height_m, pitch_deg=cfg.camera.pitch_deg, source=src,
                       confidence=0.6 if src != "default" else 0.4)
    sample = [cv2.cvtColor(cv2.imread(f.path), cv2.COLOR_BGR2GRAY) for f in frames[:: max(1, len(frames) // 25)][:25]]
    cam_vp = calibrate_pitch_from_frames(sample, cam)
    if cfg.survey_mode == "walk":
        # head-worn / hand-held cameras: the vanishing point is often set by walls, fences and tree lines, not the path.
        # Accept the estimate only when it is a plausible downward look (5-25 deg); otherwise keep the user's pitch.
        cam = cam_vp if 5.0 <= cam_vp.pitch_deg <= 25.0 else cam
    else:
        cam = cam_vp
    if cfg.survey_mode != "walk":
        cam = calibrate_height_from_zebra(frames, cam, cfg)
    log.info("camera: hfov %.1f (%s) pitch %.1f height %.2f", cam.hfov_deg or 0, cam.source, cam.pitch_deg, cam.height_m)
    # 3. perception
    detectors = build_detectors(cfg.perception, cam, cfg.survey_mode)
    names = [d.name for d in detectors]
    log.info("detectors: %s", names)
    detections: List[Detection] = []
    frame_metrics: Dict[int, Dict] = {}
    for i, fr in enumerate(frames):
        img = cv2.imread(fr.path)
        if img is None:
            continue
        for d in detectors:
            try:
                detections.extend(d.detect(img, fr, cam))
            except Exception as e:  # pragma: no cover
                log.warning("detector %s failed on frame %d: %s", d.name, fr.index, e)
            if d.name == "classical_cv":
                frame_metrics[fr.index] = dict(getattr(d, "last_metrics", {}))
        if cfg.verbose and i % 25 == 0:
            log.info("frame %d/%d, %d detections so far", i + 1, len(frames), len(detections))
    # 3b. optional VLM checklist pass (live API, or cached / reviewed JSON per frame)
    vlm_used = False
    if cfg.perception.vlm_cache_dir:
        from .vlm.claude_vision import vlm_to_detections, vlm_to_metrics
        import json as _json
        cdir = Path(cfg.perception.vlm_cache_dir)
        for fr in frames:
            jp = cdir / (Path(fr.path).stem + ".json")
            if jp.exists():
                try:
                    j = _json.loads(jp.read_text())
                except Exception:
                    continue
                vlm_used = True
                detections.extend(vlm_to_detections(fr, j, fw, fh))
                frame_metrics.setdefault(fr.index, {}).update(vlm_to_metrics(j))
                frame_metrics[fr.index]["vlm_raw"] = j
        log.info("VLM cache: %d frame checklists loaded", sum(1 for fr in frames if (cdir / (Path(fr.path).stem + ".json")).exists()))
    if cfg.perception.use_vlm and not vlm_used:
        try:
            from .vlm.claude_vision import ClaudeVisionAuditor, vlm_to_detections, vlm_to_metrics
            vlm = ClaudeVisionAuditor(model=cfg.perception.vlm_model)
            step = max(1, len(frames) // cfg.perception.vlm_max_frames)
            picked = frames[::step][: cfg.perception.vlm_max_frames]
            for fr in picked:
                j = vlm.assess_frame(fr, cfg.road_class.value)
                if not j:
                    continue
                vlm_used = True
                detections.extend(vlm_to_detections(fr, j, fw, fh))
                frame_metrics.setdefault(fr.index, {}).update(vlm_to_metrics(j))
                frame_metrics[fr.index]["vlm_raw"] = j
        except Exception as e:
            log.warning("VLM pass unavailable: %s", e)
    # 4. fusion + road model
    frames_by = {f.index: f for f in frames}
    from .perception.fusion import set_frame_half_widths
    set_frame_half_widths(frame_metrics)
    if cfg.survey_mode == "walk":
        for d in detections:
            if d.asset.value == "pothole" and d.bbox is not None and "where" not in d.attributes:
                # on a footpath walk the central field of view is the footpath; the carriageway is off to one side
                d.attributes["where"] = "footpath" if 0.15 * fw <= d.bbox.cx <= 0.85 * fw else "carriageway"
    chs = [f.chainage_m for f in frames if f.chainage_m is not None]
    assets = fuse(detections, frames_by, cam, max_chainage=(max(chs) if chs else None))
    moving = count_moving_per_frame(detections)
    ctx = dict(context or {})
    ctx["capabilities"] = detectable_assets(names, vlm_used)
    ctx["survey_mode"] = cfg.survey_mode
    # VLM per-frame metrics are stored with vlm_ prefix; expose footpath metrics under the names rules expect
    for k, m in frame_metrics.items():
        for src_k, dst_k in (("vlm_footpath_present", "vlm_footpath_present"),):
            pass
    rm = build_road_model(media, frames, track, cam, detections, assets, frame_metrics, moving, cfg.road_class, cfg.terrain,
                          cfg.design_speed_kmph, cfg.posted_speed_kmph, cfg.sampling.segment_length_m, ctx)
    _promote_vlm_metrics(rm)
    # 5. rules + scoring
    engine = RuleEngine()
    findings, compliance = engine.evaluate(rm)
    from .rules.engine import evaluate_checklist
    checklist = evaluate_checklist(compliance)
    summary = summarise(rm, findings, compliance)
    # 6. report
    positioning = (f"GPS track with {len(track)} fixes; chainage from cumulative haversine distance" if len(track) >= 2
                   else f"No GPS track: chainage estimated from time x assumed speed {ctx.get('assumed_speed_kmph', 30)} km/h (relative only)")
    methodology = {
        "positioning": positioning,
        "camera": f"HFOV {cam.hfov_deg:.1f} deg ({cam.source}), height {cam.height_m:.2f} m, pitch {cam.pitch_deg:.1f} deg; inverse perspective mapping on flat-road assumption",
        "detectors": names + (["claude_vision_checklist"] if vlm_used else []),
        "sampling": f"{len(frames)} frames at {cfg.sampling.frame_interval_s}s; {cfg.sampling.segment_length_m:.0f} m segments",
        "standards": STANDARDS,
        "rules_evaluated": len(engine.rules),
        "runtime_s": round(time.time() - t0, 1),
        "tool": f"CFI Road Auditor v{__version__}",
    }
    limitations = _limitations(rm, cam, names, vlm_used, len(track))
    if cfg.survey_mode == "walk":
        limitations.insert(1, "Walking survey: the camera is on the footpath, so carriageway geometry (lane width, markings, curve radius) is not measured; the surface width under the camera is reported as footpath width and surface defects as footpath defects. Carriageway-side items are assessed only where the camera sees them.")
        methodology["survey_mode"] = "walk (eye-level camera on the footpath)"
    else:
        methodology["survey_mode"] = "drive (vehicle-mounted camera)"
    report = build_report(rm, findings, compliance, summary, cfg.title, methodology, limitations)
    report.checklist = checklist
    from collections import Counter
    report.summary.checklist_counts = dict(Counter(c.status for c in checklist))
    write_all_outputs(report, str(out_dir), cfg.sampling.segment_length_m)
    log.info("done in %.1fs: %d findings, score %.1f, outputs %s", time.time() - t0, len(findings), summary.overall_score, list(report.outputs))
    return report


def _manifest_key(cfg, media) -> Dict:
    return {"media": os.path.abspath(media.path), "size": os.path.getsize(media.path) if os.path.exists(media.path) else 0,
            "interval_s": cfg.sampling.frame_interval_s, "max_frames": cfg.sampling.max_frames, "resize": cfg.sampling.resize_long_edge}


def _load_frame_manifest(cfg, media) -> Optional[List[FrameRef]]:
    """Reuse frames extracted by an earlier run (same media + sampling), from this out_dir or cfg.sampling.reuse_frames_dir."""
    import json as _json
    for d in [cfg.sampling.reuse_frames_dir, str(Path(cfg.out_dir) / "frames")]:
        if not d:
            continue
        mp = Path(d) / "manifest.json"
        if not mp.exists():
            continue
        try:
            m = _json.loads(mp.read_text())
        except Exception:
            continue
        if m.get("key") != _manifest_key(cfg, media):
            continue
        frames = [FrameRef(**f) for f in m.get("frames", [])]
        if frames and all(os.path.exists(f.path) for f in frames):
            log.info("reusing %d extracted frames from %s", len(frames), d)
            return frames
    return None


def _save_frame_manifest(frames_dir, cfg, media, frames) -> None:
    import json as _json
    try:
        Path(frames_dir).mkdir(parents=True, exist_ok=True)
        (Path(frames_dir) / "manifest.json").write_text(_json.dumps({"key": _manifest_key(cfg, media),
            "frames": [f.model_dump(exclude={"geo", "chainage_m"}) for f in frames]}))
    except Exception as e:  # pragma: no cover
        log.warning("could not save frame manifest: %s", e)


def calibrate_height_from_zebra(frames, cam, cfg, max_frames: int = 40):
    """Scale calibration: a zebra crossing's stripe period is 1.0 m (IRC:35). If zebras are seen in the subsample,
    the median period fixes the camera height (all IPM ground distances scale linearly with it)."""
    if getattr(cfg.camera, "height_locked", False):
        return cam
    from .perception.classical import ClassicalDetector
    det = ClassicalDetector(cam, enable_potholes=False)
    step = max(1, len(frames) // max_frames)
    hints = []
    for fr in frames[::step][:max_frames]:
        img = cv2.imread(fr.path)
        if img is None:
            continue
        try:
            det.detect(img, fr, cam)
        except Exception:
            continue
        if det.last_scale_hint and 0.6 < det.last_scale_hint < 1.6:
            hints.append(det.last_scale_hint)
    if len(hints) >= 1:
        k = float(np.median(hints))
        new_h = float(np.clip(cam.height_m * k, 0.8, 2.5))
        log.info("height calibrated from %d zebra observation(s): %.2f -> %.2f m", len(hints), cam.height_m, new_h)
        return cam.model_copy(update={"height_m": new_h, "source": cam.source + "+zebra_scale", "confidence": min(0.95, cam.confidence + 0.2)})
    return cam


def _promote_vlm_metrics(rm) -> None:
    """Segment metrics named footpath_present etc. come from the VLM pass (measurements named without vlm_ prefix)."""
    for seg in rm.segments:
        for k in list(seg.metrics):
            if k.endswith("_vlm_m") or k.endswith("_vlm"):
                base = k.replace("_vlm_m", "_m").replace("_vlm", "")
                seg.metrics.setdefault(base, seg.metrics[k])
        if "footpath_present" in seg.metrics:
            seg.flags["footpath_assessed"] = True
            seg.flags["has_footpath"] = seg.metrics["footpath_present"] > 0.5
        if rm.context.get("survey_mode") == "walk":
            seg.flags["walk_mode"] = True
        if "pedestrians_on_carriageway" in seg.metrics and "pedestrian_per_frame" not in seg.metrics:
            seg.metrics["pedestrian_per_frame"] = seg.metrics["pedestrians_on_carriageway"]
        if "intersection_present" in seg.metrics and seg.metrics["intersection_present"] > 0.5:
            seg.flags["is_intersection"] = True


def _limitations(rm, cam, names, vlm_used, n_track) -> List[str]:
    lim = [
        "Automated Stage-5 (existing road) screening audit; a certified auditor must validate findings before issue (IRC:SP:88-2019 Cl. 3).",
        "Measurements use monocular inverse perspective mapping (flat-road assumption, camera height %.2f m, pitch %.1f deg): lateral accuracy approx. +/-0.15 m within 20 m; longitudinal +/-10%%." % (cam.height_m, cam.pitch_deg),
    ]
    if n_track < 2:
        lim.append("No GPS track supplied: chainages are relative (time x assumed speed) and findings are not geo-referenced. Record a GPX/SRT track or use a camera with embedded GPS.")
    else:
        lim.append("GPS positions carry +/-3-5 m consumer-grade error; curve radii above ~1500 m and gradients below ~2% are not resolvable.")
    if not any("damage" in n for n in names):
        lim.append("No road-damage detector weights loaded: potholes come from the classical texture/contrast detector (lower precision) - install RDD2022-trained weights in data/models/ for cracks and higher pothole recall.")
    if not any("sign" in n for n in names) and not vlm_used:
        lim.append("Sign inventory based on colour/shape heuristics and COCO stop-sign class only; sign text, legibility and mounting height need the Claude vision pass (--vlm) or a traffic-sign model.")
    if not vlm_used:
        lim.append("Footpath presence/width, encroachment, barrier condition, drainage and school/work-zone context were not assessed (require --vlm). These checklist items are reported as 'not assessed'.")
    lim.append("Night-time lighting adequacy is inferred from image luminance, not measured illuminance (lux); use a lux meter for IS 1944 compliance.")
    lim.append("Coverage is limited to what the camera saw: a missing sign may exist outside the field of view - items tagged needs_field_verification require site confirmation.")
    return lim
