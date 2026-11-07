# CFI Road Auditor

Automated **Road Safety Audit (RSA)** for Indian roads. Upload a phone / dash-cam / action-cam video (or a photo) with an
optional GPS track and get an IRC:SP:88-2019 Stage-5 (existing road) style audit: a findings register with chainage,
severity, risk score and IRC clause references, an IRC/MoRTH compliance matrix, the 66-item IRC:SP:88 checklist roll-up,
evidence frames, and exports for every stakeholder (PDF, HTML, Excel, CSV, GeoJSON, KML, AutoCAD DXF, JSON).

> Status: v0.1 - working end-to-end pipeline with a validated evaluation harness. It is a **screening tool that supports a
> certified Road Safety Auditor**; it does not replace the site visit, crash-data review and professional judgement that
> IRC:SP:88 requires. See [docs/EVALUATION.md](docs/EVALUATION.md) for measured accuracy and the honest gap to the
> "98 %" target.

## What it checks

62 rules across 17 categories, each tied to an Indian standard clause (IRC:35 markings, IRC:67 signs, IRC:103 pedestrian
facilities, IRC:86 / IRC:73 geometric design, IRC:99 traffic calming, IRC:93 signals, IRC:38 curves, IRC:SP:41 junctions,
IRC:82 pavement condition, IRC:119 barriers, IRC:SP:55 work zones, IRC:80 bus bays, IRC:SP:12 parking, IS 1944 lighting,
MoRTH 2018 speed limits, MV Act 2019 s.198A). The rule database is a YAML file you can extend:
`cfi_road_auditor/rules/data/irc_rules.yaml`. The IRC:SP:88 Stage-5 checklist mapping is in
`cfi_road_auditor/rules/data/irc_sp88_checklist.yaml`.

Measured / detected from the media: lane and carriageway width, horizontal curve radius and gradient (from GPS),
lane/edge/centre lines and their widths, zebra crossings (stripe width, period, crossing width), stop lines, speed humps
and their markings, potholes (size, position), traffic signs (type, mounting height, lateral clearance, range), traffic
signals (mounting height), poles / clear-zone offsets, pedestrians, cyclists, two-wheelers, cars, buses, trucks and
animals as exposure per segment, night-time luminance and uniformity. With the optional Claude vision pass
(`--vlm`), semantic checklist items are assessed too: footpath presence/width/obstruction, kerb height, sign condition
and text, barrier condition, encroachment, drains, school/work zones, signal working state, median openings.

Everything the media does **not** allow the tool to assess is reported as *not assessed*, never silently passed.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[ml,api,vlm,dev]"
# weights (optional but recommended): put yolov8s.pt / yolo11s.pt (COCO) and cfi_damage.pt / cfi_signs.pt in data/models/
cfi-audit survey.mp4 --track survey.gpx --road-class urban_arterial --posted-speed 50 \
          --camera-height 1.3 --title "MG Road RSA" --location "Pune" --out outputs/mg_road
```

Outputs land in `outputs/mg_road/`: `audit_report.pdf`, `audit_report.html`, `audit_register.xlsx`, `audit_findings.csv`,
`audit_findings.geojson`, `audit_findings.kml`, `audit_strip_plan.dxf`, `audit_report.json`, `evidence/*.jpg`.

Web UI / API:

```bash
uvicorn cfi_road_auditor.api.app:app --host 0.0.0.0 --port 8000     # open http://localhost:8000
```

`POST /api/audits` (multipart: media, track, road_class, ...) -> `{job_id}`; `GET /api/audits/{job_id}`;
`GET /api/audits/{job_id}/download/{pdf|html|xlsx|csv|geojson|kml|dxf|json}`; `GET /api/rules`.

## Recording guidance (what makes the audit accurate)

* Mount the phone at the windscreen centre, lens ~1.3 m above the road, level (the tool self-calibrates pitch from the
  vanishing point and scale from zebra stripes, but a measured height - `--camera-height` + "height locked" - is better).
* 1080p, 30 fps, horizontal. Keep the lens clean; avoid the bonnet in frame.
* Run a GPS logger (GPX, 1 Hz or better) or use a camera with embedded GPS (DJI SRT sidecar is parsed automatically;
  iPhone videos carry only one fix, Android none - so log separately). The GPX clock must be the phone clock.
* Drive 20-40 km/h in the slow lane, both directions, once by day and once at night (IRC:SP:88 requires a night audit).
* For junction audits, also walk the junction and photograph each arm; photos are accepted and audited individually.

## Architecture

```
media (video/photo) ─ ingest/media.py ─► frames (1 s or 5 m spacing, luma/night flag)
GPS (GPX/CSV/SRT/NMEA/QuickTime/GPMF) ─ ingest/gps.py ─► smoothed track ─► chainage, speed, curvature, gradient
frames ─► geometry/camera.py (intrinsics from EXIF/device table, pitch from vanishing point, scale from zebra) ─► IPM
       ─► perception/  yolo.py (COCO + damage + sign weights) | classical.py (BEV markings, potholes, signs, signals,
                       poles, lighting) | vlm/claude_vision.py (checklist JSON per key frame)
       ─► perception/fusion.py (ground projection, chainage clustering, de-duplication) ─► Assets
       ─► roadmodel.py (50 m segments: metrics, counts, flags) ─► RoadModel
       ─► rules/engine.py (irc_rules.yaml) ─► Findings + compliance matrix ─► IRC:SP:88 checklist roll-up
       ─► scoring/risk.py (IRC:SP:88 / Austroads 4x4 matrix, priorities, indicative star bands)
       ─► report/ (PDF, HTML, XLSX, CSV, GeoJSON, KML, DXF, JSON, annotated evidence)
```

Detailed design notes: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Research knowledge bases that drive the rules:
[docs/research/irc_standards_kb.md](docs/research/irc_standards_kb.md) (≈490 numeric thresholds with clause references
and confidence grades), [docs/research/auditor_workflow_and_personas.md](docs/research/auditor_workflow_and_personas.md)
(how auditors work, risk matrices, report spec, personas, competitors, legal hooks),
[docs/research/cv_models_and_datasets.md](docs/research/cv_models_and_datasets.md) (models, datasets, sensor ingest,
accuracy benchmarks).

## Evaluation

`python -m cfi_road_auditor.eval.harness --n 60 --known-height` renders synthetic scenes with exact ground truth
and reports precision / recall per asset class and measurement errors; `python -m cfi_road_auditor.eval.synth_video`
builds a 600 m corridor video + GPX for end-to-end tests. Results and the real-data plan are in
[docs/EVALUATION.md](docs/EVALUATION.md).

## Training your own detectors

`scripts/train_detectors.sh` fine-tunes YOLOv8n for potholes (`data/datasets/pothole`) and Indian traffic signs
(`data/datasets/itsd`) and drops `cfi_damage.pt` / `cfi_signs.pt` into `data/models/`, where the registry picks them up
automatically. Any RDD2022-style weights (classes D00/D10/D20/D40) named `rdd_*.pt` are also recognised.

## Licence notes

Ultralytics YOLO weights/code are AGPL-3.0 (commercial licence needed for a closed networked product); YOLOP (MIT),
YOLOX / NanoDet / EfficientDet-Lite (Apache-2.0) are permissive alternatives documented in the CV research note.
