# CFI Road Auditor - user guide (auditors, engineers, authorities, citizens)

## 1. Who uses it and what they get

| User | What they need | Where it is in the output |
|---|---|---|
| Certified Road Safety Auditor (IRC:SP:88) | Draft findings register with chainage, standard clause, risk, evidence, to review and sign | `audit_register.xlsx` (Findings sheet with client-response / action / closure columns), finding sheets in PDF/HTML |
| ULB / PWD executive engineer | What to fix, where, by whom, how urgently; a work order list | PDF sections 3 and 8 (action plan by priority), XLSX, KML for field teams |
| NHAI project director / independent engineer | Compliance with IRC/MoRTH on a concession stretch; defect liability evidence | Compliance matrix, IRC:SP:88 checklist roll-up, GeoJSON for the project GIS |
| Traffic police (DCP Traffic) | Signals, signs, markings, crossings, speed, encroachment | Findings filtered by category (signs, markings, intersection, parking, speed) |
| Urban planner / Smart City SPV | Corridor-level scores, VRU exposure, crossing spacing | Segment summary, star bands by road user, GeoJSON |
| CAD / design consultant | Strip plan to overlay on drawings | `audit_strip_plan.dxf` (metres, local ENU, layers per asset / severity) |
| District Road Safety Committee / court committee | Black-spot style dossier, agency-wise action table | PDF executive summary + action plan; XLSX per agency pivot |
| Citizen / NGO | Simple evidence of a hazard with the rule it breaks | HTML report, evidence JPEGs, KML to share |

## 2. Capturing a survey

1. **Camera**: any phone or action camera. 1080p / 30 fps, landscape. Dash-mount at the windscreen centre so the
   bonnet is out of frame. Measure lens height above the road (tape measure; typically 1.2-1.5 m) and note it.
2. **Position**: run a GPS logger that writes GPX at 1 Hz or better (phone apps: GPS Logger, Open GPX Tracker, Strava
   export; DJI Osmo Action writes a `.SRT` next to the video which is read automatically). Keep the phone clock synced.
3. **Drive**: 20-40 km/h in the kerb-side lane, both directions, once by day and once after dark. Stop at nothing; the
   tool handles stationary periods. For junctions, additionally walk each arm and take photos (audited one by one).
4. **Upload**: web UI (`/`) or CLI. Choose the road class (this selects the IRC thresholds), terrain, posted speed, and
   enter the camera height and tick "height locked" if you measured it.

## 3. Reading the report

* **Safety score / star band** are indicative screening numbers, not an official iRAP rating.
* **Findings register**: ID `CFI-RSA-<km>+<m>-<CAT>-<n>`; severity (critical/high/medium/low) x likelihood -> risk score
  16/10/5/2 -> priority *Essential / Highly Desirable / Desirable / Optional* with indicative time-frames, following
  IRC:SP:88-2019 (Austroads matrix). *Confidence* is the tool's confidence in the observation; tags
  `needs_field_verification` and `low_confidence_detection` must be checked on site before issuing.
* **Compliance matrix** lists every rule with *compliant / non-compliant / not assessed / not applicable*. "Not assessed"
  means the media could not support the check (e.g. footpath width without the vision-language pass) - never a pass.
* **IRC:SP:88 checklist**: the 66 Stage-5 questions rolled up from the rules, with *manual* items the auditor must do
  (crash records, skid resistance, signal phasing, sight triangles).
* **Asset inventory / segments**: everything detected with chainage, side, size and confidence; per-50 m metrics.
* **Evidence**: annotated frames per finding; GeoJSON/KML pins for field verification.

## 4. From draft to issued audit (recommended workflow)

1. Auditor imports `audit_register.xlsx`, verifies each finding on site or from the evidence, fills *client_response*
   (accept / modify / reject with reason) - this is the IRC:SP:88 response report.
2. Authority assigns *action_taken* and *closure_date*; re-survey after works and re-run to confirm closure.
3. Keep the JSON export as the machine record (every measurement, rule version and camera calibration is inside).

## 5. Limits you must know

* Monocular geometry assumes a flat road: lateral measurements are good to about +/-0.15 m within 20 m when the camera
  height is right; wrong height scales every width proportionally. The tool self-corrects when it sees a zebra crossing.
* Objects outside the camera's field of view do not exist for the tool: a "missing sign" may be on the other side of a
  median or behind a bus. Hence `needs_field_verification`.
* Potholes and cracks need the trained damage detector (`cfi_damage.pt`) for good recall; the built-in classical
  detector is deliberately conservative (few false alarms, misses small potholes).
* Night audits: lighting is judged from image brightness and uniformity, not measured lux; signs' retro-reflectivity is
  not measured.
* Footpath width, obstruction, barrier damage, encroachment, drains and sign legibility require the Claude vision pass
  (`--vlm`, needs an API key) or a segmentation model; otherwise they are reported as not assessed.
* The tool does not replace the certified auditor's judgement, the crash-data review or the authority's design
  responsibility under MV (Amendment) Act 2019 s.198A.
