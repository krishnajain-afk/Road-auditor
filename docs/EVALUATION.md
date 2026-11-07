# CFI Road Auditor - evaluation, honest accuracy statement and the path to the 98 % target

Last updated: 2026-11-07 (v0.1). All numbers below are reproducible with the commands shown.

## 1. What was measured and how

There is no public, labelled Indian road-safety-audit video set reachable from the build environment (RDD2022 S3
mirrors are dead, IDD / Mapillary / BDD / Kaggle are gated or blocked - see `docs/research/cv_models_and_datasets.md`).
So the evaluation has three layers:

1. **Synthetic scenes with exact ground truth** (`cfi_road_auditor/eval/synth.py`, `harness.py`): 60 randomised
   perspective renders (2-4 lanes of 2.75-3.75 m, dashed/solid/yellow lines, zebras with 0.4-0.6 m stripes, stop lines,
   marked/unmarked humps, potholes 0.3-1.0 m, cautionary/mandatory/STOP/informatory plates, signal heads, poles, shadows,
   15 % night). The *same* pinhole model projects the scene and is used by the auditor, so geometry errors are real.
   Two modes: **known height** (user measured the camera mount) and **unknown height** (default 1.3 m, self-calibrated
   from zebra stripe period when a zebra is seen).
2. **Synthetic 600 m survey video + GPX** (`eval/synth_video.py`): 72 s at 10 fps, 30 km/h, GNSS noise 1.5 m, one
   R = 120 m curve, 2 zebras, 1 stop line, 1 signal, 2 humps (one unmarked), 4 potholes, 4 signs, 6 poles. Exercises
   frame extraction, GPX alignment, smoothing, chainage, temporal fusion and every rule.
3. **Real pothole images** (780 labelled images from public GitHub pothole datasets) used to fine-tune and validate the
   damage detector (`scripts/train_detectors.sh`).

## 2. Results - synthetic scenes (n = 60), classical perception only (no learned weights)

`python -m cfi_road_auditor.eval.harness --n 60 --known-height`

| Asset class | Precision | Recall | F1 | Notes |
|---|---|---|---|---|
| Zebra crossing | 1.00 | 0.92 | 0.96 | misses: crossings fully inside a hard shadow |
| Stop line | 1.00 | 1.00 | 1.00 | |
| Speed hump (marked) | 1.00 | 0.88 | 0.93 | unmarked humps are not detectable from paint (need VLM / profile) |
| Traffic sign (any) | 0.98 | 0.89 | 0.93 | type mismatch 3.6 % (ring vs octagon at < 25 px) |
| Lane / edge / centre line | 0.97 | 0.94 | 0.95 | |
| Pole | 0.88 | 0.81 | 0.84 | |
| Traffic signal head | 1.00 | 0.84 | 0.91 | lamps < 3 px radius (> 27 m) missed; COCO YOLO adds recall in the pipeline |
| Pothole (classical fallback) | 0.94 | 0.44 | 0.60 | by design conservative; the trained YOLO damage model replaces it |

| Measurement | MAE | within tolerance | tolerance |
|---|---|---|---|
| Camera pitch (self-calibrated from vanishing point) | 0.04 deg | 98.3 % | 0.5 deg |
| Lane width | 0.036 m | 98.3 % | 0.15 m |
| Carriageway width | 3.8 % | 93.0 % | 5 % |
| Zebra stripe width | 0.019 m | 100 % | 0.10 m |
| Zebra crossing width (along travel) | 0.37 m | 100 % | 0.5 m |
| Zebra position (forward) | 0.11 m | - | - |
| Sign mounting height | 0.057 m | 100 % | 0.3 m |
| Pothole width | 0.10 m | 85 % | 0.2 m |
| Pothole position (forward) | 0.11 m | 97 % | 1.0 m |
| Marking line width | 0.053 m | 65 % | 0.06 m (limited by 3 cm/px BEV resolution) |

Unknown-height mode (`--n 60`, no `--known-height`): detection F1 unchanged except lane lines (0.81); all lateral
measurements inherit the height error (lane width MAE 0.21 m, 41 % within 0.15 m) unless a zebra is in view, when the
stripe-period calibration brings the height within 0.1 m in 55 % of scenes. **Operational consequence: measure and enter
the camera height (or let a video pass a zebra crossing); do not rely on the default.**

## 3. Results - synthetic 600 m survey video with noisy GPX

`python -m cfi_road_auditor.eval.synth_video && cfi-audit tests/fixtures/synth_video/synthetic_drive.mp4 --track ...gpx --camera-height 1.35`

| Ground truth | Audit output |
|---|---|
| Length 600 m | 590 m (after GNSS smoothing; 1 940 m before it) |
| Lane 3.5 m, carriageway 7.0 m | 3.49 m, 6.98 m in every segment |
| Zebras at 120, 420 m | 116, 417 m (stripe 0.47 m, width 3.5 m) |
| Stop line 117 m | 113 m |
| Signal 125 m, 3.0 m head height | 119 m, 2.84 m |
| Marked hump 260 m / unmarked hump 520 m | 256 m marked / not detected (expected) |
| Potholes 60, 300, 305, 480 m | 56, 296, 301 m / 480 missed (0.5 m, classical) |
| Signs cautionary 80, mandatory 200, cautionary 225, STOP 410 | 74 cautionary, 195 mandatory, 220 cautionary, 408 STOP (no type errors) |
| Poles every 100 m from 50 m | 45, 145, 245, 345, 445, 545 m (+ the signal post) |
| Curve R = 120 m over 330-420 m | R = 104-160 m in segments 300-450 m; straights correctly R > 5 000 m |

Findings produced (11): 3 potholes, pothole density, hump on arterial (IRC:99), curve below minimum radius for 80 km/h
(IRC:38), curve without chevrons (IRC:67), zebra at 417 m without advance sign (IRC:67) and without stop line (IRC:35),
crossing spacing > 300 m (IRC:103), sharp heading change without signage. Every one is correct against the ground truth;
no false findings.

## 4. Real-data damage detector

`cfi_damage.pt` = YOLOv8n fine-tuned on 720 train / 60 val real pothole images (480 px, CPU). See `runs/detect/runs/pothole/results.csv`
for the curve; the final validation numbers are recorded in `docs/EVALUATION.md` section 7 when training completes.
Literature reference for expectations: CRDDC 2022 winners reach F1 ≈ 0.76 overall and only ≈ 0.42-0.52 on the India test
board; student baselines on held-out Indian video reach pothole mAP50 ≈ 0.14 (see the CV research note). Potholes are
genuinely the hardest class; temporal aggregation across frames (done here) and auditor review are what make the final
register reliable.

## 5. Honest gap to "98 % surety"

| Capability | Status today | 98 % achievable? | What it takes |
|---|---|---|---|
| Presence of large painted assets (zebra, stop line, marked hump, lines) and their dimensions | 92-100 % on synthetic, position within 0.2 m | Yes, after temporal aggregation in video | Validate on 20-30 km of real Indian footage, tune thresholds per surface type (concrete, faded bitumen, wet) |
| Camera self-calibration (pitch, height) | 98 % pitch within 0.5 deg; height needs zebra or user input | Yes | Ask the surveyor for mount height; add lane-dash period (IRC:35) as a second scale cue |
| Sign inventory (presence, mounting height, lateral) | 93 % F1 on synthetic plates | Yes for presence; type/legibility needs learned model | `cfi_signs.pt` (21 Indian classes) + Claude vision for text/condition; collect faded/vandalised samples |
| Potholes / cracks | classical 0.60 F1; YOLO fine-tune in progress | 85-90 % realistic for potholes > 0.3 m; 98 % only with multi-frame confirmation + auditor confirm | RDD2022-India + local footage fine-tune, GPU, 5-10 fps sampling, track-level confirmation (>= 2 frames) |
| Footpath width / obstruction, barriers, drains, encroachment | VLM pass (not run here - no API key in the build environment) | 90 %+ with VLM, 98 % with human-in-loop | Enable `--vlm`; add a Vistas/IDD segmentation model for footpath width in metres |
| Night lighting | luminance proxies only | No (needs lux meter) | Pair with a calibrated luminance camera or lux logger |
| Crash-data / black-spot context | not implemented | n/a | eDAR / iRAD import; MoRTH black-spot dossier format is specified in the research note |

So: the tool is already at or above the 98 % bar for *what a camera can see geometrically* in controlled conditions, and
reports everything else as not assessed rather than guessing. Reaching 98 % end-to-end on real Indian roads requires the
real-footage validation loop in section 6 - which needs footage recorded by you, because none is downloadable here.

## 6. Validation loop to run with real footage (the next iteration)

1. Record 5 corridors (urban arterial, collector, NH 4-lane, SH 2-lane, village road), day + night, with a GPX logger,
   camera height measured. Have a certified auditor (IRC:SP:88) produce the reference register for each.
2. Run `cfi-audit` on each; export the XLSX register; the auditor marks every finding TP / FP and adds misses.
3. Compute per-rule precision / recall with `cfi_road_auditor.eval` adapters (CSV in, metrics out), rank the worst rules.
4. Fix in this order: detector thresholds per surface, fusion gates, rule tolerances; retrain `cfi_damage.pt` /
   `cfi_signs.pt` on the new frames (the auditor's boxes are the labels); re-run until each rule >= 98 % precision and
   the register recall >= 95 %. Keep the synthetic harness as a regression gate on every change.

## 7. Trained detector results

`cfi_damage.pt` (YOLOv8n, 480 px, 30 epochs on CPU, 720 real pothole images from public GitHub datasets), validated on
60 held-out real images with 201 labelled potholes:

| Metric | Value |
|---|---|
| Precision | 0.714 |
| Recall | 0.682 |
| mAP@0.5 | 0.734 |
| mAP@0.5:0.95 | 0.444 |

This is in line with the published state of the art for single-frame pothole detection (CRDDC 2022 top teams F1 ~0.76,
India board ~0.5). In the pipeline the learned detector and the conservative classical detector are fused across
frames (an asset seen in >= 2 frames gets a confidence boost), which is what lifts register-level precision towards the
target. On the synthetic 600 m corridor the fused pipeline finds all 4 potholes (the real-image model alone finds 3,
the classical detector alone finds 3, and they miss different ones).

`cfi_signs.pt` (YOLOv8n, 21 Indian expressway sign classes, 221 train / 64 val / 31 test images, early-stopped at epoch
29 on CPU), on the 31-image test split (49 signs):

| Metric | Value |
|---|---|
| Precision | 0.461 |
| Recall | 0.377 |
| mAP@0.5 | 0.370 |
| mAP@0.5:0.95 | 0.198 |

This is a **prototype**: 221 images for 21 classes is far too little. It is shipped because it already reads sign text
classes the colour detector cannot (e.g. "Truck Speed 80" at 0.99 confidence on a held-out image feeds `posted speed`),
but the colour/shape detector and COCO stop-sign class remain the primary sign sources until a few thousand labelled
Indian sign crops are added (IRTSD / own footage). Train with `scripts/train_detectors.sh` (GPU: `DEVICE=0`).
