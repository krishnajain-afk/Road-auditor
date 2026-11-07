# CFI Road Auditor - architecture and design notes

## 1. Goals
1. Turn ordinary survey media (phone / dash-cam / action-cam / smart-glasses video, photos, optional GPS track) into an
   IRC:SP:88-2019 Stage-5 (existing road) Road Safety Audit that a certified auditor can review, edit and sign.
2. Every finding cites the governing Indian standard clause, states the requirement, the observation (with a measurement
   where possible), a risk rating from the IRC:SP:88 / Austroads matrix, a priority, the responsible agency, the affected
   road users and an evidence frame.
3. Never fake coverage: checklist items that the media cannot support are reported as *not assessed* / *manual*.
4. Degrade gracefully: works with no learned weights (classical CV), gets better with COCO / damage / sign YOLO weights,
   and best with the Claude vision checklist pass.

## 2. Data model (`schemas.py`)
`MediaMeta -> FrameRef[] -> Detection[] -> Asset[]` (de-duplicated, chainage-referenced physical objects and defects),
`Measurement[]` (metric quantities with method and confidence), `Segment[]` (homogeneous 50 m sections with aggregated
metrics / counts / flags), `RoadModel` (the digital twin), `Finding[]` + `ComplianceItem[]` + `ChecklistItem[]` +
`AuditSummary` -> `AuditReport`. Everything is pydantic v2 and serialises to the JSON export unchanged.

Finding ID: `CFI-RSA-<km>+<mmm>-<CAT>-<nn>` (chainage-ordered, category code per the auditor-report spec).

## 3. Ingest (`ingest/`)
* `media.py` - ffprobe metadata (device, rotation, creation time, embedded GPS tags, data/subtitle streams), OpenCV
  frame extraction at fixed time spacing (distance spacing when a track exists), long-edge resize, mean luma -> night flag,
  EXIF for photos (make/model/focal/GPS).
* `gps.py` - GPX / CSV / DJI SRT / NMEA / JSON / QuickTime ISO-6709 / GoPro GPMF (optional dep) -> `GeoPoint[]` with
  `t` relative to media start (absolute GPX times aligned to `creation_time`). `smooth_track()` removes consumer-GNSS
  jitter (centred moving average over 4 s + stationary-point suppression) before chainage integration - without it raw
  1-10 Hz fixes inflate chainage 2-3x and create fake curves. Speed, heading, cumulative chainage, frame interpolation.

## 4. Geometry (`geometry/`)
* `camera.py` - pinhole model; HFOV from EXIF 35 mm focal, device table or default 70 deg; `IPM` (inverse perspective
  mapping) pixel<->ground on the flat-road assumption; bird's-eye warp at 32 px/m; `estimate_vanishing_point()` (Hough +
  weighted intersection voting) -> pitch/yaw self-calibration; `height_above_ground()` (sign / signal mounting height from
  range); `range_from_width()` (sign plate 0.75 m, signal head 0.35 m). Camera height = user value, refined by zebra
  stripe period (IRC:35: 1.0 m) unless `height_locked`.
* `road.py` - IRC design-speed table (IRC:73 / IRC:86), SSD (IRC:66), minimum radii (IRC:38), Kasa circle fit over a
  60 m sliding window with a heading-change significance test (6 deg) and window-edge guard, gradient from altitude,
  heading-change hotspots (junction / sharp-bend candidates), speed profile.

## 5. Perception (`perception/`)
Tiered backends, all returning `Detection` in pixel space; the registry loads what exists in `data/models/`.
* `classical.py` (always on): exposure normalisation (CLAHE) for night; drivable-surface mask (seeded LAB similarity +
  paint union); carriageway width (outer line spacing, fallback mask probes); lane / edge / centre lines in BEV with
  per-row width, dashed/continuous, colour, exclusion of transverse-marking rows; zebra (lateral periodicity ~1.0 m,
  >= 3 regular stripes, stripe width, crossing length); stop line; hump / rumble bands (alternating bars with painted
  black gaps, zebra exclusion); painted kerbs; potholes (local relative darkness on a paint- and kerb-neutral reference,
  texture energy, metric size/aspect, island test, border and edge exclusions, transverse-band exclusion); signs by
  colour + mask-fill + shape (ring vs solid vs triangle, lamp and sky rejection) with range, lateral, mounting height;
  signal lamps in dark housings; poles by dark-column runs crossing the horizon with ground contact; night lighting
  metrics (road luma, uniformity, point sources).
* `yolo.py` - ultralytics adapter with three roles: `general` (COCO -> road users, traffic lights, stop signs, animals),
  `damage` (RDD2022-style D00/D10/D20/D40 or `cfi_damage.pt`), `sign` (`cfi_signs.pt`, Indian sign classes).
* `vlm/claude_vision.py` - Claude vision with a strict JSON checklist schema per key frame (footpath, carriageway,
  markings, signs, signals, calming, roadside, context, hazards, counts). Converted to Detections (source=VLM) and to
  per-frame metrics (`vlm_*`) that the road model promotes to segment metrics.
* `fusion.py` - ground projection (`localise`), class-specific chainage gates, side agreement, confidence = 1 - prod(1-c)
  with multi-frame boost, attribute medians, cross-label sign de-duplication, moving-object counts per frame.

## 6. Road model (`roadmodel.py`)
Measurements -> 50 m segments: lane width (25th percentile, conservative), carriageway width (median), sharpest curve,
steepest grade, night flag, exposure (road users per frame), asset counts, junction flags (signal / stop line / VLM /
GPS heading change).

## 7. Rules (`rules/`)
`irc_rules.yaml` - 62 rules; check types: `asset_conf`, `asset_attr` (with tolerances), `asset_size`, `asset_presence`,
`asset_requires` (upstream/downstream windows, e.g. hump needs sign within 120 m), `asset_requires_metric`,
`asset_forbidden_near`, `segment_metric` (class-keyed thresholds, named thresholds like `min_radius_for_design_speed`),
`segment_flag`, `segment_requires_asset`, `density`, `spacing`. Capability gating: a rule whose asset class no loaded
backend can emit is *not assessed*. `irc_sp88_checklist.yaml` rolls rules up to the 66 Stage-5 questions
(deficient / satisfactory / partially assessed / not assessed / manual).

## 8. Scoring (`scoring/risk.py`)
IRC:SP:88-2019 adopts the Austroads 4x4 likelihood x consequence matrix -> Intolerable (16) / High (10) / Medium (5) /
Low (2) and priorities Essential / Highly Desirable / Desirable / Optional with time-frames. Safety score 0-100 from
risk density per 100 m; indicative 1-5 star band overall and per road-user group (explicitly *not* an iRAP rating).

## 9. Reports (`report/`)
HTML (Jinja), PDF (reportlab), XLSX (findings register with client-response columns, compliance, IRC:SP:88 checklist,
assets, segments, summary), CSV, GeoJSON + KML (track, findings, assets), DXF R2010 strip plan (centreline, edges from
measured widths, chainage ticks, asset symbols, findings with leaders; local ENU metres with lat/lon origin note),
annotated evidence JPEGs.

## 10. API (`api/app.py`)
FastAPI: `POST /api/audits` (multipart) -> background job; `GET /api/audits/{id}`; downloads per format; `GET /api/rules`;
single-page web UI at `/`.

## 11. Known limitations and roadmap
* Flat-road IPM: lateral error grows with pitch error and road crown; longitudinal ~10 %. Use a measured camera height.
* Classical pothole detector is a fallback (F1 ~0.5 on synthetic); the trained `cfi_damage.pt` or RDD2022 weights should
  be used in production, ideally fine-tuned on local footage; cracks need a damage model.
* Footpath width/obstruction, barrier condition, sign legibility, encroachment and drainage need the VLM pass or a
  segmentation model (Mapillary Vistas / IDD classes) - weights are not pip-installable in restricted networks, see the
  CV research note for mirrors and licences.
* Night audits infer lighting from image luminance, not lux; retro-reflectivity needs a retroreflectometer.
* No crash-data (eDAR/iRAD) fusion yet; the report spec in the research notes defines the black-spot dossier format.
* Production: GPU inference, 5-10 fps sampling, multi-object tracking, both-direction merge, auditor review UI with
  accept/modify/reject per finding (IRC:SP:88 response report), PostGIS storage, authority dashboards.
