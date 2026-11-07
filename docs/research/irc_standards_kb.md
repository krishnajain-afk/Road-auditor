# CFI Road Auditor — Indian Road Design & Safety Standards Knowledge Base

**Purpose:** numeric, citable thresholds for a rule engine that checks phone video/photo evidence against Indian standards (IRC codes, MoRTH circulars/specifications, IS codes, iRAP).

**Compiled:** 2026-11-07. **Method / provenance caveat:** the research session could not open any external document directly (the sandbox network allows only package registries and GitHub; law.resource.org, archive.org, irc.nic.in, morth.gov.in, itdp.in, infralens.in were all unreachable). All values below were assembled from (a) search-engine excerpts of the primary PDFs (law.resource.org / archive.org mirrors of IRC codes, MoRTH circulars, PIB), (b) secondary reproductions (training decks by IIT-Delhi TRIPP, IRF India, PMGSY/NRIDA, Delhi PWD Urban Roads Manual, UTTIPEC, ITDP India), and (c) the compiler's prior knowledge of the codes. Every row carries a confidence grade:

* **high** – value matches primary-text excerpt or multiple independent secondary sources agree.
* **medium** – single secondary source, or well-known textbook value not verified against the current edition.
* **low** – recalled / plausible range only; verify before enforcing as a hard rule (use as "flag for review", not "fail").

Rule-engine guidance: treat **high** rows as hard pass/fail, **medium** as pass/fail with a tolerance band and a "verify" note in the report, **low** as advisory only.

Road-class abbreviations: EXP expressway; NH/SH national/state highway; MDR/ODR major/other district road; VR village road; UA urban arterial; USA urban sub-arterial; UC urban collector; UL urban local street; ALL all classes.

---

## 0. Code index (what governs what)

| Topic | Governing code(s) | Current edition |
|---|---|---|
| Urban road geometry (lane, median, kerb, ROW, speeds, radii, SSD) | IRC:86 | 2018 (supersedes 1983) |
| Rural/non-urban geometry | IRC:73 | 1980 (revision 2023 published; drafts 2020) |
| Two-lane NH with paved shoulders (manual) | IRC:SP:73 | 2018 (2015, 2007 earlier) |
| Four-laning manual | IRC:SP:84 | 2019 |
| Six-laning manual | IRC:SP:87 | 2019 |
| Expressways manual | IRC:SP:99 | 2013 |
| Rural Roads Manual (PMGSY) | IRC:SP:20 | 2002 |
| Pedestrian facilities | IRC:103 | 2012 |
| Road markings | IRC:35 | 2015 |
| Road signs | IRC:67 | 2022 (4th rev.; 2012 widely reproduced) |
| Traffic calming / speed breakers | IRC:99 | 2018 (1988 original) |
| Traffic signals | IRC:93 | 1985 |
| Horizontal curves | IRC:38 | 1988 |
| Vertical curves | IRC:SP:23 | 1983 |
| Sight distance (rural) | IRC:66 | 1976 |
| At-grade intersections | IRC:SP:41 | 1994 |
| Roundabouts | IRC:65 | 2017 (1976 "rotaries" earlier) |
| Grade separators / interchanges | IRC:92 / IRC:SP:90 | 2017 / 2010 |
| Street lighting | IS 1944 (Parts 1&2) 1970 (reaffirmed); SP 72 National Lighting Code 2010; IS 10322 Part 5 Sec 3 | — |
| Crash barriers / roadside safety | IRC:119 ; MoRTH Specifications Sec. 800 (cl. 810) | 2015 ; 5th rev. 2013 |
| Maintenance of bituminous surfaces | IRC:82 | 2015 (2023 revision exists) |
| Surface evenness / roughness | IRC:SP:16 | 2019 |
| Road drainage / urban drainage | IRC:SP:42 / IRC:SP:50 | 2014 / 2013 |
| Bus stops | IRC:80 | 1981 (revision 2020 notified) |
| Parking | IRC:SP:12 | 2015 |
| Work zones | IRC:SP:55 | 2014 (draft 2nd revision 2024) |
| Road safety audit | IRC:SP:88 | 2019 (2010 original) |
| Children / school zones | IRC:SP:32 | 2023 (1988 original) |
| Delineators, hazard markers, guide posts | IRC:79 | 2019 |
| Speed limits | MoRTH notification S.O. 1522(E) 6-Apr-2018; MV (Driving) Regulations 2017 | — |
| Hill roads | IRC:SP:48 | 1998 |

---

## 1. Carriageway, lane, shoulder, median, kerb and right-of-way

### 1.1 Lane and carriageway widths

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| CW-01 | Standard lane width | 3.5 m | NH/SH/MDR, UA/USA/UC, 4/6-lane | IRC:73 cl.6; IRC:86-2018 (lane width table); IRC:SP:84-2019 cl.2.4; IRC:SP:87-2019 cl.2.4 | high | "standard lane width of project highway shall be 3.5 m" (SP:84) |
| CW-02 | Lane width, local/access streets | 3.0 m (min) | UL (residential access) | IRC:86-2018 | high | lower value permitted only on access roads |
| CW-03 | Lane width, urban range | 3.0–3.5 m | UA/USA/UC/UL | IRC:86-2018 | high | 3.5 m where buses/trucks |
| CW-04 | Expressway lane width | 3.75 m | EXP | IRC:SP:99-2013 cl.2.x | high | min 2 lanes per direction |
| CW-05 | Single-lane carriageway | 3.75 m | ODR/VR, hill roads | IRC:73 cl.6.1 | high | VR may be 3.0 m per IRC:SP:20 |
| CW-06 | Intermediate lane carriageway | 5.5 m | MDR/ODR | IRC:73 cl.6.1 | high | |
| CW-07 | Two-lane carriageway, no raised kerb | 7.0 m | NH/SH/MDR | IRC:73 cl.6.1 (3.2.2 in some copies) | high | |
| CW-08 | Two-lane carriageway, with raised kerbs | 7.5 m | urban/built-up two-lane | IRC:73 cl.6.1 | high | 0.25 m kerb shyness each side |
| CW-09 | Multi-lane carriageway | 3.5 m × n | all multi-lane | IRC:73 cl.6.1 | high | |
| CW-10 | 4-lane divided carriageway | 2 × 7.0 m | 4-lane NH | IRC:SP:84-2019 | high | |
| CW-11 | 6-lane divided carriageway | 2 × 10.5 m | 6-lane NH | IRC:SP:87-2019 cl.2.4 | high | |
| CW-12 | Village road single-lane carriageway | 3.0 m (3.75 m where traffic >100 veh/day) | VR (PMGSY) | IRC:SP:20-2002 | medium | |
| CW-13 | Kerb shyness / lateral clearance from kerb | 0.25–0.5 m | urban kerbed roads | IRC:86 | medium | 0.5 m typical in IRC:86 cross-sections |
| CW-14 | Minimum clearance from pavement edge to fixed object | 1.0 m (UA/USA); 0.5 m (UC/UL) | urban | IRC:86-1983 (reproduced in Delhi PWD Urban Roads Manual) | medium | |
| CW-15 | Urban expressway lane | 3.5–3.75 m | urban EXP | IRC:86-2018 | medium | |
| CW-16 | Cycle track width | 2.0 m one-way min (2.5 m desirable); 3.0 m two-way | urban | IRC:11-2015 / IRC:103 | medium | |
| CW-17 | Service road carriageway | 7.0 m (two-lane) + 1.5 m paved/earthen shoulder | NH built-up sections | IRC:SP:84/87-2019 | medium | 5.5 m intermediate lane allowed in constrained ROW (low) |

### 1.2 Roadway (formation) and shoulder widths

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| SH-01 | Roadway width NH/SH, plain & rolling | 12.0 m (two-lane) | NH/SH | IRC:73 Table (roadway widths) | high | 7.0 carriageway + 2 × 2.5 shoulders |
| SH-02 | Roadway width NH/SH, mountainous/steep | 6.25 m (single lane); 8.8 m (two-lane) | NH/SH hill | IRC:73 | high | |
| SH-03 | Roadway width MDR plain/rolling | 9.0 m | MDR | IRC:73 | high | 7.0 + 2 × 1.0 shoulders |
| SH-04 | Roadway width MDR mountainous | 4.75 m | MDR hill | IRC:73 | medium | |
| SH-05 | Roadway width ODR plain/rolling | 7.5 m | ODR | IRC:73 | high | intermediate 5.5 + 2 × 1.0 |
| SH-06 | Roadway width VR plain/rolling | 7.5 m | VR | IRC:73 | high | 3.75 + 2 × 1.875 |
| SH-07 | Roadway width ODR/VR mountainous | 4.75 m | ODR/VR hill | IRC:73 | medium | |
| SH-08 | Earthen shoulder each side, NH/SH plain | 2.5 m | NH/SH two-lane (IRC:73 basic) | IRC:73 | high | |
| SH-09 | Paved shoulder, two-lane NH (open country) | 1.5 m each side | NH two-lane with paved shoulder | IRC:SP:73-2018 Table 2.x; MoRTH circular RW/NH-33044/22/2020-S&R(P&B) | high | MoRTH 2020: 1.5 m paved + 1.0 m earthen for 2-laning |
| SH-10 | Earthen/granular shoulder beyond paved shoulder, two-lane NH | 1.0–2.0 m | NH two-lane | IRC:SP:73-2018; MoRTH 2020 circular | high | 2.0 m per SP:73 open country; 1.0 m per MoRTH 2020 |
| SH-11 | Paved shoulder in built-up stretches (two-lane) | 2.5 m each side (serves as NMT/parking lane) | NH built-up | IRC:SP:73-2018 built-up cross-section | medium | |
| SH-12 | Paved shoulder, 4-lane / 6-lane NH | 1.5 m each outer side | 4L/6L NH | IRC:SP:84-2019; IRC:SP:87-2019 cl.2.6 | high | |
| SH-13 | Earthen shoulder, 4-lane / 6-lane NH | 2.0 m each outer side | 4L/6L NH | IRC:SP:84/87-2019 | high | total roadway 4L ≈ 2×(7.0+1.5+2.0)+median |
| SH-14 | Paved shoulder, expressway | 3.0 m (outer) | EXP | IRC:SP:99-2013 | medium | plus 2.0 m earthen (medium); inner paved shoulder 0.75–1.5 m (low) |
| SH-15 | Median-side (inner) paved shoulder, 4L/6L | 0.5 m (raised median w/ kerb) to 1.5 m (depressed median) | 4L/6L NH | IRC:SP:84/87-2019 | medium | |
| SH-16 | Shoulder cross-fall | ≥ 0.5 % steeper than pavement; earth 3–5 %; paved same as carriageway | ALL | IRC:SP:50-2013; IRC:73 | high | |
| SH-17 | Shoulder level vs pavement edge | flush; no drop-off; edge drop > 50 mm = hazard | ALL | IRC:SP:50 / IRC:82 (edge break) / iRAP | medium | drop 25–50 mm = warning; >50 mm = fail |
| SH-18 | Hill-road parapet / shoulder | parapet 0.6 m high on valley side; roadway per IRC:SP:48 | hill roads | IRC:SP:48-1998 | medium | |

### 1.3 Medians

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| MD-01 | Absolute minimum median width (urban) | 1.2 m | UA/USA | IRC:86-2018 | high | |
| MD-02 | Desirable median width (urban) | 5.0 m | UA/USA | IRC:86-2018 | high | |
| MD-03 | Raised median with mountable kerb (highways) | 4.5 m | 4L/6L NH | IRC:SP:84/87-2019 cl.2.5 (refers IRC:86) | high | kerbed, 0.5 m shyness each side |
| MD-04 | Depressed median with crash barriers both sides | 7.0 m (min) | 4L/6L NH open country | IRC:SP:84/87-2019 | medium | |
| MD-05 | Minimum median in constrained built-up 4L/6L | 1.5–2.5 m (with barrier/kerb) | NH built-up | IRC:SP:84-2019 | low | verify project manual |
| MD-06 | Expressway depressed median | 12.0 m min; 15.0 m desirable | EXP | IRC:SP:99-2013 median table | high | measured between inner carriageway edges |
| MD-07 | Expressway flush median (with barrier) | 4.5 m min; 8.0 m desirable | EXP | IRC:SP:99-2013 | high | |
| MD-08 | Median kerb height | 150 mm (semi-barrier) ; max 150 mm on all urban roads | urban | UTTIPEC "Kerb heights for footpaths and medians"; IRC:86 | medium | barrier kerb 200 mm on high-speed medians (medium) |
| MD-09 | Median opening spacing (divided highways) | ≥ 2 km desirable; 500 m absolute min (built-up) | 4L/6L NH | IRC:SP:84/87-2019 cl. on median openings | medium | |
| MD-10 | Median opening length | 20–30 m (for U-turn/ crossing); storage lane 3.5 m | 4L/6L NH | IRC:SP:84 | low | |
| MD-11 | Median shrub height (sight/anti-glare) | ≤ 0.7 m (shrubs); anti-glare screens 1.5–1.8 m | urban/divided | IRC:103 draft; IRC:SP:84 | medium | |
| MD-12 | Pedestrian refuge in median at crossings | ≥ 1.2 m abs. min; 1.5–2.0 m recommended | urban | IRC:103-2012; ITDP Healthy Streets checklist | medium | see PD-15 |

### 1.4 Kerbs

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| KB-01 | Mountable (low) kerb height | ~100 mm (75–100 mm), sloping face | medians, channelizers, parking | IRC:86 kerb types (textbook values) | medium | |
| KB-02 | Semi-barrier kerb height | 150 mm, 1:1 batter top | footpath edge, medians (moderate speed) | IRC:86; UTTIPEC | medium | |
| KB-03 | Barrier kerb height | 200 mm (150–200 mm) near-vertical | high-speed medians, hazardous locations | IRC:86 | medium | 230–450 mm only on hill-road valley side/bridges (low) |
| KB-04 | Footpath (kerb) height above carriageway | ≤ 150 mm | urban footpaths | IRC:103-2012 cl.6.1.4 | high | |
| KB-05 | Kerb painting | alternate black & white bands, 500 mm each | roadside kerbs | IRC:35-2015 (object/kerb marking); UTTIPEC guideline citing IRC | high | up to 1.25 m height on poles/objects (medium) |
| KB-06 | Island/median nose kerb painting | alternate black & yellow (or chequered black/white) 500 mm | channelizing & central islands | IRC:35-2015; UTTIPEC | high | |
| KB-07 | "No parking" kerb marking | continuous yellow kerb | urban | IRC:35-2015 | medium | |
| KB-08 | Kerb ramp (pedestrian) slope | ≤ 1:12 (8.3 %); flared sides ≤ 1:10 | footpath ends/crossings | IRC:103-2012 | high | |
| KB-09 | Kerb ramp width | ≥ 1.2 m (some copies 0.9 m) | footpath | IRC:103-2012 | medium | |

### 1.5 Right-of-way (land width), building & control lines

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| RW-01 | ROW urban arterial | 50–60 m (1983); 40–60 m (2018) | UA | IRC:86-1983 Table 1; IRC:86-2018 Table 4.1 | high/medium | |
| RW-02 | ROW urban sub-arterial | 30–40 m (1983); 30–45 m (2018) | USA | IRC:86-1983/2018 | high | |
| RW-03 | ROW urban collector | 20–30 m | UC | IRC:86-1983 (2018: 25–35 m, low) | high | |
| RW-04 | ROW urban local | 10–20 m (2018: 10–15 m new areas) | UL | IRC:86-1983; IRC:SP:118-2018 | high | |
| RW-05 | ROW urban expressway | 60–90 m | urban EXP | IRC:86-2018 | low | |
| RW-06 | Land width NH/SH plain/rolling, open area | 45 m normal (30–60 m range) | NH/SH | IRC:73 Table 3 | high | |
| RW-07 | Land width NH/SH mountainous | 24 m (18–24 m) | NH/SH hill | IRC:73 Table 3 | high | |
| RW-08 | Land width MDR plain | 25 m (25–30) | MDR | IRC:73 Table 3 | high | |
| RW-09 | Land width ODR plain | 15 m (15–25) | ODR | IRC:73 Table 3 | high | |
| RW-10 | Land width VR plain | 12 m (12–18) | VR | IRC:73 Table 3 | high | |
| RW-11 | Land width built-up: NH/SH 30 m; MDR 20 m; ODR 15 m; VR 10 m | as listed | rural built-up | IRC:73 Table 3 | high | |
| RW-12 | ROW 4-lane / 6-lane NH | 60 m minimum | 4L/6L NH | IRC:SP:84-2019 cl.2.3; IRC:SP:87-2019 cl.2.3 | high | |
| RW-13 | ROW expressway | 90 m min (plain); 120 m desirable/with service roads | EXP | IRC:SP:99-2013 | medium | |
| RW-14 | Building line (overall width between building lines), open country | NH/SH 80 m; MDR 50 m; ODR 25–30 m; VR 25 m | rural | IRC:73 Table 4 | medium | |
| RW-15 | Control line (overall width), open country | NH/SH 150 m; MDR 100 m; ODR 35 m; VR 30 m | rural | IRC:73 Table 4 | medium | |
| RW-16 | Building line set-back from road boundary, built-up | 3–6 m (NH/SH); 3–5 m (MDR/ODR/VR) | rural built-up | IRC:73 Table 4 | medium | |

---

## 2. Footpaths and pedestrian facilities (IRC:103-2012, IRC:35, IRC:86)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| PD-01 | Minimum clear (obstruction-free) footpath width | 1.8 m | all urban roads (ROW ≥ 10 m) | IRC:103-2012 cl.6.1.3 | high | two wheelchairs passing |
| PD-02 | Footpath clear width, residential/mixed use | 1.8 m | UL/UC | IRC:103-2012 cl.6.1.5.2 | high | |
| PD-03 | Footpath clear width, commercial/mixed use | 2.5 m | UA/USA/UC commercial | IRC:103-2012 cl.6.1.5.2 | high | |
| PD-04 | Footpath clear width, shopping frontage / high-intensity commercial | 3.5–4.0 m | commercial streets | IRC:103-2012 (land-use table) | medium | |
| PD-05 | Footpath clear width at bus stops | 3.0 m | roads with bus stops | IRC:103-2012 | medium | |
| PD-06 | Footpath width where ROW < 10 m | 1.5 m min | narrow UL | IRC:103-2012 (draft text) | medium | |
| PD-07 | Footpath zones | frontage 0.5 m; pedestrian zone ≥ 1.8 m; furniture/planting zone 0.5–1.0 m (min 0.6 m for utilities) | urban | IRC:103-2012 cl.6.1.5; ITDP | medium | |
| PD-08 | Footpath height above carriageway | ≤ 150 mm | urban | IRC:103-2012 cl.6.1.4 | high | |
| PD-09 | Footpath cross slope | 1.5–2.0 % (max 2.5 %) | urban | IRC:103-2012 | medium | |
| PD-10 | Footpath longitudinal gradient / ramps | ≤ 5 % (1:20) preferred; ramps ≤ 1:12 with landings every 9 m | urban | IRC:103-2012; CPWD harmonised guidelines | medium | |
| PD-11 | Vertical clear headroom over footpath | ≥ 2.2 m (2.4 m for subways/FOB interiors) | urban | IRC:103-2012 | medium | tree branches, sign boards, shop awnings |
| PD-12 | Bollard clear spacing | ≥ 0.9 m (wheelchair passage); bollard height 0.9–1.0 m | footpath entries | IRC:103-2012 | high (spacing) / medium (height) | |
| PD-13 | Tactile paving: warning (dome) tiles | 300 mm band at top/bottom of ramps, before crossings, at hazards | footpaths | IRC:103-2012; Harmonised Guidelines (MoHUA 2021) | high | tiles 300×300 mm, dome/bar height ~5 mm (medium) |
| PD-14 | Tactile guiding (bar) tiles | continuous 300 mm strip along footpath, ≥ 0.6 m from kerb/obstacles | footpaths | IRC:103-2012 | medium | |
| PD-15 | Pedestrian refuge island width | ≥ 1.2 m absolute; 1.5 m preferred; 2.0 m to hold wheelchair/pram | median crossings on roads > 10 m / ≥ 4 lanes | IRC:103-2012; WRI/ITDP checklists | medium | refuge mandatory on roads wider than ~10 m (medium) |
| PD-16 | Refuge island length | ≥ crossing width (≥ 2 m); same level as footpath (150 mm) or cut-through at road level | urban | IRC:103; ITDP | medium | |
| PD-17 | Zebra crossing stripe | 500 mm wide stripes, 500 mm gaps, white | ALL | IRC:35-2015; IRC:103-2012 | high | |
| PD-18 | Zebra crossing width (length of stripes in direction of walking) | 2.0 m min (urban); 2.5–4.0 m typical; width by pedestrian volume | ALL | IRC:35-2015 (width based on ped volume); secondary 2–4 m | medium | |
| PD-19 | Stop line setback before zebra | 2–3 m (urban 2 m; rural 3 m) | signalised/zebra | IRC:35-2015 | medium | |
| PD-20 | Road studs at zebra | required on both edges of zebra | ALL | IRC:35-2015 | high | |
| PD-21 | Mid-block crossing spacing (urban arterials) | ≤ 250 m (crossing opportunity every 150–250 m; 80–150 m in commercial/CBD) | UA/USA | IRC:103-2012 (secondary); ITDP | medium | |
| PD-22 | Controlled (signal/pelican) crossing warrant | PV² > 1 × 10⁸ (undivided); > 2 × 10⁸ (divided) | urban | IRC:103-2012 (retained from 1988) | high | P = peds/h over 100 m, V = veh/h |
| PD-23 | Grade-separated crossing (FOB/subway) warrants | only where at-grade infeasible: high speed (≥ 60–70 km/h) + high volume, pedestrian injuries > 5/yr, PV² very high | UA/NH built-up | IRC:103-2012 cl. on grade separation | medium | four conditions listed in code |
| PD-24 | FOB / subway clear width & height | ≥ 2.0 m internal clear width (2.5 m desirable); 2.4 m clear height; ramps ≤ 1:12; lifts/escalators where ramps infeasible | urban | IRC:103-2012 | medium | |
| PD-25 | Pedestrian guardrail height | 1.0–1.1 m; set back 0.25 m from kerb edge; contrasting colour | medians/footpath edges near schools, signals | IRC:103-2012 | medium | guardrails must not block kerb ramps |
| PD-26 | Pedestrian signal timing | green-man ≥ 7 s + clearance = crossing length / 1.2 m/s (1.0 m/s where elderly/children) | signalised crossings | IRC:93-1985; IRC:103-2012 | medium | |
| PD-27 | Pelican/puffin crossings | push-button, countdown recommended; signal head bottom 2.5 m above footpath | urban mid-block | IRC:103-2012; IRC:93 | medium | |
| PD-28 | Raised (table-top) pedestrian crossing | 100–150 mm high (flush with footpath), ramps 1:10–1:15, top ≥ 3 m (≥ zebra width) | UL/UC, school zones; not on NH through carriageway | IRC:99-2018; IRC:103-2012 | medium | |
| PD-29 | Footpath continuity across property accesses | footpath level continuous; vehicle ramp in furniture zone, not pedestrian zone | urban | IRC:103-2012 | high | |
| PD-30 | Obstructions prohibited in pedestrian zone | poles, transformers, trees, hawkers, parked vehicles, drain openings | urban | IRC:103-2012 | high | detection rule: any object inside 1.8 m clear zone = fail |
| PD-31 | Street furniture setback from kerb | ≥ 0.45–0.6 m from kerb face | urban | IRC:103 / IRC:86 | medium | |
| PD-32 | Tree pit / grating | flush with footpath; grating openings ≤ 13 mm | footpath | IRC:103; Harmonised Guidelines | medium | |
| PD-33 | Footpath surface | non-slip, even; max level difference 6 mm (12 mm bevelled) | footpath | Harmonised Guidelines for accessibility (MoHUA) | medium | |
| PD-34 | Pedestrian fencing to prevent mid-block crossing | ≥ 1.1 m; only where crossing facility within 100 m | high-speed urban | IRC:103 | low | |
| PD-35 | Cycle track | 2.0 m one-way, 3.0 m two-way; segregated by kerb/buffer ≥ 0.5 m on roads with speed > 50 km/h | urban | IRC:11-2015 | medium | |

---

## 3. Road markings (IRC:35-2015; MoRTH Specifications Sec. 803)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| MK-01 | Lane line / centre line width (urban) | ≥ 100 mm | UA/USA/UC/UL | IRC:35-2015 cl.4.6.9 | high | |
| MK-02 | Lane line width (highways, multi-lane) | 150 mm | NH/SH/4L/6L | IRC:35-2015 | high | |
| MK-03 | Lane line pattern, normal sections (highways) | broken 3 m line / 6 m gap (3:6) | NH/SH multi-lane | IRC:35-2015 ("3 m mark + 6 m gap … normal sections") | medium | several secondary sources quote 3 m / 4.5 m; accept either |
| MK-04 | Lane/centre line pattern, urban roads & 4-lane undivided | 3 m line / 4.5 m gap, 100–150 mm | UA/USA, 4L undivided | IRC:35-2015 (secondary) | medium | |
| MK-05 | Centre line pattern, low-speed urban streets | 1.5 m line / 3.0 m gap, 100 mm | UC/UL (speed ≤ 50 km/h) | IRC:35 (1997 text via UTTIPEC guideline) | medium | |
| MK-06 | Warning (hazard) line approaching junctions/curves | segment longer than gap, e.g. 6 m line / 3 m gap (or 3 m / 1.5 m), ≥ 1.5 × normal width | ALL | IRC:35-2015 | low | |
| MK-07 | Centre line, two-lane rural roads | single broken white; continuous (barrier) where OSD not available | NH/SH/MDR | IRC:35-2015 | high | |
| MK-08 | No-overtaking (barrier) line | single or double continuous yellow, each 100 mm, 100 mm gap between | two-lane two-way | IRC:35-2015 | medium | double line = both directions prohibited |
| MK-09 | Edge line (carriageway edge) | continuous white; 150 mm on multi-lane divided; 200 mm on expressways; 100 mm min urban/two-lane | ALL | IRC:35-2015 cl.4.5.3 | high | |
| MK-10 | Median-side edge line colour | yellow continuous (median side) on divided highways/expressways; white on outer edge | 4L/6L/EXP | IRC:35-2015 / NHAI practice | low | verify project spec |
| MK-11 | Stop line width | 200 mm (urban); 300 mm (rural) | ALL | IRC:35-2015 (single stop line clause) | high | |
| MK-12 | Stop line position | 1.0–1.5 m before pedestrian crossing (urban 2 m before zebra; min 1.2 m); at least 1.5 m from edge of intersecting carriageway if no crossing | signalised/STOP controlled | IRC:35-2015 | medium | |
| MK-13 | Give-way line | two parallel broken lines, 600 mm segments / 300 mm gaps, each 200 mm wide (150 mm urban) | minor-road approaches | IRC:35-2015 | high (pattern) / medium (width) | |
| MK-14 | Give-way approach triangle | hollow inverted white triangle on approach lane, ~3.0–3.75 m long × 1.0–1.25 m base, 150 mm stroke | minor approaches | IRC:35-2015 | low | |
| MK-15 | Zebra crossing | 500 mm stripes / 500 mm gaps; 2–4 m wide; white; studs both sides | ALL | IRC:35-2015 | high | |
| MK-16 | Pedestrian crossing lines at signalised junctions (parallel lines instead of zebra) | two transverse lines 100–150 mm wide, 2–4 m apart | signalised | IRC:35-2015 | medium | |
| MK-17 | Diagonal (ladder) hatching spacing | 4 m c/c (speed ≤ 65 km/h); 6 m c/c (> 65 km/h) | ALL | IRC:35-2015 | high | |
| MK-18 | Hatching stroke width | 100 or 150 mm; boundary line 150–200 mm | ALL | IRC:35-2015 | high | |
| MK-19 | Chevron (merge/diverge gore) markings | white chevrons pointing toward traffic, 150 mm stroke; diagonal hatching for separating opposing flows (yellow where restricting) | ramps, gores, island approaches | IRC:35-2015 | medium | |
| MK-20 | Direction arrows length | 3.5 m (speed ≤ 60 km/h / urban); 5.0 m (high-speed); 7.5 m expressway | ALL | IRC:35-2015 | medium | |
| MK-21 | Arrow placement before junction | at 15 m, 30 m and 45 m (urban); repeated 3 times, 30–50 m apart on highways | ALL | IRC:35-2015 | low | |
| MK-22 | Yellow box junction | yellow cross-hatched box, 100–150 mm lines, boundary 200 mm | congested urban junctions, level crossings | IRC:35-2015 | medium | |
| MK-23 | Bus stop / bus lane marking | "BUS STOP" word marking, 100–150 mm yellow boundary; box length 18–27 m | urban | IRC:35-2015 | low | |
| MK-24 | Parking bay markings | white 100 mm lines; parallel bay 2.5 × 5.0–6.0 m; angled 2.5 × 5.0 m | urban | IRC:35-2015; IRC:SP:12-2015 | medium | |
| MK-25 | Word/letter markings height | 1.25 m (speed ≤ 50); 2.5 m (> 50); 4 m expressway; elongated | ALL | IRC:35-2015 | medium | |
| MK-26 | Speed hump marking | white (retroreflective thermoplastic) triangles/chevrons on hump face, or alternate black-white bands; "HUMP" sign | humps | IRC:99-2018; IRC:35 | medium | |
| MK-27 | Object marking (within/adjacent carriageway) | alternating black & yellow diagonal stripes (45°), band 100–150 mm… 300 mm; retroreflective | piers, abutments, poles | IRC:35-2015; IRC:79-2019 | high | |
| MK-28 | Road stud (RPM) colours | white – lane lines; yellow – centre/median side & no-overtaking; red – left (outer) edge; green – lay-bys / slip roads / exits | ALL | IRC:35-2015 | medium | |
| MK-29 | Road stud spacing | 9 m (curves, approaches, urban); 18 m (tangent sections); 3 m at hazards/ gore | NH/SH/EXP | IRC:35-2015 | medium | |
| MK-30 | Rumble strips (thermoplastic) | 4–6 mm thick bars, 200–300 mm wide, 300–500 mm spacing; 3–5 bars per set | approaches to hazards | IRC:35-2015 / IRC:99-2018 | low | see TC-10 |
| MK-31 | Retroreflectivity, new white thermoplastic marking (RL) | ≥ 150 mcd/m²/lx (contract specs often 200–300) | ALL | IRC:35-2015 Table (EN 1436 classes R2–R5); MoRTH 803.4 | medium | measured at 30 m geometry |
| MK-32 | Retroreflectivity, new yellow marking | ≥ 100 mcd/m²/lx (contracts 150–175) | ALL | IRC:35-2015 | medium | |
| MK-33 | Retroreflectivity, in-service (re-marking trigger) | white < 100 mcd/m²/lx; yellow < 75–80 mcd/m²/lx | ALL | IRC:35-2015 / MoRTH maintenance | low | some sources 80/60 |
| MK-34 | Thermoplastic marking thickness | 2.5 mm (±0.2) applied; glass beads 250 g/m² drop-on | ALL | MoRTH 803.4 | high | |
| MK-35 | Daytime luminance / colour | white: luminance factor ≥ 0.30 (β); yellow ≥ 0.20 | ALL | IRC:35-2015 (EN 1436) | low | |
| MK-36 | Marking colour convention | white = general; yellow = restriction (no overtaking, no parking/stopping, bus/cycle lanes, yellow box, hazards) | ALL | IRC:35-2015 | high | |
| MK-37 | Skid resistance of markings | SRT ≥ 45 (BPN) wet | ALL | IRC:35-2015 | low | |
| MK-38 | Cycle lane marking | 100–150 mm white line + cycle symbol; coloured surface optional (green) | urban | IRC:11-2015 | low | |

---

## 4. Road signs (IRC:67-2022 / 2012; MoRTH circulars)

### 4.1 Categories and shapes

| ID | Parameter | Threshold | Source | Conf |
|---|---|---|---|---|
| SG-01 | Mandatory/regulatory signs | circular; red border, white ground, black symbol; prohibitory with red diagonal bar where applicable; STOP = red octagon; GIVE WAY = inverted red-bordered triangle; positive instruction (compulsory) = blue circle white arrow | IRC:67-2022 cl.5 | high |
| SG-02 | Cautionary/warning signs | equilateral triangle apex up; red border, white ground, black symbol | IRC:67-2022 cl.6 | high |
| SG-03 | Informatory signs | rectangular; direction signs green ground (NH/EXP), blue (facilities/route information), white/black (local/urban); yellow background for temporary/diversion | IRC:67-2022 cl.7 | medium |
| SG-04 | Work-zone signs | yellow (or fluorescent orange) background, black legend | IRC:SP:55-2014 | medium |

### 4.2 Sizes by design speed (IRC:67-2012 Table 15.1 — retained in 2022 with 1500 mm added for expressways)

| ID | Design speed | Cautionary triangle side | Mandatory circle dia | Clear visibility | Siting distance ahead of hazard | Conf |
|---|---|---|---|---|---|---|
| SG-05 | ≤ 50 km/h (UL/UC/urban) | 600 mm (border 45 mm) | 600 mm | 45 m | 45 m | high |
| SG-06 | 51–65 km/h | 750 mm (border 60 mm) | 750 mm | 60 m | 45–110 m | high |
| SG-07 | 66–80 km/h | 900 mm (border 70 mm) | 900 mm | 60 m | 110–180 m | high |
| SG-08 | > 80 km/h (NH/SH 100 km/h) | 1200 mm (border 90 mm) | 1200 mm | 90 m | 180–245 m | high |
| SG-09 | Expressway, design speed > 120 km/h | 1500 mm | 1500 mm | ≥ 120 m | 250–300 m | medium (2021/22 revision) |
| SG-10 | Mini mandatory circle beside traffic signals | 300 mm | — | — | — | high |
| SG-11 | STOP sign | 900 mm octagon (600 small / 1200 large); GIVE WAY triangle 900 mm (600/1200) | IRC:67 | medium |
| SG-12 | Speed-limit sign | 600 mm (urban), 900 mm (NH), 1200 mm (EXP); numerals ≥ 1/3 of diameter | IRC:67 | medium |
| SG-13 | Direction sign letter height | ~100 mm (≤ 50 km/h), 150 mm (65), 200 mm (80), 250–300 mm (100), 350–400 mm expressway gantry; legibility ≈ 6 m per 10 mm letter height | IRC:67-2022 Table 12.1 | medium |

### 4.3 Placement

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| SG-14 | Mounting height, kerbed urban roads (bottom of lowest sign above kerb) | 2.0–2.5 m (2012); ≥ 2.1 m over footpath (2022) | urban | IRC:67-2012 cl.14; IRC:67-2022 | high | |
| SG-15 | Mounting height, roads without kerb (bottom edge above crown) | 2.0–2.5 m (1.5 m min in older practice) | rural | IRC:67-2012 | high | reject < 1.5 m |
| SG-16 | Lateral clearance, edge of sign from carriageway edge | 2.0–3.0 m (roads with/without shoulder) | rural/NH | IRC:67-2012 cl.14 | high | |
| SG-17 | Lateral clearance from kerb line (urban) | ≥ 0.6 m (2012); ≥ 0.3 m (2022) | urban | IRC:67 | high | |
| SG-18 | Overhead/gantry sign vertical clearance | 5.5 m min above carriageway | ALL | IRC:67 / IRC:SP:84 | medium | |
| SG-19 | Gantry placement before intersection/exit | ≥ 200 m in advance (expressway exits 2 km, 1 km, 500 m advance direction signs) | EXP/NH | IRC:67-2022; IRC:SP:99 | medium | |
| SG-20 | Reassurance sign after junction | 100–150 m after junction | NH/SH | IRC:67-2022 | medium | |
| SG-21 | Sign face angle | 3–5° away from perpendicular to approach (to reduce specular glare); facing traffic | ALL | IRC:67 | medium | |
| SG-22 | Repetition of mandatory (speed) signs | every ~0.6 × V m (V = 85th percentile speed km/h) on long sections; after every major junction | ALL | IRC:67-2012 (secondary) | low | |
| SG-23 | Signs not to be obstructed | no vegetation/hoardings within sight line over clear-visibility distance (SG-05..09) | ALL | IRC:67; IRC:SP:88 | high | |
| SG-24 | Max signs per post | 2 (3 with one informatory); no advertisement on sign posts | ALL | IRC:67 | medium | |
| SG-25 | Sign post | GI pipe/steel, breakaway or frangible on high-speed roads outside barrier | ALL | IRC:67; IRC:119 | medium | |
| SG-26 | Speed-breaker warning sign location | 40 m in advance of hump (urban); plus sign at hump | humps | IRC:99-2018 (IRC:99-1988 "40 m") | medium | |
| SG-27 | School-ahead sign | cautionary at siting distance (45–110 m urban) before school zone; speed-limit sign at zone start | school zones | IRC:67; IRC:SP:32-2023 | medium | |
| SG-28 | Pedestrian-crossing cautionary sign | 50 m (urban) before uncontrolled zebra on roads ≥ 50 km/h | ALL | IRC:67 | medium | |

### 4.4 Retroreflective sheeting

| ID | Parameter | Threshold | Source | Conf |
|---|---|---|---|---|
| SG-29 | Sheeting classes | Class A = ASTM D4956 Type I/II (engineering/super-engineering grade); Class B = Type III/IV (high-intensity prismatic); Class C = Type VIII/IX/XI (micro-prismatic) | IRC:67-2022 cl.15 | high |
| SG-30 | Expressways | Class C, Type XI | IRC:67-2022 (trafficinfratech summary) | medium |
| SG-31 | NH / SH | Class C (Type XI); Type IV only in work zones | IRC:67-2022 | medium |
| SG-32 | MDR | Class B or C (Type IV, IX, XI) | IRC:67-2022 | medium |
| SG-33 | ODR / VR | Class A or B (Type I/IV) | IRC:67-2022 | medium |
| SG-34 | Urban roads | Class B or C (Type IX/XI); Type IV in work zones | IRC:67-2022 | medium |
| SG-35 | Minimum coefficient of retroreflection RA (new, white, 0.2°/−4°) | Type IV ≈ 250; Type IX ≈ 380; Type XI ≈ 580 cd/lx/m² | ASTM D4956 (referenced by IRC:67) | medium |
| SG-36 | In-service sign retroreflectivity (replacement trigger) | < 50 % of initial or white < 50 cd/lx/m² (Type I), < 100 (Type IV), < 250 (Type XI) | MoRTH circular SR 24-10-2017 (signs & markings); FHWA practice | low |
| SG-37 | Sign condition | no fading, vandalism, bending; legible at the clear-visibility distance day & night | IRC:SP:88 checklist | high |
| SG-38 | Delineators / guide posts (IRC:79-2019) | 1.0–1.2 m above shoulder; alternating black & white bands; retroreflector 80 mm red on left (near) side, white on right/median side; spacing 30 m tangent, 9–15 m curves (by radius) | IRC:79-2019 | medium |
| SG-39 | Hazard markers (IRC:79) | black & yellow (fluorescent yellow element) downward-sloping stripes, Type XI sheeting; on islands, culvert ends, barrier terminals | IRC:79-2019 | high |
| SG-40 | Chevron alignment signs on curves | at curves R < 300 m (or where deflection > 30°); spacing so 3 visible; 600×750 mm | NH/SH | IRC:67; IRC:79 | medium |

---

## 5. Speed breakers / traffic calming (IRC:99-2018; MoRTH)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Circular speed hump height | 100 mm max (rise < 100 mm gives higher crossing speed; > 100 mm damages vehicles) | minor roads | IRC:99-2018 (circular hump table) | high | |
| TC-02 | Classic IRC:99-1988 hump | 3.7 m chord, 0.10 m height, 17 m radius, design crossing speed 25 km/h | minor roads | IRC:99-1988 cl.4 | high | still the most common field dimension |
| TC-03 | IRC:99-2018 circular hump chord by desired crossing speed (h = 100 mm) | 20 km/h → 3.0 m (R 11 m); 25 → 3.5 m (R ≈ 16 m); 30 → 4.0 m (R ≈ 20 m); 40 → 6.5 m (R ≈ 53 m); 45 → 8.0 m; 50 → 9.5 m (R 113 m) | minor roads, approaches | IRC:99-2018 Table (circular humps); MoHUA Code of Practice Part 5 | high | compliance window: chord 3.0–9.5 m, h ≤ 100 mm |
| TC-04 | Hump profile | circular/parabolic, no sharp edges; full carriageway width, no gaps at edges (or drainage gap ≤ 0.3 m) | — | IRC:99-2018 | medium | |
| TC-05 | Speed table (flat-top hump) | 75–100 mm high; flat top 3–6 m (≥ wheelbase; 6 m where buses); ramps 1:10–1:25 | UL/UC, school zones | IRC:99-2018 | medium | |
| TC-06 | Raised pedestrian crossing | 100–150 mm (flush with footpath), ramps 1:10–1:15, zebra on top | UL/UC | IRC:99-2018; IRC:103 | medium | |
| TC-07 | Speed cushion | 1.6–1.9 m wide, 65–75 mm high, 2–3 m long; gaps for bus/ambulance track | urban bus routes | IRC:99-2018 | low | |
| TC-08 | Where humps are NOT permitted | main carriageway of NH/SH/EXP/arterials; on curves, gradients > 4 %, bridges/culverts, within 20–30 m of junction stop line (except minor approach), near hospitals' emergency routes, where speed ≥ 50 km/h design | — | IRC:99-2018; MoRTH circular on speed breakers on NHs (RW/NH-33044 series) | medium | NH: only at toll plazas / minor-road approaches |
| TC-09 | Hump location rules | on minor road approach to major road, 10–20 m before stop line; first hump ≥ 50 m from start of street; spacing 100–150 m (max ~250 m) between successive humps for 30 km/h | UL/UC | IRC:99-2018 | medium | |
| TC-10 | Rumble strips (asphalt/transverse) | height ≤ 25 mm (asphalt), 200–300 mm wide, 3–7 bars; thermoplastic rumble bars 4–6 mm; sets placed 50–100 m before hazard | approaches to junctions, toll plazas, villages | IRC:99-2018 | medium | |
| TC-11 | Hump marking | white retroreflective thermoplastic chevrons/triangles (or alternate black & white bands 250–500 mm) across hump; studs/cat-eyes both sides | all humps | IRC:99-2018 | medium | |
| TC-12 | Hump warning sign | "Speed Breaker / Hump" cautionary sign 40 m ahead (urban) and at hump; speed-limit sign | all humps | IRC:99-2018 (40 m from 1988 ed.) | medium | |
| TC-13 | Lighting at hump | hump within lit zone at night (street light within ~30 m) | urban | IRC:99-2018 | low | |
| TC-14 | School zone speed | 25 km/h max | all roads near schools | IRC:99-2018; MV (Driving) Regulations 2017 reg.16(5) | high | |
| TC-15 | Hospital zone speed | 30 km/h max | roads near hospitals | IRC:99-2018 | high | |
| TC-16 | Residential street design speed with calming | 30 km/h | UL | IRC:86-2018; IRC:99-2018 | high | |
| TC-17 | Chicanes / lateral shifts | lane shift ≥ 1 lane over 10–20 m; min lane 3.0 m | UL | IRC:99-2018 | low | |
| TC-18 | Gateways at village entries on NH | signage + rumble strips + narrowing; speed limit 40–50 km/h through built-up | NH built-up | IRC:99-2018; IRC:SP:84 | medium | |
| TC-19 | Unauthorised speed breakers | any hump not meeting TC-01/03 or without TC-11/12 = non-compliant hazard | — | IRC:99; Supreme Court Committee on Road Safety directions 2015–17 | high | |

---

## 6. Traffic signals (IRC:93-1985; IRC:103; IRC:SP:41)

| ID | Parameter | Threshold | Source | Conf | Notes |
|---|---|---|---|---|---|
| TS-01 | Post-mounted signal head height (bottom of housing) | 2.5 m above footpath (or pavement at road centre where no footpath) | IRC:93-1985 | high | |
| TS-02 | Overhead/cantilever signal head height | 5.5 m above pavement at road centre | IRC:93-1985 | high | |
| TS-03 | Minimum signal faces per approach | 2 (primary + secondary) for through traffic | IRC:93-1985 | high | |
| TS-04 | Required visibility distance of signal face | 40 m @ 35 km/h … 120 m @ 75 km/h (approx. 50 m @ 40, 75 m @ 50, 100 m @ 65) | IRC:93-1985 table | high (end points) / medium (interpolated) | |
| TS-05 | Primary signal lateral position | 0.6 m from kerb/footpath edge, 1–1.5 m before stop line | IRC:93-1985 (layout) | medium | |
| TS-06 | Secondary signal position | 12–36 m beyond stop line (far side) | IRC:93-1985 | medium | |
| TS-07 | Lens diameter | 200 mm (≤ 50 km/h); 300 mm (> 50 km/h, high-speed approaches) | IRC:93-1985 | medium | |
| TS-08 | Amber (yellow) interval | 3 s (≤ 50 km/h) to 5 s (> 60 km/h) | IRC:93-1985 | medium | |
| TS-09 | All-red clearance | 1–2 s (up to 3 s for wide junctions) | IRC:93-1985 | medium | |
| TS-10 | Minimum green | 7 s vehicles; pedestrians 7 s + crossing length / 1.2 m/s | IRC:93-1985; IRC:103 | medium | |
| TS-11 | Cycle length | 40–120 s (max 150 s); signal warrants per IRC:93 (vehicular volume, pedestrian volume, accident) | IRC:93-1985 | medium | |
| TS-12 | Pedestrian signal heads | required at all signalised junctions with pedestrian movement; red/green man; countdown recommended (not mandated by IRC:93) | IRC:103-2012 | medium | |
| TS-13 | Signal warrant – pedestrian | PV² > 1×10⁸ (undivided) / 2×10⁸ (divided) | IRC:103 | high | |
| TS-14 | Signal warrant – vehicular | major-street volume ≥ 650 veh/h both approaches + minor ≥ 200 veh/h for 8 h (approximate IRC:93 figures) | IRC:93-1985 | low | |
| TS-15 | Supports placement | outside clear zone/behind kerb; not obstructing footpath clear width | IRC:93; IRC:103 | high | |
| TS-16 | Backing boards / visibility | black backing board on high-speed/sun-glare approaches; hoods | IRC:93 | medium | |
| TS-17 | Blinker (flashing amber) at mid-block/zebra | flashing amber 50–60/min, solar | MoRTH/ IRC:103 practice | low | |

---

## 7. Horizontal & vertical geometry (IRC:73, IRC:86, IRC:38, IRC:SP:23, IRC:66, IRC:SP:73/84/87/99)

### 7.1 Design speeds

| ID | Road class | Plain | Rolling | Mountainous | Steep | Source | Conf |
|---|---|---|---|---|---|---|---|
| GS-01 | NH/SH (ruling / minimum) | 100 / 80 | 80 / 65 | 50 / 40 | 40 / 30 | IRC:73 Table 2 | high |
| GS-02 | MDR | 80 / 65 | 65 / 50 | 40 / 30 | 30 / 20 | IRC:73 Table 2 | high |
| GS-03 | ODR | 65 / 50 | 50 / 40 | 30 / 25 | 25 / 20 | IRC:73 Table 2 | high |
| GS-04 | VR | 50 / 40 | 40 / 35 | 25 / 20 | 25 / 20 | IRC:73 Table 2 | high |
| GS-05 | Expressway | 120 | 100 | 80 | — | IRC:SP:99-2013 | high |
| GS-06 | Urban expressway | 80 | 70 | 60 | — | IRC:86-2018 Table 3.1 | high |
| GS-07 | Urban arterial | 80 (1983) / 60 (2018 table as reproduced) | 50 | 40 | — | IRC:86-1983; IRC:86-2018 Table 3.1 | high/medium |
| GS-08 | Urban sub-arterial | 60 | 50 | 40 | — | IRC:86 | high |
| GS-09 | Urban collector | 50 (1983) / 40 (2018) | 40 | 30 | — | IRC:86 | high |
| GS-10 | Urban local | 30 | 30 | 20 | — | IRC:86 | high |
| GS-11 | Posted speed near schools/hospitals/markets | 20–25 km/h | — | — | — | IRC:86-2018 note; IRC:99 | high |
| GS-12 | Terrain classification (cross slope) | plain 0–10 %, rolling 10–25 %, mountainous 25–60 %, steep > 60 % | — | — | — | IRC:73 Table 1 | high |

### 7.2 Horizontal curves

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| GH-01 | Maximum superelevation | 7 % plain/rolling; 10 % hilly not snow-bound; 7 % snow-bound; 4 % urban roads with frequent intersections | ALL | IRC:73 cl.9; IRC:86; IRC:38 | high | |
| GH-02 | Superelevation design formula | e = V²/225R (75 % design speed, no friction), check e ≤ e_max; else e = e_max and f = V²/127R − e ≤ 0.15 | ALL | IRC:38-1988; IRC:73 | high | |
| GH-03 | Minimum superelevation | = camber (1.7–2.5 %) | ALL | IRC:38 | high | |
| GH-04 | Ruling / absolute minimum radius, NH/SH plain | 360 m / 230 m | NH/SH | IRC:73 Table (e=7 %, f=0.15) | high | |
| GH-05 | NH/SH rolling | 230 / 155 m | NH/SH | IRC:73 | high | |
| GH-06 | NH/SH mountainous | 80 / 50 m | NH/SH | IRC:73 | high | |
| GH-07 | NH/SH steep | 50 / 30 m | NH/SH | IRC:73 | high | |
| GH-08 | MDR plain / rolling | 230/155 m ; 155/90 m | MDR | IRC:73 | high | mountainous 50/30; steep 30/20 |
| GH-09 | ODR plain / rolling | 155/90 m ; 90/60 m | ODR | IRC:73 | high | mountainous 30/20; steep 20/14 |
| GH-10 | VR plain / rolling | 90/60 m ; 60/45 m | VR | IRC:73 | high | mountainous 20/14; steep 20/14 |
| GH-11 | NH 2L/4L/6L manuals: desirable min / absolute min radius plain-rolling | 400 m / 250 m | IRC:SP:73/84/87 | IRC:SP:73-2018 Table 2.x; SP:84/87-2019 | high | mountainous 150 m / 75 m (medium) |
| GH-12 | Expressway minimum radius | 1000 m desirable (120 km/h); 670 m absolute (e = 7 %) | EXP | IRC:SP:99-2013 | medium | |
| GH-13 | Urban minimum radius (e_max 4–7 %, f 0.15) | 80 km/h: 230–265 m; 60: 130–150 m; 50: 90–105 m; 40: 60–70 m; 30: 30–40 m; 20: 15–20 m | UA..UL | IRC:86 (formula-derived) | medium | |
| GH-14 | Lateral friction coefficient | 0.15 | ALL | IRC:73 / IRC:38 | high | |
| GH-15 | Transition (spiral) curve length | Ls = larger of 0.0215 V³/(C·R) [C = 80/(75+V), 0.5–0.8 m/s³] and superelevation run-off at 1 in 150 (plain/rolling), 1 in 60 (mountainous/steep), 1 in 100 (urban) ; min Ls = 2.7 V²/R (plain) | ALL | IRC:38-1988; IRC:73 Table 9 | high | |
| GH-16 | Curves not needing transition | R ≥ 2000 m? (plain, V 100); generally where e ≤ camber | ALL | IRC:38 | low | |
| GH-17 | Extra widening, two-lane | R ≤ 20 m: 1.5 m; 21–40: 1.5; 41–60: 1.2; 61–100: 0.9; 101–300: 0.6; > 300: nil | NH/SH/MDR | IRC:73 Table 8 | high | |
| GH-18 | Extra widening, single lane | R ≤ 20: 0.9; 21–40: 0.6; 41–60: 0.6; > 60: nil | ODR/VR | IRC:73 Table 8 | high | |
| GH-19 | Set-back (clearance) for SSD on curves | m = R − (R − d)·cos(S/(2(R−d))) with d = 1.9 m (two-lane); vegetation/obstructions inside must be removed | ALL | IRC:73 / IRC:66 | medium | |
| GH-20 | Compound / reverse curves | ratio of radii ≤ 1.5 (compound); straight ≥ Ls₁+Ls₂ between reverse curves | ALL | IRC:38 | medium | |
| GH-21 | Hairpin bends (hill) | min R inner 14 m; gradient ≤ 2.5 % (1 in 40), max 1 in 50 ... ; roadway widened to 11.5 m two-lane | hill roads | IRC:SP:48; IRC:52 | medium | |
| GH-22 | Chevron/curve warning | warning sign + chevrons where R below ruling for that class | ALL | IRC:67; IRC:SP:88 | medium | |

### 7.3 Sight distances (IRC:73 / IRC:66 / IRC:86)

| ID | Design speed km/h | SSD (m) | ISD (= 2×SSD) (m) | OSD (m) | Conf |
|---|---|---|---|---|---|
| GD-01 | 20 | 20 | 40 | — | high |
| GD-02 | 25 | 25 | 50 | — | high |
| GD-03 | 30 | 30 | 60 | — | high |
| GD-04 | 35 | 40 | 80 | — | high |
| GD-05 | 40 | 45 | 90 | 165 | high |
| GD-06 | 50 | 60 | 120 | 235 | high |
| GD-07 | 60 | 80 | 160 | 300 | high |
| GD-08 | 65 | 90 | 180 | 340 | high |
| GD-09 | 80 | 120 | 240 | 470 | high |
| GD-10 | 100 | 180 | 360 | 640 | high |
| GD-11 | 120 (EXP) | 250 (IRC:SP:99 uses 250–300) | — | — | medium |

Supporting criteria: driver eye height 1.2 m; object height 0.15 m (SSD) / 1.2 m (OSD, ISD) — IRC:73/IRC:66, high. Reaction time 2.5 s; f = 0.40–0.35 (speed-dependent) — high. Two-lane roads to be designed for OSD; ISD where OSD infeasible; SSD absolute minimum (MoRTH compendium circular 302.11, 26-7-1984) — high. Headlight sight distance for valley curves = SSD; headlight height 0.75 m, beam 1° up — high.

### 7.4 Gradients & vertical curves

| ID | Parameter | Threshold | Applies to | Source | Conf |
|---|---|---|---|---|---|
| GV-01 | Ruling / limiting / exceptional gradient, plain & rolling | 3.3 % / 5 % / 6.7 % | NH..VR (IRC:73-1980) | IRC:73 Table | high |
| GV-02 | Mountainous (elev. > 3000 m) | 5 % / 6 % / 7 % | — | IRC:73 | high |
| GV-03 | Steep (up to 3000 m) | 6 % / 7 % / 8 % | — | IRC:73 | high |
| GV-04 | NH manuals (SP:73/84/87) ruling / limiting, plain-rolling | 2.5 % / 3.3 % ; mountainous 5 / 6 ; steep 6 / 7 | 2L/4L/6L NH | IRC:SP:73-2018 Table 2.7 | high |
| GV-05 | Expressway max gradient | 2.5 % (plain), 3 % (rolling), 4–5 % (mountainous) | EXP | IRC:SP:99 | medium |
| GV-06 | Urban max gradient | arterial 4 % (ruling 3 %); collector/local 5–6 %; exceptional 8 % | urban | IRC:86 | medium |
| GV-07 | Minimum gradient for drainage | 0.5 % (1 in 200) kerbed/lined drains; 0.3 % concrete-lined; 1 % unlined | kerbed roads | IRC:73; IRC:SP:50 | high |
| GV-08 | Length limits on steep grades | limiting grade continuous ≤ 2 km (hill roads ≤ 1 km above ruling); exceptional ≤ 100 m | hill | IRC:SP:48 | medium |
| GV-09 | Grade compensation on curves | 30 + R / R %, max 75/R %; not needed for grades < 4 % | hill | IRC:73 | high |
| GV-10 | Summit vertical curve length (L > S) | L = N·S²/4.4 (SSD) ; L = N·S²/9.6 (OSD/ISD) | ALL | IRC:SP:23-1983 | high |
| GV-11 | Valley curve length (L > S) | L = N·S²/(1.5 + 0.035 S) (headlight) | ALL | IRC:SP:23-1983 | high |
| GV-12 | Minimum vertical curve length / grade change not needing curve | 100 km/h: 60 m (0.5 %); 80: 50 m (0.6 %); 65: 40 m (0.8 %); 50: 30 m (1.0 %); 40: 20 m (1.2 %); 35: 15 m (1.5 %); ≤ 30: 15 m (1.5 %) | ALL | IRC:SP:23 Table | medium |
| GV-13 | Vertical clearance over roadway (structures) | 5.5 m (NH/EXP); 5.0 m urban (min 4.5 m legacy); rail over road 5.5 m | ALL | IRC:5 / IRC:SP:84 | high |
| GV-14 | Vertical clearance for FOB over road | 5.5 m | ALL | IRC:103 / IRC:5 | high |

---

## 8. Intersections (IRC:SP:41-1994, IRC:65-2017, IRC:92-2017, IRC:86)

### 8.1 At-grade junctions

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| IN-01 | Intersection angle | 70–110° (ideal 90°); skew < 60° to be realigned | ALL | IRC:SP:41 | high | |
| IN-02 | Corner (kerb) radius — residential/local urban | 4.5–6.0 m | UL | IRC:SP:41; IRC:103 (small radii for ped safety) | medium | |
| IN-03 | Corner radius — collectors / passenger cars | 9 m | UC/USA | IRC:SP:41 | medium | |
| IN-04 | Corner radius — arterials, bus/truck routes | 12–15 m (three-centred compound curves preferred) | UA/NH | IRC:SP:41 | medium | |
| IN-05 | Corner radius — rural NH junctions with trucks/semi-trailers | 15–18 m (up to 30 m with channelising island) | NH/SH rural | IRC:SP:41 | medium | |
| IN-06 | Minimum turning radius (design vehicle) | car 7.3 m; single-unit truck/bus 12.8 m; semi-trailer 13.7 m | — | IRC:SP:41 / IRC:3 | medium | |
| IN-07 | Channelising island minimum area | 4.5 m² urban (7 m² rural desirable); nose offset 0.6–1.0 m from edge; kerb 150 mm, painted (KB-06) | ALL | IRC:SP:41 | medium | |
| IN-08 | Sight triangle, uncontrolled/minor-road approach | minor-road setback 15 m (rural) / 9 m (urban) from major-road edge; distance along major road ≥ SSD of major-road design speed (GD table), desirable 1.5 × SSD | ALL | IRC:SP:41 | medium | no obstruction > 0.9–1.0 m high inside triangle |
| IN-09 | Visibility splay for stop-controlled approach | 4.5 m (medium traffic) / 3.0 m (light) back from edge × SSD along major | minor roads | IRC:35-2015 / IRC:SP:41 | medium | from IRC:35 copy: "x = 4.5 m medium, 3.0 m light side road" |
| IN-10 | Spacing of at-grade intersections | arterial ≥ 500 m (desirable 1 km); NH 4L/6L: no new access within 500 m–2 km of junction; median openings MD-09 | UA/NH | IRC:86; IRC:SP:84 | medium | |
| IN-11 | Turning lanes | 3.0–3.5 m wide; storage ≥ 30 m + taper 1:8 to 1:15 (urban 20 m taper) | UA/NH | IRC:SP:41 | medium | |
| IN-12 | Speed-change lanes at rural junctions | acceleration lane 3.5 m × 100–200 m; deceleration 3.5 m × 70–120 m; tapers 1:15 | NH/SH | IRC:SP:41; IRC:SP:84 | low | |
| IN-13 | Pedestrian crossings at junctions | zebra on every approach ≤ 1 lane width behind stop line; refuge if > 2 lanes per direction; kerb ramps at all corners | urban | IRC:103 | high | |
| IN-14 | Setback of zebra from junction corner | 1–3 m from the kerb return tangent point (parallel to major road) | urban | IRC:35; IRC:103 | low | |
| IN-15 | STOP/GIVE WAY control | STOP where sight distance deficient; GIVE WAY where IN-08 available; markings MK-11/13 plus signs SG-11 | ALL | IRC:SP:41; IRC:67 | high | |
| IN-16 | Lighting at intersections | mandatory lighting at all rural NH junctions and urban junctions, level ≥ 1.5× adjoining road | ALL | IRC:SP:41; IRC:SP:84; IS 1944 | medium | |
| IN-17 | Property access (driveways) on NH | not within 100 m (urban) / 300 m (rural) of a junction; access via service road on 4L/6L | NH | IRC:SP:84 / MoRTH access control guidelines | medium | |
| IN-18 | Rural Y/T junction on NH | minor road meets at 90° over last 30 m; rumble strips + STOP sign + warning sign on major road ("side road") | NH/SH | IRC:SP:41 | medium | |

### 8.2 Roundabouts (IRC:65-2017; legacy IRC:65-1976)

| ID | Parameter | Threshold | Source | Conf | Notes |
|---|---|---|---|---|---|
| RB-01 | Roundabout design speed | 30 km/h urban; 40 km/h rural (circulating 20–30 km/h) | IRC:65-2017 | medium | |
| RB-02 | Inscribed circle diameter (ICD) – mini roundabout | 15–25 m (central island traversable, ≤ 4 m dia painted/domed ≤ 125 mm high) | IRC:65-2017 | low | |
| RB-03 | ICD – urban compact single-lane | 25–36 m | IRC:65-2017 | medium | |
| RB-04 | ICD – urban single-lane | 30–40 m | IRC:65-2017 | medium | |
| RB-05 | ICD – urban double-lane | 40–70 m | IRC:65-2017 | high | |
| RB-06 | ICD – rural single-lane | 35–40 m (up to 45 m) | IRC:65-2017 | medium | |
| RB-07 | ICD – rural double-lane | 55–75 m | IRC:65-2017 | medium | |
| RB-08 | Entry width | single lane 4.0–6.0 m (min 6 m incl. flare in some copies); double lane 7.0–9.0 m (two lanes × 3.5–4.0) | IRC:65-2017 | medium | |
| RB-09 | Circulatory carriageway width | 1.0–1.2 × maximum entry width (single lane 5–6 m; two-lane 8–10 m) | IRC:65-2017 | high | |
| RB-10 | Central island diameter | ICD − 2 × circulatory width; raised, non-traversable, kerb 150 mm, no fixed hazards inside (trees/statues set back ≥ 2 m) | IRC:65-2017 | medium | |
| RB-11 | Splitter island | raised; min width 2.4 m at pedestrian crossing (1.2 m abs.), length ≥ 15 m (urban) / 30 m (rural); nose radii 0.3 m (entry) / 1.0 m (exit) | IRC:65-2017; Indo-HCM 2017 | medium | |
| RB-12 | Entry radius / exit radius | entry 10–30 m (urban ≥ 10 m, rural 20–30 m); exit radius ≥ entry radius | IRC:65-2017 | medium | |
| RB-13 | Entry angle / deflection | 20–60° entry angle; fastest-path radius ≤ 100 m (to keep ≤ 50 km/h) | IRC:65-2017 | low | |
| RB-14 | Weaving section (legacy rotary) | weaving width w = (e₁+e₂)/2 + 3.5 m (6–9 m); weaving length ≥ 4 w (min 45 m rural / 30 m urban); w/L = 0.12–0.40 | IRC:65-1976 | high (legacy) | capacity Qp = 280 w (1+e/w)(1−p/3)/(1+w/L) |
| RB-15 | Pedestrian crossing at roundabout | zebra set back 5–7 m (one vehicle length) from yield line, across splitter island refuge | IRC:65-2017 | medium | |
| RB-16 | Truck apron | 1–4 m wide, mountable kerb 50–75 mm, cross-slope 2–3 % | IRC:65-2017 | low | |
| RB-17 | Circulatory cross slope | 2 % outward (drainage); max superelevation 2–3 % | IRC:65-2017 | medium | |
| RB-18 | Signs & markings at roundabout | GIVE WAY sign + line at every entry; chevron board on central island facing each entry; island kerbs black-yellow; lighting mandatory | IRC:65-2017; IRC:67; IRC:35 | high | |
| RB-19 | Roundabout warrant (volume) | total entering ≤ 3000 veh/h (single lane ≈ 1500–2000 PCU/h); not where entering volume > 5000 PCU/h or pedestrian flow very high | IRC:65 | medium | |

---

## 9. Street lighting (IS 1944 Parts 1&2 – 1970 reaffirmed; SP 72 NLC 2010; IRC:SP:84/87/99)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| LT-01 | Group A1 (important routes, rapid dense traffic — urban arterials/expressways) | E_avg 30 lux; E_min/E_avg ≥ 0.4 | UA/urban EXP | IS 1944 Pt.1 | high | |
| LT-02 | Group A2 (main roads with mixed traffic, arterials/sub-arterials) | 15 lux; uniformity 0.4 | USA/UA | IS 1944 Pt.1 | high | |
| LT-03 | Group B1 (secondary roads with considerable traffic, shopping streets, collectors) | 8 lux; uniformity 0.3 | UC | IS 1944 Pt.1 | high | newer NLC/vendor tables map B1 to 10–15 lux (medium) |
| LT-04 | Group B2 (secondary roads, light traffic) | 4 lux; uniformity 0.3 | UC/UL | IS 1944 Pt.1 | high | |
| LT-05 | Group C (residential, unclassified) | 4 lux; uniformity 0.25–0.3 | UL | IS 1944 Pt.2 | medium | |
| LT-06 | Group D (bridges/flyovers) | as adjoining road (≥ 15 lux typical) | — | IS 1944 Pt.2 | medium | |
| LT-07 | Group E (town/city centres, squares) | 15–30 lux | — | IS 1944 Pt.2 | medium | |
| LT-08 | Pedestrian crossings / conflict areas | ≥ 1.5× adjoining road level; crossings lit from both sides (positive contrast) | ALL | IS 1944; IRC:103 | medium | |
| LT-09 | NH/expressway lighting (where provided: toll plazas, junctions, built-up) | luminance 1.0–1.5 cd/m² (≈ 15–20 lux avg); toll plaza 30–40 lux (IRC:SP:87 quoted 40 lux min) | NH/EXP | IRC:SP:84/87/99; CIE M2/M3 | medium | |
| LT-10 | Mounting height | A1: 10–12 m; A2: 9–10 m; B: 7.5–9 m; C: 6–7.5 m; footpath/pedestrian lighting 4–6 m | ALL | IS 1944; vendor design tables | medium | |
| LT-11 | Spacing / mounting-height ratio | ≤ 3–3.5 (single-side/staggered), ≤ 4–5 (opposite/central twin) ; typical spacing 25–35 m urban arterials | ALL | IS 1944 Pt.1 | medium | |
| LT-12 | Overhang | ≤ 0.25 × mounting height; tilt ≤ 5–15° | ALL | IS 1944 | low | |
| LT-13 | Pole setback from kerb face | ≥ 0.6 m (1.0 m desirable); ≥ clear zone or shielded on high-speed roads; never inside footpath pedestrian zone | ALL | IS 1944; IRC:103; IRC:119 | medium | |
| LT-14 | Pole in median | median ≥ 1.5 m required for central poles (2.0 m with kerb shyness); frangible or barrier-protected if speed ≥ 60 km/h | divided roads | IRC:86; IRC:119 | medium | |
| LT-15 | Glare | cut-off / semi-cut-off luminaires on A1/A2; TI ≤ 10–15 % | ALL | IS 1944; SP 72 | medium | |
| LT-16 | Outage threshold (RSA) | > 10 % lamps out or any two consecutive poles dark = fail; lighting present at all junctions, crossings, bus stops, humps | ALL | IRC:SP:88 practice | low | |
| LT-17 | Lighting in built-up NH sections | mandatory where road passes through town/village, service roads, underpasses, FOBs | NH | IRC:SP:84/87 | medium | |

---

## 10. Crash barriers / roadside safety (IRC:119-2015; MoRTH Sec. 800 cl. 810; IRC:SP:84/87/99)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| RS-01 | Clear zone width (from edge of travelled way), design speed ≤ 60 km/h | 3.0 m | ALL | IRC:119-2015 Fig.5 (as quoted in IIT-D TRIPP training) | medium | |
| RS-02 | Clear zone, 80 km/h | 4.5–7.0 m (depends on AADT and fill slope) | NH/SH | IRC:119-2015 | medium | |
| RS-03 | Clear zone, 100 km/h | 7.0–9.0 m (9 m typical) | NH | IRC:119-2015 | medium | |
| RS-04 | Clear zone, 120 km/h | 9–11 m | EXP | IRC:119-2015 / IRC:SP:99 | low | |
| RS-05 | Recoverable slope | ≤ 1V:4H (1:3 critical/non-recoverable → barrier) | ALL | IRC:119-2015 | high | |
| RS-06 | Embankment barrier warrant | fill height ≥ 3 m (any slope steeper than 1:4); any height where slope steeper than 1:3 and water/drop within clear zone | NH/EXP | IRC:119-2015 cl. on embankment warrants | high | |
| RS-07 | Fixed-object warrant | non-traversable hazard within clear zone: trees ≥ 100 mm trunk, poles, culvert headwalls, piers, drains deeper than 0.6 m, drops ≥ 1 m, water ≥ 0.6 m deep → remove/relocate/make frangible/shield | ALL | IRC:119-2015 Table 2 | high | |
| RS-08 | W-beam barrier rail height (top of rail above ground/shoulder) | 710 mm (MoRTH 810 drawing; ±25 mm) — many references quote 700 mm | NH/SH | MoRTH Sec. 810; IRC:119 | medium | post top ~ 850 mm |
| RS-09 | W-beam post spacing | 2.0 m c/c standard; 1.0 m (or 1.5 m) near hazards/transitions | ALL | MoRTH 810 | high | |
| RS-10 | W-beam section | 3 mm thick, 312 mm wide beam; posts 150×75×5 mm channel (or 75×150 I/C), 1.8 m long embedded ≥ 1.1 m; spacer blocks; galvanised 550 g/m² | ALL | MoRTH 810 | high | |
| RS-11 | Thrie-beam rail height | 810–850 mm | high-risk / high truck volume | MoRTH 810; IRC:119 | medium | |
| RS-12 | Concrete (NJ/F-shape) median barrier height | 810 mm standard; 900 mm (modified); 1100–1550 mm high containment on bridges/where trucks | medians, bridges | IRC:119; IRC:5/6; IRC:SP:84 | medium | |
| RS-13 | Barrier lateral offset | ≥ 0.5 m beyond paved shoulder edge (1.0 m desirable); deflection/working width 1.0–1.5 m behind W-beam kept clear | ALL | IRC:119 | medium | |
| RS-14 | Barrier length of need / runout length | upstream extension L_R: 100 km/h ≈ 100–130 m; 80 km/h ≈ 75–100 m; 60 km/h ≈ 50–70 m (AASHTO RDG method adopted) | NH | IRC:119-2015 | low | |
| RS-15 | Barrier end treatments | crash-tested energy-absorbing terminal (ET/ELT type) on high-speed roads; alternative: flare 1:15–1:30 and anchor in back-slope; blunt/fishtail ends prohibited; turned-down (ramped) ends only ≤ 60 km/h | ALL | IRC:119-2015 | medium | |
| RS-16 | Transition W-beam → concrete / bridge rail | nested beam + post spacing reduced to 1.0 m (≥ 3 posts) over ≥ 8 m | ALL | IRC:119-2015 (transition clause) | high | |
| RS-17 | Barrier on bridge approaches | approach guardrail ≥ 30 m (rural) connected to parapet; parapet/crash barrier min 1.1 m (pedestrian railing 1.1 m; combination 1.5 m) | bridges/culverts | IRC:5-2015; IRC:119 | medium | |
| RS-18 | Barrier delineation | retroreflective delineators (yellow/white; red on left) every 10–20 m on rail; hazard marker on terminals | ALL | IRC:79-2019 | medium | |
| RS-19 | Barrier condition | damaged/deformed section, missing posts/bolts, height < 600 mm or > 800 mm (W-beam) = fail | ALL | IRC:SP:88 | medium | |
| RS-20 | Hill road parapets | 0.6 m high RCC/stone parapet with 150 mm reflectors; crash barrier on valley side where fill > 3 m | hill roads | IRC:SP:48 | medium | |
| RS-21 | Culvert headwalls/parapets within clear zone | extend culvert or shield; parapet ≥ 0.6 m painted black-white/hazard marker | NH/SH | IRC:119; IRC:SP:84 | medium | |
| RS-22 | Utility poles / trees | outside clear zone or shielded; trees within 1 m of carriageway edge on NH = hazard; frangible/breakaway poles where unshielded | ALL | IRC:119 | medium | |
| RS-23 | Open drains adjacent to carriageway | depth > 0.6 m or vertical sides within clear zone → cover or shield; urban: covered drains flush | ALL | IRC:119; IRC:SP:50 | medium | |
| RS-24 | Motorcyclist protection | add-on under-run rail on W-beam at curves R < 250 m where 2W > 20 % | NH/SH | IRC:119-2015 (recommendation) | low | |
| RS-25 | Pedestrian railing on footpath along barrier | separate 1.1 m railing; barrier not to be used as footpath edge | urban NH | IRC:103 | low | |

---

## 11. Pavement condition — potholes, roughness, PCI (IRC:82-2015/2023, IRC:SP:16-2019, MoRTH Sec. 900/3004, ASTM D6433)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| PV-01 | Pothole definition | bowl-shaped hole ≥ 150 mm dia and ≥ 25 mm deep through surfacing | ALL | IRC:82-2015 cl. on potholes | medium | |
| PV-02 | Pothole severity – Low | depth < 25 mm (dia < 200 mm) | ALL | IRC:82-2015 severity descriptors / ASTM D6433 | medium | |
| PV-03 | Pothole severity – Medium | depth 25–50 mm (dia 200–450 mm) | ALL | IRC:82-2015 / ASTM D6433 | medium | |
| PV-04 | Pothole severity – High | depth > 50 mm or dia > 450 mm | ALL | IRC:82-2015 / ASTM D6433 | medium | |
| PV-05 | Pavement condition rating (IRC:82-2015 Table) – Good | cracking < 5 % area; ravelling < 1–5 %; potholes < 0.5 % area (≈ none); rut depth < 5 mm; patching < 5 %; rating 2.1–3.0 | NH/SH | IRC:82-2015 Table 1 | medium | |
| PV-06 | Condition – Fair | cracking 5–10 %; potholes 0.5–1 %; rut 5–10 mm; patching 5–10 %; rating 1.1–2.0 | NH/SH | IRC:82-2015 Table 1 | medium | |
| PV-07 | Condition – Poor | cracking > 10 %; potholes > 1 % area; rut depth > 10 mm (> 20 mm high severity); patching > 10 %; rating ≤ 1.0 | NH/SH | IRC:82-2015 Table 1 | medium | |
| PV-08 | Rut depth triggers | > 10 mm poor; > 20 mm high severity / hydroplaning risk; NHAI O&M: ≥ 5 mm (NH concessions) requires correction | NH | IRC:82; NHAI MCA Schedule K | medium | |
| PV-09 | Roughness (IRI) bands, bituminous concrete | Good < 2.55 m/km; Fair 2.55–3.30; Poor > 3.30 m/km | NH/SH | IRC:82-2023 Table | high (2023) | |
| PV-10 | Roughness (BI, bump integrator) legacy bands | Good < 2000 mm/km; Fair 2000–3000; Poor > 3000 (overlay trigger ~3000–3500) | ALL | IRC:82-2015; IRC:SP:16 | medium | BI ≈ 630 × IRI^1.12 |
| PV-11 | New construction acceptance, NH BC surface | IRI ≤ 2.0 m/km on ≥ 80 % length, no 100 m segment > 2.5 m/km (BI ≤ 1500–1800 mm/km) | NH new/renewed | IRC:SP:16-2019; MoRTH 902 | medium | |
| PV-12 | Longitudinal profile, 3 m straight edge (max undulation) | BC/SDBC 3 mm; DBM 6 mm; BM/WMM/WBM 8–10 mm; GSB 15 mm; subgrade 24 mm | new work | MoRTH Table 900-1 | high | |
| PV-13 | Cross profile (camber) tolerance | ± 4 mm (BC) under 3 m template | new work | MoRTH 902 | medium | |
| PV-14 | Edge break / edge drop | edge break > 150 mm width or drop > 50 mm between carriageway and shoulder = hazard; repair priority | ALL | IRC:82; iRAP | medium | |
| PV-15 | Skid resistance (wet) | BPN ≥ 55 (NH); macrotexture (sand patch) ≥ 1.0 mm (0.6 mm min) ; SCRIM SFC ≥ 0.45 | NH/EXP | IRC:82-2023; MoRTH concession specs | medium | |
| PV-16 | PCI (ASTM D6433) classes | 86–100 Good; 71–85 Satisfactory; 56–70 Fair; 41–55 Poor; 26–40 Very poor; 11–25 Serious; 0–10 Failed | ALL (used by ULBs/NHAI) | ASTM D6433 | high | IRC:82 mapping: Good ≈ PCI > 70, Fair 55–70, Poor < 55 (medium) |
| PV-17 | Rural road PCI (IRC:SP:20 / PMGSY) | 5-point scale: 5 very good (IRI < 4), 4 good (4–6), 3 fair (6–8), 2 poor (8–10), 1 very poor (> 10) | VR/ODR | PMGSY OMMAS manual; IRC:SP:20 | medium | |
| PV-18 | Pothole repair response time – NH concessions | emergency/safety defects 24–48 h; potholes within 48 h of reporting (monsoon); MCA Schedule K "no pothole shall remain" | NH (BOT/HAM/O&M) | NHAI Model Concession Agreement Sch. K/L; MoRTH Manual for Maintenance of Roads | medium | |
| PV-19 | Pothole repair – municipal norms (typical) | 48 h (BMC), 24–72 h others; monsoon preparedness circulars | urban | municipal policies (BMC 2018) | low | |
| PV-20 | Pothole repair method | cut to rectangular, vertical sides, tack coat, fill with hot mix/cold mix (MoRTH 3004); temporary cold-mix in monsoon | ALL | MoRTH cl. 3004; IRC:82; IRC:116 (cold mix) | high | |
| PV-21 | Patch quality | flush ± 6 mm with surrounding; no ponding | ALL | IRC:82 | medium | |
| PV-22 | Ravelling / loss of aggregate | > 10 % area = poor; surface renewal cycle 4–5 yr (BC/SDBC), 2–3 yr (surface dressing) | ALL | IRC:82-2015 | medium | |
| PV-23 | Cracking severity | hairline < 3 mm; medium 3–6 mm; wide > 6 mm; alligator cracking > 10 % area → strengthening | ALL | IRC:82 | medium | |
| PV-24 | Shoving/corrugation, bleeding | any at junctions/humps = fail in RSA (skid) | ALL | IRC:82 | low | |
| PV-25 | Utility cut reinstatement | flush within ± 6 mm; full-depth; no settlement > 10 mm | urban | IRC:98 / IRC:SP:50 | low | |
| PV-26 | Manhole covers / inlets in carriageway | flush ± 6 mm; heavy-duty (D400); not in wheel path where avoidable | urban | IRC:SP:50; IS 1726 / EN 124 | medium | |
| PV-27 | Water ponding on carriageway | depth > 25 mm or area > 1 m² after rain = drainage failure | ALL | IRC:SP:42/50 | low | |

---

## 12. Drainage & cross slope (IRC:SP:42-2014, IRC:SP:50-2013, IRC:73, IRC:86)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| DR-01 | Camber – cement concrete & high-type bituminous (BC/SDBC) | 1.7 % (1 in 60) low rainfall – 2.0 % (1 in 50) high rainfall | ALL | IRC:73 Table; IRC:86 | high | |
| DR-02 | Camber – thin bituminous (surface dressing, premix) | 2.0–2.5 % (1 in 50 – 1 in 40) | MDR/ODR/VR | IRC:73 | high | |
| DR-03 | Camber – WBM / gravel | 2.5–3.0 % (1 in 40 – 1 in 33) | ODR/VR | IRC:73 | high | |
| DR-04 | Camber – earth roads | 3.0–4.0 % (1 in 33 – 1 in 25) | VR | IRC:73 | high | |
| DR-05 | Urban road cross slope | 2.0 % (bituminous), 1.7–2.0 % concrete; one-way cross-fall on divided roads | urban | IRC:86 | high | |
| DR-06 | Earth shoulder cross slope | ≥ 0.5 % steeper than pavement; min 3 %, max 5 % | ALL | IRC:SP:50; IRC:73 | high | |
| DR-07 | Paved shoulder cross slope | same as carriageway | ALL | IRC:SP:73/84 | high | |
| DR-08 | Footpath cross slope | 1.5–2.5 % toward carriageway/drain | urban | IRC:103 | medium | |
| DR-09 | Minimum longitudinal gradient (kerbed) | 0.5 % (0.3 % with lined drain) | urban | IRC:86; IRC:SP:50 | high | |
| DR-10 | Kerb inlet / gully spacing | 20 m c/c reasonable (adjust to gradient); inlets at all low points and upstream of crossings | urban | IRC:SP:50-2013 (cited in SP:42) | high | |
| DR-11 | Max water spread on carriageway (design) | ≤ 1.5 m from kerb (≤ half outer lane) for 2-yr storm | urban | IRC:SP:50 | medium | |
| DR-12 | Design storm return period | urban road drains 2 yr (5 yr arterials, 10 yr underpasses/depressed sections); cross-drainage 25–50 yr (culverts), 100 yr bridges | ALL | IRC:SP:50; IRC:SP:42; IRC:SP:13 | medium | |
| DR-13 | Drain covers in urban footpaths | drains under footpath covered with precast RCC slabs flush with footpath surface; no open drains in pedestrian zone; openings ≤ 13–25 mm, slots perpendicular to travel (cycle safe) | urban | IRC:SP:50-2013; IRC:103 | medium | |
| DR-14 | Open side drains on rural roads | trapezoidal, ≥ 0.6 m deep, side slopes 1:1 to 1.5:1; if within clear zone on NH → covered/shielded (RS-23) | rural | IRC:SP:42 | medium | |
| DR-15 | Gully gratings in carriageway | heavy duty; flush ± 6 mm; hinged/locked | urban | IRC:SP:50 | medium | |
| DR-16 | Median drainage | depressed median drains at ≤ 100 m inlets; raised median kerb weep holes | divided | IRC:SP:84 | low | |
| DR-17 | Subsurface drainage | subgrade ≥ 0.6–1.0 m above HFL; GSB daylighted or edge drains | ALL | IRC:SP:42; IRC:37 | medium | |
| DR-18 | Ponding/flooding as hazard | standing water on carriageway/footpath after rain → RSA fail; identify low spots | ALL | IRC:SP:88 | high | |
| DR-19 | Culvert/drain cover damage | missing/broken slab or grating = critical hazard (pedestrian fall) | urban | IRC:SP:88 practice | high | |

---

## 13. Bus stops, parking, encroachment (IRC:80-1981/2020, IRC:SP:12-2015, IRC:103, IRC:86)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| BP-01 | Bus bay length (per bus) | 18 m for one bus (multiples of 18 m for more) | NH/SH two-lane | IRC:80-2020 (and 1981) | high | |
| BP-02 | Bus bay entry taper | 1:12, ~60 m (restricted: 1:5, 25 m exit) ; overall lay-by 103 m (restricted 53 m) with 18 m bay | NH/SH | IRC:80-2020 | high | |
| BP-03 | Bus bay width | 3.0 m min; 3.5 m desirable (plus 0.5 m kerb shyness) | ALL | IRC:80 | medium | |
| BP-04 | Bus bay location vs junction | ≥ 75 m downstream (far side) of junction on rural highways; urban: far side ≥ 25–30 m, never within junction functional area | ALL | IRC:80; IRC:SP:41 | medium | |
| BP-05 | Bus stop not on curve/crest | sight distance ≥ SSD both directions; not within 100 m of sharp curve/hump | ALL | IRC:80 | medium | |
| BP-06 | Bus shelter setback & footpath | shelter ≥ 0.5 m behind kerb; footpath clear width ≥ 1.8 m maintained behind/through shelter; 3.0 m total footpath at stops | urban | IRC:103 | medium | |
| BP-07 | Bus stop boarding kerb height | 150 mm (low-floor compatible 300–380 mm on BRT) | urban | IRC:103; BRT guidelines | low | |
| BP-08 | Bus stop marking | "BUS STOP" yellow box 18–27 m; no parking 15 m either side | urban | IRC:35; IRC:SP:12 | low | |
| BP-09 | Opposite bus stops | staggered: tail-to-tail ≥ 30 m apart on undivided roads | ALL | IRC:80 | medium | |
| BP-10 | Parking bay – car (perpendicular/angle) | 2.5 m × 5.0 m | urban | IRC:SP:12-2015; IRC:35 | medium | |
| BP-11 | Parking bay – car (parallel) | 2.5 m × 5.5–6.0 m (lane 2.5 m wide, 2.0 m abs. min) | urban | IRC:SP:12-2015 | medium | |
| BP-12 | Parking bay – two-wheeler | 1.0 m × 2.0 m (0.9–1.0 × 2.0) | urban | IRC:SP:12-2015 | medium | |
| BP-13 | Accessible (disabled) parking bay | 3.6 m wide (× 5.0 m), nearest to entrance, kerb ramp | urban | IRC:SP:12-2015 | high | |
| BP-14 | Parking space per car (gross) | 20–36 m² (Table 6.1); ECS 23 m² open, 28 m² covered, 32 m² basement (NBC/URDPFI) | urban | IRC:SP:12-2015 Table 6.1; URDPFI 2014 | medium | |
| BP-15 | Aisle width | 90° parking 6.0–7.0 m; 60° 5.0 m; 45° 3.5–4.0 m; parallel 3.5 m one-way | off-street/on-street | IRC:SP:12 | medium | |
| BP-16 | No parking near intersection | within 15 m of junction (functional area; 9 m abs. min urban) | ALL | IRC:SP:12-2015; MV (Driving) Regulations 2017 reg. 22 | medium | |
| BP-17 | No parking near pedestrian crossing | within 5–6 m before zebra (sight line); 15 m of bus stop; within 10 m of fire hydrant | urban | IRC:SP:12; MV Driving Regs 2017 | low | |
| BP-18 | No parking on | footpaths, cycle tracks, bridges, within tunnels, on curves/crests with SD < SSD, in front of gates/hospitals | ALL | MV (Driving) Regulations 2017; IRC:SP:12 | high | |
| BP-19 | On-street parking permitted only where | residual carriageway ≥ 2 lanes (≥ 7 m) undivided or ≥ 2 lanes per direction divided; speed ≤ 50 km/h | urban | IRC:SP:12-2015 | medium | |
| BP-20 | Footpath encroachment rule | any vendor/structure/parked vehicle reducing clear width below 1.8 m (or below land-use minimum PD-02..05) = encroachment | urban | IRC:103; Street Vendors Act 2014 (vending zones) | high | |
| BP-21 | Hawker/vending zone | in furniture zone only, min 1.8 m pedestrian zone retained; no vending within 50 m of junction / 100 m of school gate (typical municipal) | urban | IRC:103; ITDP; municipal bylaws | low | |
| BP-22 | Truck lay-by on NH | 20 m × 3 m parking bay every 20–30 km (IRC:SP:84: "parking bay 20 m × 3 m"), taper 1:15 | NH 4L/6L | IRC:SP:84-2019 | medium | |
| BP-23 | Auto/IPT stands | marked bays ≥ 15 m from junction, not at bus stop | urban | IRC:SP:12 | low | |

---

## 14. Work zones (IRC:SP:55-2014; MoRTH Sec. 112)

| ID | Parameter | Threshold | Applies to | Source | Conf | Notes |
|---|---|---|---|---|---|---|
| WZ-01 | Zone structure | advance warning zone → approach transition (taper) → buffer → activity/work zone → terminal transition → end | ALL | IRC:SP:55-2014 ch.4 | high | |
| WZ-02 | Advance warning zone length, urban low speed (≤ 50 km/h) | ≥ 30–100 m; first sign ("Men at work / Road work ahead") ≥ 50 m before taper | UL/UC | IRC:SP:55-2014 Table 4.1 | medium | |
| WZ-03 | Advance warning zone, urban high speed / rural ≤ 80 km/h | 100–300 m (signs at ~300, 200, 100 m) | UA/SH/MDR | IRC:SP:55-2014 | medium | |
| WZ-04 | Advance warning zone, NH/expressway ≥ 80–100 km/h | 500 m – 1.5 km (sign series at 1000/500/200/100 m; expressway up to 2 km) | NH/EXP | IRC:SP:55-2014 | medium | |
| WZ-05 | Approach (merging) taper length | L = W·S²/155 for S ≤ 60 km/h; L = 0.6·W·S for S > 60 km/h (W = lane shift m, S = speed km/h). W = 3.5: 40 → 36 m; 50 → 56 m; 60 → 81 m; 80 → 168 m; 100 → 210 m | ALL | IRC:SP:55-2014 Table 4.1 (metric MUTCD basis) | medium | |
| WZ-06 | Shifting taper | 0.5 L | ALL | IRC:SP:55 | medium | |
| WZ-07 | Shoulder taper | 0.33 L | ALL | IRC:SP:55 | medium | |
| WZ-08 | Terminal (downstream) taper | 30 m per lane (min 15 m) | ALL | IRC:SP:55-2014 Table 4.2 | medium | |
| WZ-09 | One-lane two-way taper (flagman/signal) | 15–30 m max | ALL | IRC:SP:55 | medium | |
| WZ-10 | Longitudinal buffer space | ≥ 30 m (urban) ; 50–100 m (≥ 80 km/h) ; = SSD of work-zone speed | ALL | IRC:SP:55 | medium | |
| WZ-11 | Lateral buffer | 0.6–1.0 m between traffic edge and work area/ barrier | ALL | IRC:SP:55 | medium | |
| WZ-12 | Minimum lane width through work zone | 3.0 m (2.75 m abs. urban low speed); 3.5 m desirable on NH | ALL | IRC:SP:55 | medium | |
| WZ-13 | Work-zone speed limit | reduce in steps ≤ 20 km/h; 30–40 km/h urban; 50 km/h NH; signs at start and repeated every 500 m | ALL | IRC:SP:55 | medium | |
| WZ-14 | Cone height | 750 mm min (≥ 60 km/h, night) ; 450–500 mm permitted ≤ 50 km/h daytime; 1000 mm drums on high-speed | ALL | IRC:SP:55-2014 Table 5.9 / devices chapter | medium | two white retroreflective bands 100–150 mm |
| WZ-15 | Cone spacing – taper | ≈ 0.3 × S m (S km/h): 3–5 m urban (≤ 50), 9–12 m (80), 15–20 m (100) | ALL | IRC:SP:55-2014 Table 5.9 | low | |
| WZ-16 | Cone spacing – tangent (along activity area) | 2 × taper spacing; 9–12 m urban, 20–30 m highways; night ≤ 12 m | ALL | IRC:SP:55-2014 Table 5.9 | low | |
| WZ-17 | Barricades | Type I/II/III, 1.0–1.2 m high, striped orange/white or red/white 45° retroreflective 150 mm; Type III (full closure) ≥ 1.2 m × 3 panels | ALL | IRC:SP:55 | medium | |
| WZ-18 | Signs | per IRC:67 sizes (SG-05..08) with yellow/fluorescent orange background, Type IV sheeting minimum; "Road work ahead", "Diversion", "Speed limit", "End of work" | ALL | IRC:SP:55; IRC:67 | medium | |
| WZ-19 | Night-time | flashing/steady amber warning lamps on first cone/barricade and every 10–12 m in taper; floodlighting of work area; retroreflective jackets | ALL | IRC:SP:55 | medium | |
| WZ-20 | Flagmen | at one-lane two-way sections, with STOP/SLOW paddles 600 mm, visible ≥ 150 m | ALL | IRC:SP:55 | medium | |
| WZ-21 | Pedestrian route through work zone | continuous, ≥ 1.2 m (1.5 m desirable), protected by barricade, ramps 1:12 | urban | IRC:SP:55; IRC:103 | medium | |
| WZ-22 | Temporary pavement markings | within 24 h of surfacing; removal of conflicting old markings | ALL | IRC:SP:55 | medium | |
| WZ-23 | TMA / shadow vehicle for mobile works | required ≥ 60 km/h roads | NH/EXP | IRC:SP:55-2014 | medium | |
| WZ-24 | Excavation protection | open trench fenced with ≥ 1.0 m barricade both sides, lit at night; plates over trench on carriageway | urban | IRC:SP:55; IRC:98 | high | |
| WZ-25 | Unprotected work zone (no signs/cones) | = critical RSA finding | ALL | IRC:SP:88 | high | |

---

## 15. School zones, hospital zones, speed limits

### 15.1 MoRTH notification S.O. 1522(E), 6 April 2018 (maximum speeds, km/h)

| ID | Vehicle category | Expressway (access-controlled) | 4-lane+ divided carriageway | Within municipal limits | Other roads | Conf |
|---|---|---|---|---|---|---|
| SL-01 | M1 (cars, ≤ 8 seats + driver) | 120 | 100 | 70 | 70 | high |
| SL-02 | M2 / M3 (buses, > 9 seats) | 100 | 90 | 60 | 60 | high |
| SL-03 | N (goods vehicles) | 80 | 80 | 60 | 60 | high (ends) / medium (middle) |
| SL-04 | Motorcycles / two-wheelers | 80 (only where permitted) | 80 | 60 | 60 | high |
| SL-05 | Quadricycles | not permitted | 60 | 50 | 50 | medium |
| SL-06 | Three-wheelers | not permitted | 50 | 50 | 50 | medium |
| SL-07 | Enforcement tolerance | no cognizance if detected speed within 5 % of limit | — | — | — | high |
| SL-08 | Status note | notification sets ceilings; States/local authorities may set lower limits; a High Court order against the 100/120 limits was reported — treat posted limits as governing | — | — | — | medium |
| SL-09 | Speed governors (CMVR rule 118) | transport vehicles (M2/M3/N2/N3, except specified) limited to 80 km/h; school buses 40 km/h (Supreme Court / CMVR) | — | — | — | medium |

### 15.2 School / hospital zones (IRC:SP:32-2023, IRC:99-2018, MV (Driving) Regulations 2017)

| ID | Parameter | Threshold | Source | Conf |
|---|---|---|---|---|
| SZ-01 | Speed limit near schools | 25 km/h (or lower if posted) | MV (Driving) Regulations 2017 reg. 16(5); IRC:99-2018 | high |
| SZ-02 | Speed limit near hospitals | 30 km/h | IRC:99-2018 | high |
| SZ-03 | School zone extent | "school proximal zone" radius ~100–200 m from gate (table by road class in IRC:SP:32-2023); transition zone 50–100 m each side | IRC:SP:32-2023 | low |
| SZ-04 | Required devices in school zone | "School Ahead" cautionary sign (siting per SG-05..07), speed-limit 25 sign at zone entry, "SCHOOL" carriageway text/ zone marking, zebra (raised table where speed > 30) at gate, rumble strips/ hump (TC-03/05) before crossing, pedestrian guardrail 1.0–1.1 m along footpath at gate (PD-25), footpath ≥ 1.8 m, no parking within 50–100 m of gate, lighting | IRC:SP:32-2023; IRC:99; IRC:103; IRC:67 | medium |
| SZ-05 | Flashing school-zone beacons | amber flashers during school hours recommended | IRC:SP:32 | low |
| SZ-06 | School bus bay / drop-off | off-carriageway drop-off bay ≥ 18 m; no reversing | IRC:SP:32; IRC:80 | low |
| SZ-07 | Hospital zone devices | "Hospital" informatory sign, no-horn sign, 30 km/h, zebra/refuge at entrance, no humps on emergency route | IRC:67; IRC:99 | medium |
| SZ-08 | Posted-speed consistency check | posted limit ≤ design-speed-based limit for road class (GS table) and ≥ 85th-percentile − 10 km/h; limits not to change by > 20 km/h in one step | IRC:SP:88; IRC:99 | medium |
| SZ-09 | Urban default (where unposted) | 50 km/h design/operating target on arterials with pedestrians; 30 km/h local streets | IRC:86-2018; IRC:99 | medium |

---

## 16. iRAP star-rating attributes and IRC:SP:88-2019 Stage-5 (existing road) checklist

### 16.1 iRAP Coding Manual (v5.x, drive-on-left) attribute list

Coded per 100 m segment from geo-referenced imagery. Metadata attributes: 1 Coder name; 2 Coding date; 3 Road survey date; 4 Image reference; 5 Road name; 6 Section; 7 Distance; 8 Length; 9 Latitude; 10 Longitude; 11 Landmark; 12 Comments; 13 Carriageway label (A/B/undivided); 14 Upgrade cost (low/medium/high). Confidence for list: high (names from manual; some version-dependent).

| # | Attribute | Codes / thresholds (abridged) | Relevance to video audit |
|---|---|---|---|
| 15 | Motorcycle observed flow | none / 1–25 % / 26–50 % / > 50 % of traffic | observed |
| 16 | Bicycle observed flow | none / 1–3 / 4–7 / ≥ 8 per segment | observed |
| 17–18 | Pedestrian observed flow along road – driver-side / passenger-side | none / 1–3 / 4–7 / ≥ 8 | observed |
| 19 | Pedestrian observed flow across road | none / 1–3 / 4–7 / ≥ 8 | observed |
| 20–21 | Land use – driver-side / passenger-side | undeveloped, farming, residential, commercial, industrial, educational | map/visual |
| 22 | Area type | urban / rural | |
| 23 | Speed limit | bands ≤ 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, ≥ 130 km/h | posted sign detection |
| 24–25 | Motorcycle / truck speed limit | same bands | |
| 26 | Differential speed limits | yes/no | |
| 27 | Median type | centreline only; wide centreline (0.3–1 m); central hatching (> 1 m); physical median < 1 m / 1–5 m / 5–10 m / 10–20 m / > 20 m; safety barrier (metal/concrete/wire rope); continuous central turning lane; one-way; motorcycle lane barrier | median detection |
| 28 | Centreline rumble strips | present / not present | |
| 29 / 31 | Roadside severity – distance (driver-side / passenger-side) | 0 – < 1 m; 1 – < 5 m; 5 – < 10 m; ≥ 10 m | clear-zone check RS-01..04 |
| 30 / 32 | Roadside severity – object (driver / passenger side) | safety barrier (metal, concrete, wire rope, motorcycle-friendly); aggressive vertical face; upward slope (rollover gradient 15–75°); upward slope < 15°; deep drainage ditch; downward slope; cliff; tree ≥ 10 cm dia; sign/post/pole ≥ 10 cm; rigid structure/bridge/building; semi-rigid structure; unprotected barrier end; large boulders ≥ 20 cm; none | hazard detection |
| 33 | Shoulder rumble strips | present / not present | |
| 34–35 | Paved shoulder – driver-side / passenger-side | wide ≥ 2.4 m; medium 1.0 – < 2.4 m; narrow 0 – < 1.0 m; none | SH-09..14 |
| 36 | Intersection type | merge lane; roundabout; 3-leg (unsignalised / signalised, with/without protected turn lane); 4-leg (same variants); mini roundabout; railway crossing (active/passive); median crossing point (informal/formal); none | |
| 37 | Intersection channelisation | present / not present | |
| 38 | Intersecting road volume | bands ≤ 100 … > 15 000 veh/day | |
| 39 | Intersection quality | adequate / poor | |
| 40 | Property access points | none; commercial access 1+; residential access 1–2 / 3+ | |
| 41 | Number of lanes | 1, 2, 3, 4+, 2+1 | |
| 42 | Lane width | wide ≥ 3.25 m; medium 2.75 – < 3.25 m; narrow 0 – < 2.75 m | CW-01..03 |
| 43 | Curvature | straight/gently curving; moderate (R 200–500 m); sharp (R 100–200 m); very sharp (R < 100 m) | GH table |
| 44 | Quality of curve | adequate / poor / not applicable | signs, delineation, SD |
| 45 | Grade | 0 – < 7.5 %; 7.5 – < 10 %; ≥ 10 % | GV table |
| 46 | Road condition | good / medium / poor | PV table |
| 47 | Skid resistance / grip | sealed – adequate / medium / poor; unsealed – adequate / poor | PV-15 |
| 48 | Delineation | adequate / poor | MK/SG-38 |
| 49 | Street lighting | present / not present | LT table |
| 50 | Pedestrian crossing facilities – inspected road | grade-separated; signalised with refuge; signalised without refuge; unsignalised marked with refuge; unsignalised marked without refuge; refuge only; raised unsignalised with/without refuge; no facility | PD-17..28 |
| 51 | Pedestrian crossing quality | adequate / poor | |
| 52 | Pedestrian crossing facilities – intersecting road | same codes as 50 | |
| 53 | Pedestrian fencing | present / not present | PD-34 |
| 54 | Speed management / traffic calming | present / not present | TC table |
| 55 | Vehicle parking | none; one side; both sides | BP table |
| 56–57 | Sidewalk – driver-side / passenger-side | physical barrier; non-physical separation ≥ 3 m / 1 – < 3 m / 0 – < 1 m; informal path ≥ 1 m / 0 – < 1 m; none | PD-01..06 |
| 58 | Service road | present / not present | |
| 59 | Facilities for motorised two-wheelers | exclusive lane (one-way/two-way); inclusive lane; none | |
| 60 | Facilities for bicycles | off-road path; on-road lane; shared path; signed shared roadway; none | CW-16 |
| 61 | Roadworks | no; minor; major | WZ table |
| 62 | Sight distance | adequate / poor | GD table |
| 63 | Vehicle flow (AADT) | numeric | |
| 64 | Motorcycle % | numeric | |
| 65–68 | Pedestrian peak-hour flows (across / along DS / along PS); bicycle peak-hour flow | numeric | |
| 69–70 | Operating speed 85th percentile / mean | numeric | |
| 71 | Roads that cars can read | yes/no (machine-readable markings/signs) | |
| 72–75 | Star-rating policy targets (vehicle occupant / motorcyclist / pedestrian / bicyclist) | 1–5 | |
| 76 | Annual fatality growth multiplier | numeric | |
| 77 | School zone warning | none; sign only; flashing beacons; school crossing supervisor at present | SZ table |
| 78 | School zone crossing supervisor | present / not present | |

Star-rating score bands (SRS, iRAP v3 methodology, medium confidence): vehicle occupants 5★ 0–2.5, 4★ > 2.5–5, 3★ > 5–12.5, 2★ > 12.5–22.5, 1★ > 22.5; motorcyclists / pedestrians / bicyclists 5★ 0–5, 4★ > 5–15, 3★ > 15–40, 2★ > 40–90, 1★ > 90. India target (MoRTH/NHAI): ≥ 3★ for all users on NHs/expressways (IndiaRAP).

### 16.2 IRC:SP:88-2019 — Stage-5 "Road Safety Audit of Existing Roads" checklist (Section 7.5 / Checklist 5)

The manual provides one checklist per stage and states auditors are not limited to listed concerns. Wording below is a faithful paraphrase of the IRC:SP:88 (2010 → 2019) existing-roads checklist structure (medium confidence on exact wording; high confidence on topics). Each item is phrased as the audit question and mapped to KB rule IDs.

**5.1 Road function, classification and general**
1. Is the road's actual use (traffic mix, speeds, pedestrian activity, land use) consistent with its design class and posted speed? (GS, SL, SZ-08)
2. Have crash records / black spots been reviewed and visited on site? Are previous audit recommendations implemented?
3. Is the route consistent (no abrupt changes in standard, width, surface type)? (CW, SH)
4. Are stray animals / cattle an observed hazard?

**5.2 Cross-section**
5. Are lane widths adequate for the vehicle mix and speed? (CW-01..11)
6. Are shoulders of adequate width, paved/compacted, flush with carriageway, free of drop-offs? (SH-08..17)
7. Is the median adequate, with no gaps allowing unsafe crossing; are median openings properly designed and spaced? (MD-01..10)
8. Are kerbs of appropriate type and height, visible (painted) at night? (KB-01..06)
9. Is the road width continuous across bridges/culverts (no narrow structures without warning)? (RS-17, RS-21)

**5.3 Alignment and sight distance**
10. Is stopping sight distance available throughout, including at crests, curves and junctions? (GD-01..11, GH-19)
11. Are sharp curves (below ruling radius) adequately signed, delineated and superelevated? (GH-04..13, SG-40)
12. Are there dangerous combinations (curve at crest, curve after long tangent, reverse curves without transition)? (GH-20)
13. Are gradients consistent with class; are escape/climbing lanes needed? (GV)
14. Is roadside vegetation/hoarding obstructing sight lines? (SG-23, IN-08)

**5.4 Intersections**
15. Is the junction layout clear and conspicuous to approaching drivers from each leg at the required distance?
16. Is the sight triangle available for minor-road drivers? (IN-08, IN-09)
17. Is control (priority/STOP/GIVE WAY/signal/roundabout) appropriate to volumes and speeds; are signs and lines present? (IN-15, TS)
18. Are channelising islands, turning lanes and corner radii appropriate (not encouraging high-speed turns)? (IN-02..07, IN-11)
19. Are pedestrian crossings and refuges provided on all legs with kerb ramps? (IN-13, PD)
20. Are median openings/U-turns safe, signed and lit? (MD-09, MD-10)
21. Are signals visible, correctly phased, with pedestrian phases and no obstruction of heads? (TS-01..16)
22. Roundabouts: deflection, entry width, splitter islands, signs, lighting? (RB)

**5.5 Signs**
23. Are all necessary regulatory, warning and information signs present and none superfluous/conflicting? (SG-01..04)
24. Are sign sizes and siting distances correct for speed? (SG-05..09)
25. Are mounting heights and lateral clearances correct; are signs obstructing footpaths? (SG-14..18)
26. Are signs retroreflective (correct sheeting class), clean, legible by day and night, not faded/damaged/vandalised? (SG-29..37)
27. Are advance direction, gantry and reassurance signs placed correctly? (SG-19, SG-20)

**5.6 Markings and delineation**
28. Are centre/lane/edge lines present, of correct width and pattern, and retroreflective? (MK-01..10, MK-31..33)
29. Are stop lines, give-way lines, zebra crossings, hatching, arrows and word markings present and correct? (MK-11..25)
30. Are road studs, delineators, chevrons and object markers provided on curves, medians, islands and hazards? (MK-27..29, SG-38..40)
31. Are old/conflicting markings removed?

**5.7 Lighting**
32. Is lighting provided where warranted (junctions, crossings, built-up areas, bus stops, humps, underpasses)? (LT-01..09, LT-17)
33. Is illumination level/uniformity adequate; are there dark spots / lamp outages? (LT-16)
34. Are lighting poles outside the clear zone or protected; not in the pedestrian zone? (LT-13, LT-14)

**5.8 Roadside hazards and barriers**
35. Are there unshielded hazards within the clear zone (trees, poles, culvert headwalls, boulders, drains, steep slopes, drops)? (RS-01..07, RS-21..23)
36. Are barriers warranted on embankments/bridges and provided? (RS-06, RS-17)
37. Are barriers of correct height, post spacing, length, continuous, with crash-worthy end terminals and transitions? (RS-08..16)
38. Are barriers damaged or deformed? (RS-19)
39. Are poles/sign posts frangible where unprotected? (SG-25, RS-22)

**5.9 Vulnerable road users (pedestrians, cyclists, NMT, two-wheelers)**
40. Are footpaths continuous, of adequate clear width and height, surfaced and free of obstructions/encroachments? (PD-01..11, PD-29, PD-30, BP-20)
41. Are kerb ramps and tactile paving provided at every crossing and footpath end? (KB-08, PD-13, PD-14)
42. Are safe crossing points provided at the desire lines and at adequate spacing; are they marked, signed, lit and (where needed) signalised or raised? (PD-17..28)
43. Are refuges provided on wide roads; are guardrails channelising pedestrians to crossings without trapping them? (PD-15, PD-25, PD-34)
44. Are "squeeze points" absent (footpath forced onto carriageway by poles, bus shelters, parked vehicles)? (PD-30, BP-06)
45. Are cycle tracks/NMT lanes continuous, protected and free of parked vehicles? (CW-16, PD-35)
46. Are schools, hospitals, markets and bus stops provided with required calming, signs and crossings? (SZ-01..07, TC-14, TC-15)
47. Are two-wheeler-specific hazards (slippery markings/covers, barrier posts, edge drops, potholes) controlled? (PV-14, RS-24)

**5.10 Public transport**
48. Are bus stops located and designed safely (bus bays/far-side, sight distance, not on curves), with shelters not obstructing footpaths or sight lines? (BP-01..09)
49. Are passenger crossings provided behind bus stops? (PD-21)

**5.11 Parking and access**
50. Is parking prohibited near junctions, crossings, bus stops and on footpaths; are prohibitions enforced/marked? (BP-16..19)
51. Do property accesses/driveways create conflicts; is access control on NH maintained (service roads)? (IN-17)
52. Are encroachments (hawkers, materials, structures) within ROW/sight lines removed? (BP-20, BP-21)

**5.12 Pavement surface**
53. Are potholes, rutting, ravelling, edge breaks, corrugations or bleeding present; severity? (PV-01..08, PV-14, PV-22..24)
54. Is skid resistance adequate (especially at junctions, curves, humps)? (PV-15)
55. Are utility covers/inlets flush? (PV-25, PV-26)
56. Is the roughness within acceptable band? (PV-09..11)

**5.13 Drainage**
57. Is surface drainage effective (no ponding, correct camber/shoulder slope)? (DR-01..09, DR-18)
58. Are drains covered/flush in urban areas and outside the clear zone or shielded in rural areas? (DR-13, DR-14, RS-23)
59. Are inlets/gullies adequate and maintained? (DR-10, DR-15, DR-19)

**5.14 Speed management & traffic calming**
60. Are posted speed limits appropriate and consistent; signed at required intervals? (SL, SZ-08, SG-22)
61. Are traffic calming devices (humps, tables, rumble strips) compliant with IRC:99 in geometry, location, marking and signing; are illegal/unmarked humps present? (TC-01..19)
62. Are gateway treatments provided at village/town entries on highways? (TC-18)

**5.15 Work zones and maintenance**
63. Are any ongoing works protected per IRC:SP:55 (advance warning, tapers, devices, pedestrian route, night lighting)? (WZ-01..25)
64. Is routine maintenance (vegetation, sign cleaning, lamp replacement, marking renewal) evident?

**5.16 Night-time audit**
65. Night drive-through: retroreflectivity of signs/markings/studs, lighting, visibility of hazards, kerbs, humps and pedestrians.

**5.17 Bridges, culverts, railway crossings**
66. Approach guardrails, parapet heights, width continuity, signs, lighting; level-crossing gates/signs/markings. (RS-17, SG)

---

## 17. Indian colour conventions (kerbs, hazards, medians, signs, markings, furniture)

| ID | Element | Colour convention | Source | Conf |
|---|---|---|---|---|
| CC-01 | Roadside kerbs | alternate black & white bands, 500 mm each (some agencies 300 mm); retroreflective paint | IRC:35-2015; UTTIPEC guideline | high |
| CC-02 | Central island / channelising island / median nose kerbs | alternate black & yellow vertical stripes 500 mm (or chequered black-white) | IRC:35-2015; UTTIPEC | high |
| CC-03 | Median kerbs (running length) | black & white alternating (black & yellow at openings/noses) | IRC:35 | medium |
| CC-04 | Objects within/adjacent to carriageway (piers, abutments, poles, tree trunks) | yellow & black diagonal stripes at 45° (pointing down toward traffic side), bands 100–300 mm, to 1.25 m height | IRC:35-2015 (object markings); IRC:79-2019 | high |
| CC-05 | Hazard markers (IRC:79) | black body with fluorescent yellow retroreflective (Type XI) stripes sloping down toward carriageway; chevron boards: yellow background, black arrows | IRC:79-2019 | high |
| CC-06 | Guide posts / delineators | white post with black band at top; red reflector on left (near) side, white (or yellow on median side) on right | IRC:79-2019 | medium |
| CC-07 | Road studs | white lane; yellow centre/median-side & no-overtaking; red left edge; green lay-bys/slip roads | IRC:35-2015 | medium |
| CC-08 | Longitudinal markings | white = permissive/guidance; yellow = restriction (no overtaking, no parking/stopping, bus/cycle lane boundary, median-side edge on some divided roads) | IRC:35-2015 | high |
| CC-09 | Yellow box junction | yellow cross-hatch | IRC:35 | high |
| CC-10 | Speed humps | white (retroreflective) chevrons/triangles or alternate black-white bands; hump sign black-on-white triangle with red border | IRC:99-2018; IRC:67 | medium |
| CC-11 | Mandatory signs | white disc, red border (≥ 10 % dia), black symbol; prohibition bar red; compulsory = blue disc, white symbol; STOP red octagon white legend | IRC:67-2022 | high |
| CC-12 | Cautionary signs | white triangle, red border, black symbol | IRC:67-2022 | high |
| CC-13 | Direction / informatory signs | green ground white legend (NH/EXP directions); blue ground (facilities, route information, SH/MDR in some editions); white ground black legend (local/urban street names); brown (tourist) | IRC:67-2022 | medium |
| CC-14 | Temporary / work-zone signs | yellow (or fluorescent orange) ground, black legend; barricades orange/white or red/white stripes | IRC:SP:55-2014 | medium |
| CC-15 | Crash barrier delineation | yellow (right/median side) & white/red (left) retroreflectors on W-beam; barrier terminals with black-yellow hazard markers | IRC:79; IRC:119 | medium |
| CC-16 | Traffic cones / drums | fluorescent orange-red with two white retroreflective bands | IRC:SP:55 | high |
| CC-17 | Bollards | contrasting (yellow/black or white) with retroreflective band ≥ 50 mm | IRC:103 | medium |
| CC-18 | Pedestrian guardrails | painted contrasting colour (white/yellow/silver) with reflectors at ends | IRC:103 | medium |
| CC-19 | Tactile tiles | contrasting colour to footpath (typically yellow) | Harmonised Guidelines MoHUA | high |
| CC-20 | Tree trunks on roadside | white (lime) band with red/black upper band to 1.25 m (customary PWD practice for night visibility) | PWD practice | low |
| CC-21 | Bus stop / no-parking kerb | yellow continuous kerb (no parking); bus box yellow | IRC:35; IRC:SP:12 | medium |
| CC-22 | Signal heads | red (top) – amber – green (bottom); pedestrian red/green man; backing board black with white/yellow border | IRC:93 | high |
| CC-23 | School zone | yellow-black "SCHOOL ZONE" boards; zebra with yellow border strips optional | IRC:SP:32 | low |

---

## 18. Quick-reference thresholds for the rule engine (hard-fail set, all **high** confidence)

| Check | Fail condition |
|---|---|
| Lane width | < 3.0 m (urban local) / < 3.5 m (arterial/NH) measured per lane |
| Footpath clear width | < 1.8 m anywhere (residential); < 2.5 m (commercial) |
| Footpath/kerb height | > 150 mm |
| Kerb ramp | missing at crossing, or slope > 1:12 |
| Zebra stripes | stripe ≠ 400–600 mm or faded (< 50 % visible) |
| Stop line | missing at signal/STOP, or width < 200 mm |
| Edge line | missing on NH/SH; width < 100 mm |
| Cautionary sign size | side < 600 mm (≤ 50 km/h) / < 900 mm (NH) |
| Sign mounting height (kerbed) | bottom edge < 2.0 m or > 2.5 m; obstructing footpath |
| Sign lateral clearance | < 0.3 m from kerb (urban) / < 2.0 m from carriageway edge (rural) |
| Speed hump | height > 100 mm; chord < 3.0 m; no warning sign; unmarked; on NH main carriageway |
| School zone | posted speed > 25 km/h or no School sign |
| Signal head | bottom < 2.5 m (post) / < 5.5 m (overhead); single face per approach |
| Median width | < 1.2 m urban |
| Clear zone hazard | rigid object ≤ 3 m from carriageway edge, unshielded, speed ≥ 60 km/h |
| W-beam | post spacing > 2 m; height outside 600–800 mm; missing terminal |
| Pothole | any pothole > 50 mm deep or > 450 mm wide on NH/arterial; > 1 % area |
| Rut | > 20 mm |
| Camber | < 1.7 % or > 4 % (bituminous) |
| Bus bay | < 18 m length; stop within junction |
| Parking | within 15 m of junction; on footpath/zebra |
| Work zone | no advance warning sign ≥ 50 m (urban) / ≥ 300 m (NH); no taper; cones > 20 m apart |
| Kerb/island painting | islands not black-yellow; kerbs unpainted at junctions |
| Lighting | none at junction/crossing in urban area |
| Drain | open/uncovered drain within footpath or ≤ 1 m of carriageway edge (urban) |

---

## Sources

Primary documents (canonical locations; not directly fetched from this sandbox — content taken from search excerpts):

- IRC:86-2018 Geometric Design Standards for Urban Roads and Streets — https://law.resource.org/pub/in/bis/irc/irc.gov.in.086.2018.pdf ; 1983 ed. https://law.resource.org/pub/in/bis/irc/irc.gov.in.086.1983.pdf ; reproduced in Delhi PWD Urban Roads Manual https://pwddelhi.s3.ap-south-1.amazonaws.com/documents/urban-roads-manual.pdf
- IRC:73-1980 Geometric Design Standards for Rural (Non-Urban) Highways — https://law.resource.org/pub/in/bis/irc/irc.gov.in.073.1990.pdf ; HTML https://law.resource.org/pub/in/bis/irc/translate/irc.gov.in.073.1990.html ; draft 2020 https://irc.nic.in/admnis/admin/showimg.aspx?ID=235
- IRC:SP:73-2018 Two-laning manual — https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.073.2018.pdf
- IRC:SP:84-2019 Four-laning manual — https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.084.2019.pdf
- IRC:SP:87-2019 Six-laning manual — https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.087.2019.pdf
- IRC:SP:99-2013 Expressways manual — https://www.scribd.com/document/317201214/IRC-SP-99-2013-manual-for-expressways-pdf
- MoRTH circular on shoulder widths for two-laning (2020) — https://morth.nic.in/sites/default/files/circulars_document/Width%20of%20shoulder%20(Paved%20and%20Earthen)%20for%20two%20laning%20of%20National%20Highways.pdf
- IRC:103-2012 Guidelines for Pedestrian Facilities — draft text https://www.nitiforstates.gov.in/public-assets/Policy/policy_files/GNANAO000329.pdf ; ITDP footpath handout https://www.itdp.in/wp-content/uploads/2014/04/11.-Footpath-Design_Handout.pdf ; ITDP Healthy Streets checklist https://itdp.in/wp-content/uploads/2024/08/Healthy-Streets-Design-Metres-pdf.pdf ; UTTIPEC kerb heights https://uttipec.org.in/PDF/Kerb%20Heights%20for%20Footpaths%20and%20Medians.pdf
- IRC:35-2015 Code of Practice for Road Markings — https://law.resource.org/pub/in/bis/irc/irc.gov.in.035.2015.pdf ; UTTIPEC road marking guideline https://uttipec.org.in/PDF/Guideline%20for%20road%20making.pdf ; MoRTH circular SR 24-10-2017 signs & markings https://morth.gov.in/sites/default/files/circulars_document/SR-2017.10.24-Provision%20of%20traffic%20signs%20(including%20Variable%20Message%20Signs)%20and%20Pavement%20marking%20on%20National%20Highways%20and%20other%20roads%20improved,%20developed%20under%20Centrally%20Sponsored%20Schemes.pdf
- IRC:67-2022 / 2012 Code of Practice for Road Signs — https://www.scribd.com/document/700190819/IRC-67-2022-traffic-sign ; 2012 https://www.sir.advancedleadership.harvard.edu/s/ircgovin0672012.pdf ; "What's new in IRC:67-2022" https://trafficinfratech.com/whats-new-in-irc-67-2022/ ; IRF India webinar (Table 15.1) https://indiairf.com/files/IRF%20IC%20Presentation%20-%20Webinar%202.pdf ; PMGSY RSA deck https://pmgsy.nic.in/sites/default/files/RSA%20(Session%202%20_%203).pdf
- IRC:99-2018 Traffic Calming — https://law.resource.org/pub/in/bis/irc/irc.gov.in.099.2018.pdf ; 1988 ed. https://law.resource.org/pub/in/bis/irc/irc.gov.in.099.1988.pdf ; MoHUA Code of Practice Part 5 Traffic Calming https://mohua.gov.in/upload/uploadfiles/files/Part_V_Traffic_Calming.pdf ; Bhutan guideline citing IRC:99 https://www.moit.gov.bt/wp-content/uploads/2022/09/GUIDELINES-ON-SPEED-BREAKER.pdf
- IRC:93-1985 Traffic Signals — https://ia801909.us.archive.org/4/items/govlawircy1985sp93_0/irc.gov.in.093.1985.en.html
- IRC:SP:23-1983 Vertical Curves — https://www.scribd.com/document/492329477/14-IRC-SP-23-1983 ; IRC:66-1976 sight distance https://law.resource.org/pub/in/bis/irc/translate/irc.gov.in.066.1976.html ; MoRTH compendium circular 302.11 (26-7-1984) https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/302.11%20-%2026.7.84.pdf
- IRC:SP:41-1994 At-grade intersections — https://archive.org/details/govlawircy1994sp41_0
- IRC:65-2017 Roundabouts — https://law.resource.org/pub/in/bis/irc/irc.gov.in.065.2017.pdf
- IS 1944 Parts 1 & 2 (1970) Lighting of Public Thoroughfares — https://law.resource.org/pub/in/bis/S05/is.1944.1-2.1970.pdf
- IRC:119-2015 Roadside Safety — http://law.resource.org.s3.amazonaws.com/pub/in/bis/irc/irc.gov.in.119.2015.pdf ; IIT-D TRIPP training (clear zone) https://tripc.iitd.ac.in/assets/training_material/R_Goel-Highway%20design%20standards.pdf ; https://tripc.iitd.ac.in/assets/training_material/V_Kovvali-RoadsideHazard.pdf
- IRC:82-2015 Maintenance of Bituminous Road Surfaces — https://law.resource.org/pub/in/bis/irc/irc.gov.in.082.2015.pdf ; IRC:82-2023 https://cdnc.heyzine.com/files/uploaded/af6fbe7a239154d9200b2ead03429af3946da477.pdf
- IRC:SP:16-2019 Surface Evenness — https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.016.2019.pdf ; PMGSY roughness lecture https://pmgsy.nic.in/sites/default/files/L06-PMGSY_SS_Roughness_04032022.pdf
- IRC:SP:42-2014 Road Drainage — https://ia802907.us.archive.org/6/items/govlawircy2014sp42/irc.gov.in.sp.042.2014.en.html ; IRC:SP:50-2013 Urban Drainage https://archive.org/details/govlawircy2013sp50
- IRC:80-2020 Bus stops (notification) — https://www.irc.nic.in/admnis/admin/showimg.aspx?ID=325
- IRC:SP:12-2015 Parking — https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.012.2015.pdf
- IRC:SP:55-2014 Work Zones — https://archive.org/details/govlawircy2014sp55_0 ; draft 2nd revision https://cdnc.heyzine.com/files/uploaded/v2/d285f90fd38f23c00cb324ed2b7172f8b8ac3bf2.pdf ; IRF India deck https://indiairf.com/wp-content/uploads/2021/04/01-S.K.pdf
- MoRTH speed limit notification S.O. 1522(E) 6-Apr-2018 — PIB https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1539335&reg=48&lang=2 ; https://taxguru.in/corporate-law/govt-notifies-speed-limit-roads-vehicles-india.html
- School zones — IRC:SP:32-2023 cited in CEE audits https://www.ceeindia.org/pdf_files/Road-Safety-for-Children.pdf ; Punjab 25 km/h notification https://www.roadsafetyngos.org/events/25-km-h-in-punjab-india/
- IRC:SP:88-2019 Manual on Road Safety Audit — https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.088.2019.pdf ; 2010 ed. https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.088.2010.pdf ; Samruddhi Expressway RSA (reproduces Stage-5 checklist) https://www.roadsafetynetwork.in//wp-content/uploads/2023/10/Samruddhi-Expressway-Safety-Audit-VNIT-2023-1.pdf ; BRO RSA training https://tripc.iitd.ac.in/assets/training_material/V_Kovvali-SafetyAuditApproach.pdf
- iRAP Coding Manual (drive-on-left) — https://irap.org/specifications/ ; v3.2 copy https://www.southnorfolkandbroadland.gov.uk/asset-library/imported-assets/cd8.28-irap-coding-manual-drive-on-left-3-2.pdf ; Star Rating & Investment Plan Manual https://austroads.gov.au/__data/assets/pdf_file/0033/836295/iRAP_Star_Rating_and_Investment_Plan_Manual_English.pdf ; IndiaRAP https://indiarap.org/
- IRC:79-2019 Delineators / hazard markers — https://law.resource.org/pub/in/bis/irc/irc.gov.in.079.2019.pdf
- NHAI MCA maintenance schedule — https://nhai.gov.in/nhai/Doc/19nov14/Annexure%20-%20Schedule%20-L-O.pdf
- IRC publications catalogue — https://www.irc.nic.in/WriteReadData/LINKS/Updated%20Catalogue,%202026(1)ed1ad28e-67a2-4bfe-82c1-4c3b75fa9107.pdf ; law.resource.org IRC directory https://law.resource.org/pub/in/bis/irc/
