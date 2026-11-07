# How Professional Road Safety Audits Are Done in India, Who Consumes Them, and What Our Report Must Contain

Research memo for **CFI Road Auditor** (automated RSA from phone video/photos).
Compiled 7 November 2026 from web research. Where a primary document could not be opened in this session (several government and standards hosts were unreachable from the research sandbox), the text says so and marks the item as *reconstructed* or *unverified*. Items marked **[verify]** should be checked against the primary PDF before being hard-coded into product logic.

---

## Table of contents

1. [How a professional RSA is done in India](#1-how-a-professional-road-safety-audit-is-done-in-india)
   - 1.1 Governing documents
   - 1.2 Audit stages
   - 1.3 Team composition and auditor qualifications
   - 1.4 Data auditors collect
   - 1.5 Equipment
   - 1.6 The process, step by step
   - 1.7 Structure of a real Indian RSA report (and worked examples)
2. [Risk rating methods (exact matrices)](#2-risk-rating-methods)
3. [Existing-road / in-service checklists](#3-checklists-existing-road--in-service-audit)
4. [User personas and what each needs](#4-user-personas)
5. [Existing products and competitors](#5-existing-products--competitors)
6. [Legal and regulatory hooks](#6-legal--regulatory)
7. [Proposed CFI report specification](#7-proposed-cfi-report-specification)
8. [Sources](#8-sources)

---

## 1. How a professional Road Safety Audit is done in India

### 1.1 Governing documents

| Document | Status / what it does |
|---|---|
| **IRC:SP:88-2019 "Manual on Road Safety Audit" (First Revision)** | The national standard. Published September 2019, replacing IRC:SP:88-2010. Revised to cover *all* categories of roads (urban and rural, expressways, NH/SH/MDR, PMGSY rural roads) and align with international practice. Defines stages, team composition, process, risk-rating (Tables 4.2/4.3), reporting format, the road authority's response procedure and stage-wise checklists. |
| **MoRTH circulars (Comprehensive Compendium, Section 604 "Road Safety")** | 19.10.2015 Road Safety Engineering Measures; 28.10.2015 OM *Protocol for identification and rectification of black spots on NHs*; 20.04.2017 *Essential approach and principles for Road Safety Engineering works*; 04.07.2018 *RSA at engineering-design (DPR) stage of new road projects*; 20.09.2019 *Road Safety Measures on stretches of NHs* (RSA recommended on all NHs with follow-up action); 26.08.2019 *Rectification of Accident Black Spot – preparation of proposal and sanction*; **09.11.2020 *All-stage Road Safety Audit through Independent Road Safety Experts*** (audits at all stages must be done by independent experts engaged through the IE/AE or directly by MoRTH/NHAI/PWD, to remove the conflict of interest created when concessionaires audited their own designs); 01.07.2021 letter RW/NH-29020/03/2020-S&R(P&B)-RSCE on third-party RSA procedures; 21.11.2025 letter making the IAHE (or designated institute) RSA certification course mandatory for all personnel carrying out RSA of highways. |
| **NHAI** | 2016 circular NHAI/RSC/012/Empanelment/4231 (08.12.2016) on empanelment/skilling of road safety auditors; NHAI Road Safety Cell; ToR for empanelled *Road Safety Experts*; Jan 2023 decision making third-party RSA at DPR stage mandatory for all projects; FY2021-22 NHAI audited ~16,500 km of NH through specialised safety auditors. |
| **Model Concession Agreement (BOT/HAM/TOT) – Schedule L "Safety Requirements"** | Concessionaire must run a surveillance and safety programme; NHAI appoints a *Safety Consultant* to audit against Schedule L; Independent Engineer (IE) / Authority Engineer (AE) supervises. |
| **Motor Vehicles (Amendment) Act 2019** | S.198A liability for failing road design/construction/maintenance standards; S.210D central power to notify design/construction/maintenance standards; S.215 State Road Safety Councils and District Road Safety Committees; S.164B Motor Vehicle Accident Fund; S.135 crash-investigation schemes. |
| **Supreme Court** | *S. Rajaseekaran v. Union of India* W.P.(C) 295/2012 – Supreme Court Committee on Road Safety (SCCoRS) constituted 22.04.2014 (Justice K.S. Radhakrishnan; now Justice A.M. Sapre); 30.11.2017 directions (state road safety policy, council, lead agency, fund, DRSCs, action plans, RSAs, engineering, trauma care); *In Re: Phalodi Accident* suo motu order 13.04.2026 (commuter safety is part of Article 21; nationwide interim directions). |
| **International references used by Indian auditors** | Austroads *Guide to Road Safety Part 6 – Road Safety Audit* (2009, 2019, 2022 editions – the source of the risk matrix IRC adopted); UK DMRB **GG 119** (replaced HD 19/15 in 2018; v2.0.1 April 2025); PIARC *Road Safety Inspection Guidelines for Safety Checks of Existing Roads* (2012R27EN), PIARC *Road Safety Audit Guide* (2023), PIARC *Catalogue of Design Safety Problems and Potential Countermeasures* (2009R07EN); ADB **CAREC Road Safety Engineering Manual 1: Road Safety Audit** (2018) and Manual 5 *Star Ratings for RSA*; FHWA *Road Safety Audit Guidelines* FHWA-SA-06-06 (Prompt List 6 = Existing Road Audit); iRAP Star Rating methodology (fact sheets 1–8, Star Rating & Investment Plan Manual); World Bank *Delivering Road Safety in India* (2020); ITF Safe System case study on Karnataka KSHIP (3-star-for-all-users target). |

### 1.2 Audit stages

**IRC:SP:88-2019 (five stages)** – wording reconstructed from training material (BRO/TRIPP-IIT Delhi, PMGSY sessions) that quotes the manual **[verify exact clause numbers]**:

| Stage | When | What is examined |
|---|---|---|
| **Stage 1 – Feasibility / Preliminary design** | DPR concept, alignment options | Route choice, access control, junction type/spacing, provision for VRUs, land-use conflicts, design speed vs function |
| **Stage 2 – Detailed design** | Before tender drawings are frozen | Geometry (horizontal/vertical, sight distance), cross-section, junction layouts, signs/markings plan, lighting, barriers, drainage, pedestrian/cyclist/bus facilities, work-zone traffic management plan |
| **Stage 3 – Construction** | During works | Temporary traffic management, diversions, work-zone signs, exposure of workers and road users, whether built as designed |
| **Stage 4 – Pre-opening** | After completion, before traffic | Day **and night** drive-through; all signs/markings/lighting/barriers in place; conflicts not visible on drawings |
| **Stage 5 – Existing roads (operational / in-service)** | Any time on open roads; black-spot investigation; O&M period of concessions | Whether the road's safety features are compatible with its functional class and actual use; deficiencies that have developed (encroachment, faded markings, damaged barriers, unauthorised median openings, new accesses, parking, hawkers) |

The 2010 edition had six stages (Stage 1 feasibility, 2 preliminary design, 3 detailed design, 4 construction, 5 pre-opening, **6 existing roads / O&M of concession projects**); 2019 merged the first two. MoRTH's 2020 circular requires audits at *all* stages ("design, construction, operation and maintenance") by independent experts; PIB describes RSA of all NHs as mandatory through third-party auditors at all stages.

**Other frameworks for comparison**

- **UK GG 119**: Stage 1 (completion of preliminary design), Stage 2 (completion of detailed design), Stage 3 (completion of construction – day *and* night site visits), **Stage 4 (post-opening collision monitoring at 12 months and 36 months)**, plus *interim* audits. GG 119 covers new schemes; in-service roads are handled by separate "road safety inspection"/collision investigation processes.
- **Austroads Part 6 (2022)**: feasibility, concept/preliminary design, detailed design, pre-opening, **existing roads (road safety audit of existing roads)**, plus roadwork traffic-management audits and thematic audits (e.g. motorcycle, pedestrian, land-use development).
- **PIARC** distinguishes **Road Safety Audit (RSA)** – new projects – from **Road Safety Inspection (RSI)** – periodic, systematic on-site review of existing roads *not requiring crash data*. India's "Stage 5" is functionally an RSI plus crash analysis.
- **iRAP** is not an audit but a *star rating* of existing roads coded in 100 m segments; it is increasingly combined with RSA (ADB CAREC Manual 5).

### 1.3 Team composition and auditor qualifications

**IRC:SP:88-2019 clause 3.3 (reconstructed from secondary sources) [verify]**

- Minimum team of **two**; led by a **Senior Road Safety Auditor** who is **empanelled as such by the competent authority** (NHAI/MoRTH/State PWD/ULB), plus at least one qualified engineer. Larger teams add specialists as the stage demands (traffic engineer, pavement engineer, lighting, human factors, police/enforcement officer, NMT/urban designer for urban roads).
- Independence: auditors must be independent of the design/construction/O&M team being audited (the entire point of the 2020 MoRTH circular).
- Senior RSA (as summarised in the PMGSY training deck): civil engineering graduate, **>10 years** in design/construction/maintenance of roads, a formal RSA training programme of **at least two weeks**, **≥2 years** of practical road-safety engineering experience, and **≥3 completed RSAs**. Road Safety Auditor (team member): engineering graduate with RSA training and some RSA experience.

**NHAI Road Safety Expert (empanelment ToR)** – 20 years in highway/expressway design, DPR or RSA; worked as Team Leader/Road Safety Expert on ≥3 highway projects and submitted RSA reports covering ≥100 km of 4-lane-or-wider highways; age ≤65. NHAI may remove an expert from the panel without stating reasons.

**Certification pipeline**

- 15-day **Road Safety Auditor Certification Course** run by CSIR-CRRI, IAHE (Noida), IIT Roorkee, IIT Guwahati, IIT Madras and others under MoRTH's programme (pass mark 75 % in IAHE course). CRRI alone reports a pool of **991 certified auditors** created in 2024–25 sessions who went on to win >20,000 km of RSA work from NHAI/MoRTH/PWDs.
- **MoRTH letter 21.11.2025**: personnel involved in RSA of highways *must* have completed the IAHE (or designated) certification course; also a mandatory-training requirement for DPR-consultant personnel.
- **October 2025**: a *Road Safety Audit Certification Programme* ("Certification of Competence", internationally benchmarked, run by IRF India Chapter with NHAI in Delhi and MSRDC in Mumbai) – ~40 engineers in the inaugural cohort. IRF (Dec 2025) proposed that MoRTH empanel IRF-IC to run it nationally and link it to IRF's International Registry of road safety auditors. (Proposal, not yet a confirmed MoRTH decision.)

**UK GG 119 for comparison** (useful because Indian consultants working for multilaterals often cite it): team = Team Leader + ≥1 Team Member; Observers are not team members. Team Leader: ≥4 years relevant RSA/collision-investigation experience, ≥5 RSAs in the last 12 months, ≥2 days CPD/yr; Team Member: ≥5 RSAs in last 24 months; at least one holder of a **Certificate of Competency** (Appendix G) for motorway/trunk-road work. Auditors must be independent of the design organisation; the Overseeing Organisation approves the team.

### 1.4 Data auditors collect

For an **existing-road (Stage 5) audit** the manual and practice expect:

| Category | Specifics |
|---|---|
| **Desk data (pre-visit brief)** | Road classification & function (NH/SH/MDR/urban arterial), design standards applicable (IRC:SP:84/87/73, IRC:86 for urban), as-built/strip plan drawings, chainage reference, land use, previous audits/inspections, maintenance records, complaints |
| **Crash data** | Police FIR data for ≥3 calendar years (now from **iRAD/eDAR**), by chainage, severity (fatal/grievous/minor/non-injury), collision type, road user, time of day, light & weather; black-spot register (MoRTH MIS); hospital/108 ambulance data where available |
| **Traffic** | Classified volume counts (ADT, peak hour, % two-wheelers, % heavy vehicles, NMT, animal-drawn), turning-movement counts at junctions |
| **Speed** | Spot speeds (85th percentile, mean, speed differential between vehicle classes) at tangents, curves, approaches to built-up areas, school zones; posted vs operating speed |
| **Pedestrian / VRU** | Pedestrian crossing counts and desire lines, bus-stop boarding/alighting, cyclist counts, school peak flows, hawker/market activity, informal crossing points at medians |
| **Road inventory** | Lane/shoulder/median widths, cross-fall, curve radius/superelevation (estimated), sight distance, signs (type, size, sheeting, condition, retroreflectivity), markings (presence, condition, retroreflectivity), lighting (presence, working lamps, lux), barriers (type, terminal, height, damage), culverts/bridges (parapets, width transitions), drainage, pavement condition (potholes, rutting, edge drop, skid), roadside hazards (trees, poles, open drains, unprotected culvert headwalls), accesses, median openings |
| **Site observations** | **Daytime drive-through** both directions at operating speed (video), **night drive-through** (sign/marking visibility, lighting, glare, unlit obstructions), **walk-through** of junctions, built-up stretches, bus stops and black spots; peak-hour observation of conflicts; wet-weather observation where possible |
| **Environment** | Weather patterns (fog belts, flooding), animal crossings, encroachments, construction activity |

### 1.5 Equipment

Typical kit carried by an Indian RSA team (compiled from IRC/Austroads/CAREC practice and NHAI tender ToRs):

- **Distance/location**: measuring wheel, **Distance Measuring Instrument (DMI)** on the survey vehicle, handheld **GNSS/GPS** (or phone GPS logging at 1 Hz), laser distance meter, 30/50 m tape, chainage from km stones/reference pillars.
- **Imaging**: forward-facing **dash camera** (time/GPS-stamped), handheld DSLR/phone camera, **360° camera** on roof mount (increasingly), drone for junction aerials (where permitted), night photography capability.
- **Measurement**: **retroreflectometer for signs** (coefficient of retroreflection RA, cd/lx/m²) and **for markings** (RL, mcd/m²/lx), **lux meter** for lighting, **radar/LIDAR speed gun** for spot speeds, inclinometer/crossfall gauge, 3 m straight edge and wedge for rutting, pothole depth gauge, **British Pendulum Tester** or grip tester for skid resistance (spot checks), ball-bank indicator for curve advisory speed, sound-level meter (rarely).
- **Traffic**: tube/radar counters or video-based counters, manual count boards, stopwatch for pedestrian crossing times/signal phasing.
- **Safety & admin**: high-visibility PPE, cones, warning triangle, torches, printed checklists/tablet app, clipboards, strip map, mobile data for iRAD lookups.

What the phone-video-based product can and cannot replace: GPS-stamped video replaces the DMI/dashcam/camera/strip-map set; it **cannot** directly measure retroreflectivity, lux, skid resistance or speed with instrument accuracy — these should be flagged as "field verification required" with the instrument named.

### 1.6 The process, step by step

Consolidated from IRC:SP:88 (2010/2019), GG 119, Austroads and CAREC:

1. **Commissioning** – Client (NHAI PIU / PWD EE / ULB / concessionaire via IE) issues ToR; defines stage, length (chainage from–to), standard to audit against, deliverables; appoints independent team; conflict-of-interest declaration.
2. **Briefing / commencement meeting** – Client + designer/O&M team + auditors. Hand over drawings, crash data, traffic data, previous audit reports, project background. Agree programme, site-visit dates (day + night), access/safety arrangements.
3. **Desk study** – Review drawings and data; crash cluster analysis (MoRTH 500 m sliding window); identify locations needing attention; prepare checklists and strip map.
4. **Site inspection** – Drive-through both directions in daylight, drive-through at night, walk-throughs at junctions/built-up areas/black spots; photograph every concern with chainage + GPS; measurements as needed; observe peak-hour and off-peak behaviour (wrong-side driving, informal crossings, parking).
5. **Analysis** – For each concern: describe the problem, the crash type it could cause, who is at risk, assign **likelihood × severity → risk rating → priority**; draft recommendation(s) with reference to the governing IRC code; cost class and timeframe (immediate/short/medium/long).
6. **Audit report** – Formal signed report (see 1.7). In IRC practice a *draft* report is discussed at a **completion/exit meeting** before being finalised.
7. **Response report / exception report** – Road authority & designer respond to **each** finding: *accept / accept with modification / reject with reasons*. GG 119 formalises this as the **RSA Response Report**; disagreements go to an **Exception Report** and the Overseeing Organisation's decision is recorded in a **decision log**. IRC:SP:88 prescribes an equivalent road-authority response procedure (NHAI reports carry a "Client response" column).
8. **Implementation & close-out** – Action plan with owner and date; compliance tracking (in NHAI, by the PIU/IE; for black spots, by the MoRTH Black Spot MIS); follow-up audit/re-inspection; for GG 119 Stage 4 collision monitoring at 12 and 36 months.

### 1.7 Structure of a real Indian RSA report

**What IRC:SP:88-2019 prescribes** (reporting format chapter; reconstructed):

1. Title page (project, stretch & chainage, stage, client, auditor organisation, date, report version).
2. Project description and background (road class, length, cross-section, traffic, land use).
3. Audit team names, qualifications and empanelment numbers; statement of independence.
4. Documents and data reviewed.
5. Dates of inspections, **weather and light conditions** for each visit; who attended.
6. Methodology (checklists used, risk-rating method – Section 4.6, Tables 4.2 & 4.3).
7. **Findings table**: every safety concern from desk and site audit, with location (chainage/GPS), description, photograph reference, **risk rating**, recommendation and **priority** (Essential / Highly Desirable / Desirable).
8. Summary of priorities and an implementation/action plan.
9. Photographs (geo-tagged, numbered, cross-referenced).
10. Appendices: checklists completed, crash data analysis, location plans/strip maps, signed audit statement.

**Example: NHAI existing-road RSA, NH-220 Karanjia–Patna–Dhenkikote (Odisha), "RSA-2"** (structure as described in the public copy):

- Executive summary → Introduction (project, scope, stage) → Audit team → Methodology (IRC:SP:88; day/night inspection; risk assessment) → Road description (chainage-wise strip description) → **Risk Assessment Criteria table** (likelihood × severity) → **Priority Level table** → Findings organised **by hazard type**: deficiencies at **curves**, **water bodies alongside the road**, **high embankments** (unprotected), **built-up areas**, **junctions**, **bridges/culverts** → each finding: chainage, photograph, observation, risk, recommendation, priority → consolidated recommendations with cost/timeframe → Annexures (photo log, checklists).

**Example: NH-44 (Jammu & Kashmir) design-stage RSA table** – columns: *S. No. | Safety concern | Chainage | Finding/observation | Recommendation | Risk type | Priority (auditor) | Client response.*

**Example: SaveLIFE Foundation Zero Fatality Corridor (Mumbai–Pune Expressway, 94.5 km)** – 2012–14 forensic crash analysis → 2015 on-site RSA that logged **~2,145 engineering issues in 15 sub-categories** (e.g. barrier gaps/ends, missing/incorrect signage, markings, crash cushions, median openings, shoulder drop-offs, lighting, drainage, animal/pedestrian ingress, emergency bays) → monthly re-audits → 4E action plan with MSRDC, Highway Police and IRB; reported **58.3 % reduction in deaths 2016→2023 (151→63)**. The ZFC report format is issue-level (location, photo, category, status open/closed) — effectively a **tracked defect register**, which is what O&M clients value.

**Example: VNIT Nagpur safety audit of Samruddhi Mahamarg (2023)** – structured explicitly around the *"Checklist for Safety Audit of Existing Roads as per IRC:SP:88-2019"* (delineation, VRU provisions, signage, barrier terminals, rest areas, speed management, tyre-burst/"highway hypnosis" factors); later MSRDC/SaveLIFE work reported 29 % drop in deaths in one year.

**Example: Bengaluru Traffic Police Road Safety Report 2023 (with Vital Strategies / BIGRS)** – 43 black spots and 24 high-risk corridors; black-spot definition identical to MoRTH's; 2023–25 list of 64 black spots published 2026 with location, number of crashes/deaths, and a proposed engineering fix per spot. BBMP's *Suraksha 75* junction programme (WRI India knowledge partner, ~₹100 crore) consumes junction-level audits.

**Common features across all real Indian reports** (and therefore minimum requirements for ours):

- Every finding anchored to **chainage (km + m) and direction (LHS/RHS, increasing/decreasing chainage)**, and increasingly also to **GPS lat/long**.
- A **photograph per finding**, numbered and taken in the direction of travel.
- A **risk rating and a priority label** per finding, derived from a stated matrix.
- Recommendations that **cite the IRC code** that is breached (IRC:67 signs, IRC:35 markings, IRC:119 barriers, IRC:99 traffic calming, IRC:103 pedestrian facilities, IRC:SP:55 work zones, IRC:SP:84/87/73 geometric standards, IRC:SP:90 grade separators, IRC:SP:41/IRC:65 junctions, IRC:SP:50 drainage, IRC:SP:12 parking, IRC:86 urban cross-sections, IS 1944 lighting).
- A **summary table by priority** and a chainage-ordered **strip map**.
- A **response column** for the road authority.

---

## 2. Risk rating methods

### 2.1 IRC:SP:88-2019 (Section 4.6, Tables 4.2 & 4.3)

Risk is defined as **likelihood (frequency) × consequence (severity)**. Table 4.2 gives qualitative criteria for both; the matrix output is **Very High / High / Medium / Low**. Table 4.3 maps risk to the priority wording that goes in the report:

| Risk (Table 4.2 output) | Priority label (Table 4.3) | Meaning |
|---|---|---|
| **Very High** | **Essential** | Must be rectified regardless of cost; immediate action |
| **High** | **Highly Desirable** | Should be rectified even at high cost, *unless remedial cost is prohibitive and the risk can be reduced by other means* |
| **Medium** | **Desirable** | Rectify where cost is moderate / within programme |
| **Low** | (Desirable / "may be considered") **[verify wording]** | Rectify if cost is low, or at next maintenance |

The severity column of Table 4.2 is known to use the Austroads-style descriptions (the "Very High" example in the published fragment is *"high-speed, multi-vehicle crashes on expressways"*), so IRC's criteria are, in substance, the **Austroads 2009 matrix** below with the labels renamed Intolerable→Very High. **[verify the exact row/column labels against the IRC PDF before encoding.]**

### 2.2 Austroads Guide to Road Safety Part 6 (2009) – the matrix most Indian reports actually print

**Frequency (likelihood) of a crash resulting from the deficiency**

| Label | Definition (Austroads 2009) | CAREC 2018 variant |
|---|---|---|
| Frequent | Once or more per **week** | once or more per **month** |
| Probable | Once or more per **year** (but less than weekly) | once or more per year (less than monthly) |
| Occasional | Once every **five to ten years** | same |
| Improbable | Less often than once every **ten years** | same |

**Severity of the likely crash**

| Label | Definition |
|---|---|
| Catastrophic | Likely multiple deaths (e.g. high-speed multi-vehicle crash on a freeway; bus/truck run-off into deep water) |
| Serious | Likely death or serious (hospitalising) injury (e.g. high-speed head-on, pedestrian struck at speed, run-off into tree/pole) |
| Minor | Likely minor injury (e.g. low-speed rear-end, cyclist fall) |
| Limited | Trivial injury or property damage only |

**Resulting risk matrix**

| Frequency ↓ / Severity → | Catastrophic | Serious | Minor | Limited |
|---|---|---|---|---|
| **Frequent** | Intolerable | Intolerable | High | Medium |
| **Probable** | Intolerable | High | Medium | Low |
| **Occasional** | High | Medium | Low | Low |
| **Improbable** | Medium | Low | Low | Low |

**Treatment approach by risk level**

| Risk | Suggested treatment |
|---|---|
| Intolerable | Must be corrected **at any cost** |
| High | Should be corrected (or risk significantly reduced) **even if cost is high** |
| Medium | Should be corrected (or risk significantly reduced) **if treatment cost is moderate** |
| Low | Should be corrected or risk reduced **if treatment cost is low** |

### 2.3 Austroads Part 6 (2019 / 2022 editions)

The 2022 edition (AGRS06-22) replaced the 4×4 grid with a **5-level** scheme and a **Safe System "energy tolerance" severity guidance sheet** (Figure 10.3): likelihood on a five-point scale (Rare → Unlikely → Possible → Likely → Almost certain) against severity assessed from impact speed/energy and road-user vulnerability, giving risk **Negligible / Low / Medium / High / Extreme**. Mitigation priority: Negligible = no action; Low = address in routine maintenance; Medium = address in programme; High = address as a priority; **Extreme = correct regardless of cost / do not open**. (Exact cell contents **[verify]** in AGRS06-22.)

### 2.4 UK DMRB HD 19/15 → GG 119

GG 119 deliberately does **not** rank or score problems. Each problem is reported as a numbered **Problem** (location, summary, description of the crash type/road users at risk, photograph) followed by one or more **Recommendations**, with an A1/A3 **problem location plan**. Prioritisation happens in the **RSA Response Report** (designer/Overseeing Organisation accept, reject or modify each recommendation with reasons) and any disagreement is settled in an **Exception Report** recorded in the scheme's decision log. Irish TII (GE-STY-01024/01025) follows the same no-ranking approach. Some UK local authority reports nevertheless add an Austroads-type 3×3 (Frequent/Probable/Occasional × Serious/Minor/Limited → High/Medium/Low).

### 2.5 iRAP Star Rating (proactive risk score, not an audit)

- Road coded in **100 m segments** on ~50 attributes (sources quote 52–78 depending on model version): speed (operating & posted), curvature, grade, sight distance, lane/shoulder width, delineation, roadside severity & distance (both sides), median type, intersection type/quality/volume, property access, pedestrian/bicycle facilities & crossing provisions, pedestrian/bicycle/motorcycle flows, street lighting, skid resistance, school zone warning, speed management, service-road, sidewalk, etc.
- **Star Rating Score (SRS)** computed separately for **vehicle occupants, motorcyclists, pedestrians, bicyclists** as the sum over crash types of (likelihood × severity × operating speed × external flow × median traversability) factors.
- **Bands (vehicle occupants & motorcyclists, model ≤3.x):** 5★ 0 to <2.5 · 4★ 2.5 to <5 · 3★ 5 to <12.5 · 2★ 12.5 to <22.5 · 1★ ≥22.5.
- Pedestrians and bicyclists use **wider bands** because their equations differ (fact sheet 7; commonly cited values: pedestrians 5★ <5, 4★ 5–<15, 3★ 15–<40, 2★ 40–<90, 1★ ≥90; bicyclists 5★ <5, 4★ 5–<10, 3★ 10–<30, 2★ 30–<60, 1★ ≥60 **[unverified in this session]**).
- **Model 3.10 (released May 2026)** harmonised the pedestrian/bicyclist banding and added a **"Zero Star" band** for extremely high-risk sections.
- Smoothed star ratings are averaged over longer lengths for mapping. Outputs via **ViDA**: star-rating maps, **Safer Roads Investment Plans (SRIP)** with ~90 countermeasures, estimated fatalities and serious injuries (FSI) saved, BCR. UN Global Target 3/4: all new roads ≥3★ for all users; >75 % of travel on ≥3★ roads by 2030. **IndiaRAP** (hosted by AITD) works with NHAI's Road Safety Cell and PIUs (e.g. 2,400 km programme: 791 km UP, 188 km TN, 309 km Maharashtra); KSHIP-II (World Bank) set a 3-star-for-all-users target for Karnataka state highways.

### 2.6 PIARC / EU and other schemes

- PIARC RSM prioritises interventions by a **hierarchy of control** and economic appraisal (BCR / cost-effectiveness) rather than a fixed matrix; the 2012 RSI guideline recommends classifying each deficiency by *severity of potential consequence* and *urgency*.
- EU Directive 2019/1936 **network-wide road safety assessment** ranks sections into risk classes (Austria uses 6 priority classes) to target RSIs.
- **MoRTH Highway Rating (2021 SOP)**: scores NH sections on Efficiency 45 / **Safety 35** / User services 20 (undivided 2-lane SOP; divided carriageways have a separate SOP); Oct 2026 notification created separate criteria for expressways/high-speed corridors vs normal NHs. This is a *performance score*, not a hazard rating, but it is what NHAI PDs are graded on.
- **MoRTH black-spot ranking**: severity-weighted counts within a 500 m window over 3 years; MoRTH's sliding-window method and NHAI's "accident-prone stretch" lists use fatalities first, then grievous injuries.

### 2.7 Recommendation for CFI (used in §7)

Adopt IRC:SP:88-2019 labels (Very High / High / Medium / Low → Essential / Highly Desirable / Desirable / Optional) computed from the Austroads 4×4 likelihood × severity matrix, show the **matrix cell** for each finding so an auditor can override it, and *additionally* emit an **indicative iRAP-style star band per 100 m per road-user group** so the output speaks both languages (IRC for Indian authorities, iRAP for NHAI/World Bank/ADB programmes).

---

## 3. Checklists: existing-road / in-service audit

Synthesised from IRC:SP:88 checklists (2010: Checklists 1–18 — planning, alignment, cross-section, junctions, signs, markings, lighting, roadside hazards, VRUs, developmental proposals, maintenance work, etc.; 2019: stage-wise checklists for rural, urban and expressway contexts, including "Checklist for Safety Audit of Existing Roads"), **Austroads Part 6 Checklist 6 "Existing roads"** (road alignment & cross-section; intersections; signs & lighting; markings & delineation; pedestrians & cyclists; bridges & culverts; pavement; parking; heavy vehicles; floodways & causeways; miscellaneous), **FHWA Prompt List 6 "Existing road audit"**, **PIARC RSI checklists** (motorways, inter-urban, urban main roads) and India-specific items observed in NHAI/SaveLIFE/BTP work. Each item is phrased as the question an auditor asks; the bracketed code is the reference used in recommendations.

**A. Road function, alignment & cross-section** (IRC:SP:84/87/73, IRC:86, IRC:38/73 geometry)
- Is the road's design speed/operating speed consistent with its function and the adjacent land use? Has land use changed since design (ribbon development)?
- Are horizontal curves consistent with approach speeds? Any isolated sharp curve after a long tangent? Is superelevation adequate and not reversed? Are curve warning/chevron/advisory-speed signs present?
- Are sight distances (stopping, overtaking, intersection) adequate? Obstructed by vegetation, hoardings, parked vehicles, structures, crest curves?
- Is the vertical alignment free of hidden dips, crest curves that hide junctions/crossings?
- Are lane widths, shoulder widths and median widths adequate for the traffic mix (two-wheelers, trucks, slow vehicles)? Is there a paved shoulder; is the edge drop-off >50 mm?
- Are cross-section transitions (4-lane→2-lane, bridge narrowing, bypass ends) safely tapered and signed?
- Is the camber/cross-fall adequate; any ponding?
- Are overtaking opportunities adequate; are no-overtaking zones marked (IRC:35)?
- Is there a service road where accesses are dense; is it continuous and separated?
- Are climbing lanes/truck lay-bys needed on grades?

**B. Intersections** (IRC:SP:41, IRC:65, IRC:SP:90, IRC:93 signals)
- Is each junction's type (uncontrolled, priority, roundabout, signalised, grade-separated) appropriate for volumes and speeds?
- Is the junction conspicuous from all approaches (advance warning, lighting, markings)? Any junction hidden on a curve/crest?
- Are sight triangles clear? Are approach speeds controlled (rumble strips, speed humps on minor road, transverse bar markings)?
- Are turning radii, channelisation islands, and refuge islands present and not over-run? Is there a right-turn storage lane; is the median opening long enough?
- Are stop/give-way lines, lane arrows, box markings, zebra crossings present and visible?
- Signals: are phases adequate for pedestrians; are signal heads visible; countdown timers; are they operational at night; is there a flashing amber at night?
- Roundabouts: deflection on entry, splitter islands, signage, central island visibility.
- Skewed junctions, Y-junctions, staggered T junctions, multi-leg junctions, junctions within 100 m of each other?
- Are medians at junctions opened for U-turns creating conflict with through traffic?
- Are accident-prone junction features present: **unsignalised median openings on 4/6-lane NH**, cross-traffic from village roads, bus stops at the junction mouth, hawkers in the junction?

**C. Pedestrians** (IRC:103-2022, IRC:11)
- Are footpaths present on both sides where there is pedestrian demand (built-up areas, schools, markets, bus stops)? Continuous, ≥1.8 m clear, unobstructed, level, with kerb ramps and tactile paving?
- Are crossings provided at desire lines (every ~250 m in urban areas; at every bus stop, school, market)? Type appropriate to speed and volume (zebra with refuge, signalised, raised table, FOB/subway)?
- Are FOBs/subways actually used (location, lighting, cleanliness, escalators)? Is there a median fence forcing use?
- Are medians opened informally by pedestrians (broken railings)? Are refuge islands wide enough (≥1.5–2 m)?
- Is pedestrian crossing time adequate at signals; are pedestrian signal heads present?
- Night-time: are crossings lit; are pedestrians visible against glare?
- Are there pedestrians walking on the carriageway because of encroached footpaths?
- School zones: see M.

**D. Cyclists & non-motorised vehicles (cycle rickshaws, carts)**
- Is there a segregated cycle track or wide paved shoulder/service road where NMT volumes justify?
- Are cycle tracks continuous through junctions, free of parked vehicles, drain gratings parallel to travel, utility poles?
- Are slow-vehicle lanes provided on NH through villages; are tractor-trolleys/carts mixing with high-speed traffic?
- Lighting and surface quality on NMT facilities; conflicts at bus stops.

**E. Motorcyclists / two-wheelers (very relevant: ~45 % of Indian road deaths)**
- Loose gravel, sand, mud, spilled diesel, water, algae or debris on the carriageway, especially on curves and at junction approaches?
- Surface irregularities: potholes, raised/sunken manholes, longitudinal cracks, edge drop-offs, raised lane markers, speed humps without markings, polished/bleeding bitumen, rumble strips too high.
- Steel W-beam barrier posts exposed on the outside of curves (need **rub rail / motorcycle protection system**); barrier ends unprotected; kerbs that can launch a motorcycle.
- Unexpected narrowing; two-wheelers squeezed by trucks at toll plazas and merges.
- Visibility of markings/signs at motorcycle headlight height at night.
- Illegal wrong-side riding generated by long gaps between median openings — are there designated U-turns?
- Adequate separation at high-speed sections; is a two-wheeler lane feasible?
- Helmet-use observation (for police persona), speed differential at curves.

**F. Public transport / bus stops** (IRC:80)
- Are bus bays/stops located away from junctions (≥75–100 m downstream), curves and crests?
- Do buses stop on the carriageway creating rear-end and overtaking conflicts? Is there a bus bay or layby with taper?
- Shelter, lighting, footpath connection, crossing within 50 m, no vendor encroachment?
- Informal bus/auto/shared-taxi stands on carriageway (very common at NH village junctions)?
- Are school buses stopping on the wrong side forcing children to cross?

**G. Parking & roadside activity** (IRC:SP:12)
- Parking on carriageway/shoulder reducing lane width or sight distance? Truck parking on shoulders at night (unlit) on NHs; dhaba clusters; parked vehicles at curves.
- Are parking bays marked and angled correctly; is reversing into traffic required?
- Roadside markets, weekly haats, fuel stations with multiple uncontrolled accesses, religious structures in the road space.

**H. Traffic signs** (IRC:67-2022; sheeting per ASTM D4956 — micro-prismatic Type XI mandated on NHs, Type IV minimum on other roads)
- Are mandatory, cautionary and informatory signs present where required (curve, junction, pedestrian crossing, school, hospital, speed limit, no overtaking, narrow bridge, animal crossing, accident-prone area)?
- Correct size for design speed; mounted at correct height and lateral offset; not obscured by trees, hoardings, poles; not damaged, faded, vandalised, rotated?
- **Retroreflectivity**: adequate at night (measure RA; sign legible at ≥150 m at 80 km/h)? Mixed sheeting types; damaged sheeting; non-standard colours/fonts; sign clutter; advertising confused with signage.
- Advance direction signs and overhead gantries at major junctions/exits; chevrons on curve outside; object markers/hazard markers on culvert ends, median noses, poles.
- Speed limit signage: consistent, repeated after junctions, credible; variable speed signs for school/fog?
- Temporary/work-zone signs left in place after works?

**I. Road markings & delineation** (IRC:35-2015)
- Centre line, edge lines, lane lines present and continuous? Correct pattern (no-overtaking solid lines on curves/crests)? Hatching at median noses, gore areas, island approaches?
- Visibility: worn/faded (<30 % remaining), not retroreflective at night (measure RL), obscured by dust/mud, bleeding bitumen covering markings?
- Raised pavement markers (cat's eyes) on curves and at median openings; delineator posts on embankments/curves; guard-rail reflectors; kerb painting.
- Transverse bar markings/rumble strips on approaches to junctions, toll plazas, built-up areas; speed hump markings and signs.
- Zebra crossings, stop lines, arrows, "SLOW/SCHOOL" legends, bus-stop markings, cycle markings.
- Conflicting/old markings not removed after realignment (ghost markings).

**J. Street lighting** (IS 1944, IRC:SP:... urban lighting; NH lighting at junctions/built-up/toll plazas)
- Is lighting provided at all junctions, pedestrian crossings, bus stops, built-up stretches, toll plazas, underpasses/FOBs, service roads?
- Uniformity and level adequate (measure lux); dark patches; lamps not working; vegetation blocking; poles in clear zone without breakaway/barrier; glare from opposing traffic or roadside premises?
- Is lighting continuous through transitions (lit→unlit) with a transition zone?
- Solar/high-mast lighting operational at the time of night audit?

**K. Roadside hazards, clear zone & safety barriers** (IRC:119-2015)
- Fixed objects within the clear zone (trees, poles, culvert headwalls, boulders, signposts, high-mast bases, kerbs on high-speed roads, temples/shrines, utility boxes, hoardings)?
- High embankments (>3 m), deep drains/canals/water bodies, bridge approaches, ravines without barrier?
- Barrier type appropriate (W-beam, thrie-beam, concrete, wire rope); correct height (≈700 mm to top of W-beam) and post spacing; **terminals/end treatments** (flared, buried, crash cushion) not blunt/"fish-tail"; transitions between barrier types; length-of-need adequate before hazard; barrier not damaged/missing sections; not too close to the hazard to deflect; motorcycle rub-rail where needed.
- Median barrier presence and continuity on divided roads; median openings protected by crash cushions/impact attenuators; median plantation blocking sight lines or acting as fixed objects.
- Bridge parapets/railings: height, continuity with approach barrier, kerb that can vault vehicles.
- Breakaway/frangible supports for signs/lighting.

**L. Drainage & weather** (IRC:SP:50, IRC:SP:42)
- Ponding/water-logging on carriageway; blocked side drains; drain covers missing (pedestrian/two-wheeler hazard); open drains adjacent to carriageway without barrier/cover.
- Hydroplaning risk from rutting; culvert inlets/outlets as hazards; scour at bridge approaches; flood-prone dips/causeways with depth gauges and signs.
- Fog-prone stretches: fog lights, raised pavement markers, VMS, speed limits? Monsoon landslide zones signed/protected?
- Dust/visibility from unpaved shoulders and roadworks.

**M. Pavement surface** (IRC:82 maintenance, IRC:SP:16)
- Potholes, raveling, rutting, corrugation, edge breaks, patch failures, bleeding, polished aggregate (low skid resistance), utility trenches not reinstated, manholes above/below grade, speed humps non-standard (IRC:99).
- Transitions at bridge joints/expansion joints; loose chippings after surface dressing; unmarked newly laid surface; unsealed shoulders with drop-off.
- Spot skid-resistance check at curves, junction approaches and pedestrian crossings.

**N. Traffic calming & speed management** (IRC:99-2018)
- Are speed-reducing measures present at village/town entries on NHs (gateways, transverse rumble strips, chicane, narrowing, raised crossings)? Are speed humps designed per IRC:99 (height/length, markings, signs) and not placed on NH main carriageway arbitrarily?
- Are operating speeds (85th percentile) consistent with posted limits and the environment; is there speed-camera/enforcement infrastructure?
- Toll plaza approaches: rumble strips, chevrons, lane markings, lighting, crash cushions, adequate taper.

**O. School zones & hospitals**
- School within 200 m of the carriageway? Are "School Ahead" signs, speed limit (≤30 km/h), raised/signalised crossing, footpath, gates set back, pick-up/drop-off zone off-carriageway, crossing guard, flashing beacons present?
- Hospital/emergency access, ambulance bays.

**P. Work zones / roadworks** (IRC:SP:55)
- Advance warning, taper lengths, channelising devices (cones/barricades with reflectors), speed limits, flagmen, night lighting of works, pedestrian diversions, protection of excavations/open trenches, debris/material on carriageway, end-of-works signs, old works signs left in place.
- Half-width construction on NHs: median crossovers signed/lit; dust; water tankers; uncontrolled haul-road access.

**Q. Medians & median openings / U-turns**
- Spacing and location of openings (not on curves/crests, not within junction influence); length adequate for storage; **unauthorised/illegal median cuts** (very common); openings protected (crash cushion/impact attenuator, hazard markers, lighting); U-turn geometry (radius for buses/trucks); conflict with pedestrians using opening as crossing; median railings broken.

**R. Access control & frontage**
- Uncontrolled private/commercial accesses, fuel stations with full-width aprons, ramps over footpaths/drains; service roads not used because of missing entries/exits; wrong-way use of service roads; toll-plaza bypass lanes.

**S. Vulnerable road users (combined walk-through view)**
- Do VRU facilities form a continuous network? Points where VRUs are forced into traffic; mobility-impaired access (ramps, tactile); animal-drawn and hand carts; elderly crossing times; children at bus stops.

**T. Night-time conditions (mandatory night drive)**
- Sign/marking retroreflectivity; lighting outages; unlit obstructions (parked trucks, construction, barricades, animals, pedestrians in dark clothing); glare from roadside premises and oncoming traffic; delineation of curves/median openings/bridge ends; visibility of speed humps/rumble strips; illuminated signs working.

**U. Animals**
- Cattle/stray dog/wildlife crossing zones; signage; fencing; animal underpasses/overpasses in forest stretches; cattle resting on warm carriageway at night; cattle-catching arrangements by ULB.

**V. Encroachments, hawkers & informal activity (India-specific)**
- Hawkers/vendors on carriageway/shoulders/junctions; temporary structures in the ROW; dhabas/mechanic shops with vehicles on the road; religious structures; weekly markets; wedding tents; dumping of construction debris/garbage; signage hidden by hoardings; political banners on poles; illegal speed breakers built by residents.

**W. Wrong-side driving & wrong-way movements**
- Where and why (long gaps between U-turns, missing service-road entries, median openings closed, convenience access to fuel stations/villages); count during observation; conflict with high-speed traffic; are "No Entry/Wrong Way" signs, channelisers and enforcement present; do service roads run two-way?

**X. Toll plazas, rest areas, truck lay-bys, emergency facilities**
- Approach signage and speed reduction, lane markings/canopy lighting, crash cushions at islands, pedestrian safety for toll staff, FASTag lane merging; truck lay-bys & rest areas spacing (every ~50 km on expressways), emergency call boxes/SOS, ambulance posts, helpline signage, emergency crossovers.

**Y. Bridges, culverts, ROBs/RUBs, flyovers**
- Width transition (narrow bridge on wide road), approach guard rail, parapet height, expansion joint condition, approach settlement (bump), drainage spouts, lighting, pedestrian path on bridge, chevrons at skewed RUB, height gauge for low RUBs, flyover ramp merging, median opening at flyover ends.

**Z. Hill / ghat roads (IRC:52, IRC:SP:48)**
- Hairpin bends and sight lines, parapet/crash barrier on valley side, landslide/shooting-stone zones, retaining walls, convex mirrors at blind bends, water on carriageway, passing places, grade and length, brake-failure runaway ramps, fog.

For each item the product should record: **present / absent / deficient / not applicable**, evidence frame(s), measurement (if any), and whether a *night* check is required.

---

## 4. User personas

Common legal/regulatory hooks referenced below:
**MVAA 2019 S.198A** (designated authority/contractor/consultant/concessionaire liable; fine up to ₹1 lakh where non-compliance causes death or disability, paid into the S.164B Motor Vehicle Accident Fund; "contractor" includes sub-contractors and all persons responsible for any stage of design/construction/maintenance) · **S.210D** (central standards) · **S.215** (SRSC/DRSC) · **MoRTH circulars** (2018 DPR-stage RSA; 2019 RSA on all NHs; 2020 independent all-stage RSA; 2015 black-spot protocol; 2019 black-spot sanction format) · **IRC:SP:88-2019** · **SCCoRS directions (30.11.2017 and later)** · **SC *Phalodi* order 13.04.2026** · **CAG performance audits** on road safety (2026 chapter cites missing RSAs) · **Highway Rating SOP** (Safety 35 marks).

### 4.1 Certified Road Safety Auditor (independent consultant / empanelled Senior RSA)
- **Goals**: produce an IRC:SP:88-compliant report quickly, defensibly and consistently across a 100–300 km stretch; win and retain empanelment; avoid missing an Essential finding that later features in a fatal-crash inquiry.
- **Decisions**: what to flag, risk rating per finding, which code clause to cite, what to recommend, which locations need instrumented verification or night re-visit.
- **KPIs**: km audited per day, findings per km, time from site visit to draft, % findings accepted by client, repeat business, zero "missed hazard" incidents.
- **Needs from the product**: chainage/GPS-anchored finding log with frames; pre-filled IRC checklist with evidence; draft risk rating that they can override (auditor remains the signatory); code citations; night-audit gap list; exportable **PDF (IRC format)**, **DOCX** for editing, **XLSX finding register**, **GeoJSON/KML** for strip map, photo log ZIP; audit trail (who changed what); signature block with empanelment number; declaration of independence.
- **Hooks**: IRC:SP:88 reporting format; MoRTH 21.11.2025 certification requirement; professional liability under S.198A ("consultant").

### 4.2 Municipal Corporation engineer / PWD Executive Engineer (road-owning agency)
- **Goals**: comply with SCCoRS/DRSC directions and CAG scrutiny; fix black spots within the MoRTH calendar; spend maintenance budget where it reduces crashes; respond to court/RTI/press queries about a specific fatal crash.
- **Decisions**: which findings to accept/reject (response report), prioritisation into the annual maintenance plan and estimates, sanction of short-term vs long-term measures, work orders to contractors, attendance at DRSC with status.
- **KPIs**: black spots rectified vs identified (MoRTH MIS), % Essential findings closed within 30/90 days, crash/fatality reduction on treated stretches, compliance with DRSC minutes, audit observations by CAG.
- **Needs**: ward/division-wise summary; **cost-classed action plan** (immediate ≤₹1 lakh, short-term, long-term with rough BoQ heads); **Excel** register importable into their works MIS; **CAD/DXF or GeoJSON** of junction fixes for the DPR consultant; before/after photo compare; letter-ready "response report" template; Hindi/regional-language summary.
- **Hooks**: S.198A ("designated authority"); S.215 DRSC; MoRTH black-spot protocol & 26.08.2019 sanction format; SCCoRS compliance returns; state circulars (e.g. Maharashtra 2019: 1 % of project cost for RSA on projects ≥5 km).

### 4.3 NHAI Project Director / Independent Engineer (IE) / Authority Engineer
- **Goals**: pass MoRTH Highway Rating (Safety 35 marks), close NHAI Road Safety Cell observations, ensure concessionaire meets Schedule L, rectify black spots on the PIU's stretch, avoid adverse findings after high-profile crashes (e.g. Samruddhi, Phalodi).
- **Decisions**: issue non-compliance notices to concessionaire/contractor, approve change-of-scope for safety works, accept/reject RSA recommendations, programme RSAs (all-stage, independent), input to MoRTH MIS.
- **KPIs**: Highway Rating safety score; black spots rectified; RSA findings open/closed; crash KPIs from eDAR for the stretch; MoRTH/NHAI RO compliance deadlines; SCCoRS/SC task-force reporting.
- **Needs**: findings mapped to **Schedule L / MCA clauses** and **IRC:SP:84/87 standards** so penalties are enforceable; chainage in NHAI format (km+m, LHS/RHS per increasing chainage); segregation of concessionaire O&M defects vs authority capital works; **iRAP-style star band** (NHAI already partners with IndiaRAP); IE-ready **PDF + Excel**; integration hooks for NHAI's **Data Lake / PMIS**, **Black Spot MIS** and **Rajmargyatra** complaints.
- **Hooks**: MoRTH 09.11.2020 circular; NHAI Jan 2023 mandatory third-party DPR RSA; MCA Schedule L & Schedule N (Independent Expert ToR); S.198A ("designated authority", "concessionaire"); SC *Phalodi* order (24×7 route patrols at ≤50 km intervals; District Highway Safety Task Forces; licence/NOC review in highway safety zones).

### 4.4 Traffic Police (DCP Traffic / SP Traffic / Highway Patrol)
- **Goals**: reduce fatalities in their jurisdiction; have engineering evidence to push road agencies at DRSC; target enforcement (speed, wrong-side, helmet) at the right places; investigate fatal crashes with road-condition evidence.
- **Decisions**: where to deploy patrols/cameras/interceptors, what to raise at DRSC, whether to register a case against a road agency after a crash (S.198A / IPC/BNS negligence), temporary measures (barricades, diversions, hawker clearance with ULB).
- **KPIs**: fatalities/grievous injuries (eDAR), black spots in their jurisdiction, enforcement challans by location, response time, DRSC action-taken reports.
- **Needs**: **map-first view** of findings with crash overlay (import eDAR CSV); plain-language one-pager per black spot ("what is wrong, who must fix, by when"); evidence pack (geo-tagged frames, timestamps) usable in crash-case files; wrong-side/encroachment/parking hotspot layer; **PDF + KML**; WhatsApp-sized summaries.
- **Hooks**: S.215 DRSC membership; eDAR obligation (S.159 accident information reports); SCCoRS directions on enforcement; Section 198A complaints.

### 4.5 Urban planner / Smart City SPV / UMTA
- **Goals**: integrate safety into street redesign (complete streets, junction redesign like BBMP Suraksha 75), prioritise capital projects, meet Bloomberg/WRI/ITDP programme metrics.
- **Decisions**: project selection and design briefs, tactical-urbanism trials, budget allocation, consultant ToRs.
- **KPIs**: km of footpath/cycle track, junctions redesigned, pedestrian fatalities, iRAP pedestrian star rating, modal share.
- **Needs**: **GIS layers (GeoJSON/Shapefile)** of deficiencies by category, junction-level dossiers, cross-section measurements, pedestrian-facility inventory, **DXF** base for designers, dashboards across the network, repeatability (re-run after works).
- **Hooks**: IRC:103, IRC:86, IRC:99; Smart City/AMRUT guidelines; state street-design guidelines (e.g. Pune Urban Street Design Guidelines, Delhi UTTIPEC).

### 4.6 Concessionaire O&M manager / Toll operator / EPC contractor (DLP period)
- **Goals**: avoid IE non-compliance notices and penalties, meet Schedule L and Highway Rating, keep O&M costs down, document that defects were not theirs (e.g. third-party damage), close defects before NHAI inspections.
- **Decisions**: daily patrol work orders, barrier/sign replacement, median-cut closure, encroachment reporting to NHAI/district administration, budget for safety consultant audits.
- **KPIs**: defects open/closed, time-to-repair, IE penalties, crash counts on stretch, Rajmargyatra complaints.
- **Needs**: **defect register with ticket IDs**, repeat-run change detection (new vs recurring vs fixed), photo evidence with timestamps, **Excel/CSV + API** into their maintenance management system, split of "within O&M scope" vs "authority scope".
- **Hooks**: MCA Schedule L safety requirements; S.198A ("concessionaire", "contractor" incl. sub-contractors); MoRTH 2020 circular (independent audits — the concessionaire must *facilitate* but not conduct).

### 4.7 NGO / citizen activist (SaveLIFE Foundation, Raahgiri/WRI, Parisar, Footpath Initiative, RTI activists)
- **Goals**: evidence-based advocacy; hold agencies accountable; run corridor programmes (ZFC) and tactical trials; public awareness.
- **Decisions**: which corridors/junctions to campaign on, what to file (RTI, PIL, DRSC representation, S.198A complaint), what to publish.
- **KPIs**: fatalities on adopted corridors, issues closed by agencies, media/policy uptake.
- **Needs**: citizen-friendly **PDF/HTML** with maps and photos, open-data **CSV/GeoJSON**, issue tracker with agency responsibility, before/after comparisons, ability to crowd-source phone video from volunteers.
- **Hooks**: RTI Act; S.198A; SCCoRS public grievance; Supreme Court *Phalodi* task forces.

### 4.8 Insurer / reinsurer / motor TP claims
- **Goals**: price corridor risk, reduce TP claim costs, support subrogation/contribution claims against road agencies where road defect caused the crash, ESG/road-safety CSR reporting.
- **Decisions**: fleet telematics incentives, CSR funding of corridor fixes (e.g. ZFC funded by insurers/corporates), claim investigation.
- **KPIs**: claims frequency/severity by corridor, loss ratio, lives saved on sponsored corridors.
- **Needs**: **segment-level risk scores (100 m)**, machine-readable **CSV/API**, evidence packs linked to eDAR accident IDs, trend over time.
- **Hooks**: eDAR (used for MACT claim settlement, interim reports within 3 months per S.159 rules); S.164B fund; MACT jurisprudence on contributory negligence of road agencies.

### 4.9 District Road Safety Committee (DRSC) — Collector/DM (chair), SP, CMO, PWD/NHAI/ULB engineers, RTO, NGO member
- **Goals**: statutory fortnightly/monthly review (Odisha mandates ≥fortnightly virtual meetings), close black spots, comply with SCCoRS & state RSC directions and now the SC *Phalodi* District Highway Safety Task Force mandate (constituted within 15 days of the 13.04.2026 order).
- **Decisions**: assign responsibility by agency, deadlines, escalation to state, fund short-term fixes from district/road-safety fund, enforcement drives.
- **KPIs**: black spots rectified, action-taken-report compliance, fatalities vs previous year (eDAR), meeting regularity.
- **Needs**: **one-page agency-wise action table** (finding → responsible agency → deadline → status), district map, printable PDF, auto-generated minutes annex, SMS/WhatsApp reminders.
- **Hooks**: S.215(3); SCCoRS uniform-composition letter; MoRTH black-spot calendar (data by 15 Jan, identification by 28 Feb, short-term report by 15 Apr, DPR by 1 Jun, permanent fix by 30 Sep — Kerala/MoRTH adaptation).

### 4.10 Court-appointed bodies — Supreme Court Committee on Road Safety (Justice Sapre), High Court committees, amicus curiae, Lokayukta
- **Goals**: verify state compliance; order time-bound rectification (e.g. Indore/Bhopal/Jabalpur black spots in 2025); build state-specific frameworks (SC order Jan 2023).
- **Decisions**: directions to states/agencies, compliance affidavit demands, identification of defaulting agencies.
- **KPIs**: black spots rectified, RSAs conducted by all road-owning agencies (a 2017 SCCoRS note recorded that agencies other than PWD had not followed the RSA direction), lead-agency/fund/DRSC establishment.
- **Needs**: **auditable, standardised, independent** evidence — fixed report schema, signed PDF with hash, GIS layer, compliance dashboard across districts, ability to re-audit the same stretch and show closure.
- **Hooks**: Article 21 (SC *Phalodi*, 2026); Article 142 interim directions; contempt jurisdiction.

### 4.11 Others worth designing for
- **MoRTH/State Transport Dept Road Safety Cell & Lead Agency** (state-level dashboards, Section 215 councils).
- **DPR consultant** (needs existing-road findings as input to rehabilitation DPR; wants DXF/GeoJSON and inventory).
- **Multilateral project teams (World Bank/ADB)** – want iRAP star ratings + IRC:SP:88 audit + ESS4 road-safety compliance evidence.
- **Media** – one-page infographic with map.

---

## 5. Existing products & competitors

| Product | Inputs | Outputs | Accuracy / scale claims | Pricing (public) | Strengths | Gaps vs an Indian RSA |
|---|---|---|---|---|---|---|
| **iRAP ViDA / Star Rating (IndiaRAP via AITD; AusRAP, etc.)** | Geo-referenced video/imagery coded manually or with AI (iRAP-accredited coders; AiRAP accelerators), traffic & speed data | 100 m star ratings for 4 user groups, SRIP countermeasure plan, FSI saved, BCR, maps | Global standard; UN targets; >1.5 M km rated; coding consistency depends on accredited coders | Software free for accredited users; coding/survey services commercial (₹ per km); accreditation courses paid | Evidence-based, internationally recognised, investment-planning output, NHAI/World Bank/ADB uptake | Not an IRC:SP:88 audit; no finding-level defects (e.g. a broken barrier or a hawker) — rates attributes, not maintenance condition; needs trained coders; outputs not in IRC risk/priority language |
| **RoadBotics / Michelin "RoadWay"** (acquired by Michelin July 2022, folded into Michelin DDi) | Smartphone dashcam video | Pavement condition rating 1–5 per ~3 m, map, asset inventory | Used by >250 governments (pre-acquisition) | Not public; municipal subscriptions | Easiest phone-based workflow; good pavement models | Pavement-centric; no safety-audit logic; US/Europe road assumptions; weak on VRU/signage/barriers |
| **Vaisala Xweather RoadAI** | Smartphone video from maintenance/inspection vehicles | Pavement defects (20+ classes), **traffic-sign inventory & condition**, missing/new sign alerts, map/dashboard | Deployed by UK councils (Northumberland, Milton Keynes), Nordics | UK G-Cloud listing **£8,500–£250,000 per licence per year** | Sign inventory + pavement, workflow integration, subscription SaaS | No RSA findings/risk ratings; no Indian sign taxonomy (IRC:67); no VRU/encroachment logic |
| **Mobileye (REM / Data Services)** | Crowd-sourced data from Mobileye-equipped vehicles | HD map layers of signs, poles, markings, lane geometry; infrastructure change detection (Ordnance Survey UK trials) | Fleet-scale, high positional accuracy | Enterprise/OEM contracts | Scale and freshness | Not available as a municipal audit product in India; no audit/risk logic; vehicle-centric |
| **Mapillary (Meta)** | Crowd-sourced street-level images | Object detection incl. traffic signs (~1,500 classes), point features, open imagery | Free platform; coverage patchy in India | Free | Open, API, OSM integration | No safety assessment; coverage/timeliness; no Indian signage classes |
| **Google (Maps data; Road Management Insights for road authorities)** | Probe data | Traffic speeds, congestion, incident patterns, route analytics for agencies | — | Agency programmes | Speed/volume proxy useful as input to risk | No visual infrastructure assessment; not an audit |
| **RoadMetrics (Bengaluru)** | Phone mounted on windshield; AI | Potholes, cracks, faded markings, missing signs; GIS dashboard with green→red road grades; municipal reports | ">50,000 km", "~90 % accuracy on 100k data points from 3 cities"; Surat pilot; Telangana AI Mission/GHMC challenge; seed from 100X.VC | Not public; B2B/B2G contracts | Indian road conditions in training data; municipal traction | Road-condition / asset tool, not RSA; no IRC checklist, risk matrix, VRU, night audit, crash integration |
| **Intents Mobi (Intents Go)** | Smartphone sensors (accelerometer/GPS), user reports; HERE maps | Pothole/speed-breaker/water-logging alerts; road condition map | Consumer app | Free app | Crowd-sourced hazard layer | Consumer navigation; no audit output |
| **RoadBounce (Pune)** | Smartphone accelerometer | Roughness (IRI proxy), pothole detection | Startup-stage | — | Cheap roughness | Pavement only |
| **Ola / Uber (Guardian, RideCheck, telematics)** | Trip telematics, harsh-braking events | Internal safety analytics, some city partnerships (e.g. Uber Movement speeds, discontinued 2023) | Fleet-scale | Not a product | Could supply speed/harsh-event layers | No infrastructure assessment |
| **iRASTE (Nagpur, 2021–May 2024; Intel, INAI/IIIT-H, CSIR-CRRI, Mahindra, NMC)** | ADAS cameras on ~city buses, GPS, driver alerts; road-condition AI | Collision alerts to drivers; "grey spots"/black spots from near-miss data (37 black spots identified from bus data); engineering recommendations by CRRI | Aimed at 50 % crash reduction; no published before/after fatality data | Grant-funded pilot | Near-miss-based proactive hazard discovery; CRRI engineering follow-through | Project concluded; not a product; needs instrumented fleet |
| **IIT Madras CoERS (TARA, Sanjaya, eDAR analytics, DDHI 100 districts)** | eDAR/iRAD data, police records | Crash dashboards, hotspot maps, district action plans | Nationwide via MoRTH | Government | Authoritative crash data layer | Reactive (crash-based); no infrastructure vision |
| **RASSI / JP Research India** | On-site in-depth crash investigation teams (6 centres; 7,000+ crashes) | Causation database (vehicle, road, human factors); national projections | Research-grade | Consortium-funded (OEMs) | Deep causal insight on road-factor contributions | Sample-based; not a survey tool |
| **Bengaluru Traffic Police (ASTraM, AI cameras, BTP Road Safety Report with Vital Strategies)** | ITMS cameras, FIR data | Black-spot lists (43 in 2023 report; 64 for 2023–25), corridor lists, enforcement analytics | City-scale | Government | Data-driven targeting | Engineering fixes depend on BBMP/NHAI; no systematic infrastructure audit |
| **Delhi iRAD/eDAR, PWD "AI traffic & safety audit" of 420 km South Delhi (2025 plan), ITMS 3D radar cameras** | eDAR, CCTV | Crash data; congestion/CCTV coverage study | 36 States/UTs on eDAR; Kalyanpuri PS first eDAR station (2024) | Government | National crash data standard with 10 forms (FAR, driver, owner, interim report, victim, DAR, mechanical inspection, etc.) | eDAR records "road features" coarsely; no imagery-based audit |
| **State AI pilots** – ITI Ltd AI road-safety pilot (UP), Andhra Pradesh AI corridor screening (384 corridors), Roadvision.ai, Geovista (iRAP Karnataka) | Video/eDAR | Hazard screening | Early | Tender-based | Government appetite for AI tools exists | Fragmented; none produce an IRC:SP:88 report |

**What "best-in-class" would do (gap this product can own)**

1. Ingest ordinary phone video (day + night) with GPS, auto-compute chainage against the road's km-stone/strip map, and segment into 100 m bins.
2. Detect and *measure* the full IRC:SP:88 existing-road checklist (not only potholes/signs): barriers & terminals, median openings, VRU facilities, encroachments, wrong-side movements, bus-stop conflicts, lighting outages (from night pass), sign retroreflectivity *proxy* (night-pass luminance), marking visibility, roadside hazards and clear-zone estimation.
3. Output an **IRC:SP:88-formatted report** with risk matrix and priorities, **plus** an iRAP-style star band per 100 m, **plus** a defect register — one dataset, three audiences.
4. Fuse **eDAR crash data** (and MoRTH black-spot list) to show "deficiency + crash history" and to automate the MoRTH 500 m sliding-window black-spot test.
5. Keep the **certified auditor in the loop** (override, sign, empanelment number) so the output is legally an RSA, not a machine opinion.
6. Track findings to closure across repeat drives (change detection) for O&M/DRSC/court use.
7. Export PDF/DOCX/XLSX/GeoJSON/Shapefile/DXF/KML and an API.

---

## 6. Legal & regulatory

### 6.1 Motor Vehicles (Amendment) Act 2019
- **S.198A – Failure to comply with standards for road design, construction and maintenance**: (1) any *designated authority, contractor, consultant or concessionaire* responsible for design/construction/maintenance of a road shall follow the standards notified by the Central Government; (2) where failure results in **death or disability**, the responsible party is liable to a fine **up to ₹1,00,000**, credited to the Motor Vehicle Accident Fund (S.164B). Explanation: "contractor" includes sub-contractors and all persons responsible for any stage of design, construction and maintenance. Commentators note that, as of 2026, **no agency has reportedly been penalised** under it — but it is the hook every persona cites, and an RSA report that documents a known, unrectified Essential finding is the evidence a prosecution or MACT claim would use.
- **S.210D** – Central Government power to make rules on design, construction and maintenance standards for NHs (and standards for other roads through states).
- **S.215** – State Road Safety Council and **District Road Safety Committees** (DM/Collector chair; SP, CMO, PWD/NHAI/ULB engineers, RTO, NGO members; uniform composition pushed by SCCoRS).
- **S.135 / S.136A** – crash investigation schemes; electronic monitoring and enforcement.
- **S.159 & rules** – police to file accident information reports (eDAR) and interim reports to MACT within 3 months.
- **S.164B** – Motor Vehicle Accident Fund.

### 6.2 MoRTH mandates on RSA
- **04.07.2018** – RSA at engineering-design (DPR) stage for new road projects (states apply it to projects **≥5 km**; Maharashtra earmarks **1 % of project cost** for RSA).
- **20.09.2019** – RSA recommended on **all NHs** with follow-up action on recommendations.
- **09.11.2020** – **All-stage RSA through Independent Road Safety Experts** (design, construction, pre-opening, O&M), engaged through the IE/AE or directly by MoRTH/NHAI/PWD; concessionaires may not audit themselves.
- **01.07.2021** – procedures for third-party RSA (referenced in NHIDCL/NHAI RFPs).
- **Jan 2023 (NHAI)** – third-party RSA at DPR stage mandatory for all projects; FY22 16,500 km audited.
- **21.11.2025** – RSA personnel must hold IAHE/designated-institute certification.
- **Highway Rating SOP (2021)** and **Oct 2026 notification** – safety component of NH performance rating.
- **Policy guidelines on Network Survey Vehicles (13.11.2019)** – MoRTH already accepts vehicle-mounted imaging surveys for condition; precedent for video-based evidence.

### 6.3 IRC:SP:88-2019 as a requirement
Referenced in MoRTH circulars, NHAI/NHIDCL RFPs, state PWD circulars and CAG audits as *the* method; CAG's 2026 performance-audit chapter faulted a state for not conducting audits at design/construction/completion stages as IRC requires.

### 6.4 Black spots
- **MoRTH OM 28.10.2015** – *Protocol for identification and rectification of road accident black spots on NHs*: a black spot is a **~500 m stretch** on which **either ≥5 road accidents (involving fatalities/grievous injuries) in the last 3 calendar years, or ≥10 fatalities in the last 3 calendar years**, occurred. Process: identification (police data → RO/PIU), site investigation/RSA, **short-term measures** (signs, markings, rumble strips, lighting, barriers — within weeks), **long-term measures** (geometric correction, grade separation, service roads — via DPR & sanction), monitoring; MoRTH's 2017 Kolkata workshop deck frames it as a continuous process with ROs empowered to take immediate cautionary measures.
- **26.08.2019 circular** – format for preparing and sanctioning black-spot rectification proposals.
- **Black Spot MIS (blackspot.morth.gov.in)** – tracks identified/sanctioned/rectified (temporary vs permanent). Reported totals: 13,795 black spots identified (2016–2022 cycle) with ~4,777 permanently rectified by Dec 2024; target of ~9,000 rectified by March 2025; parliamentary panel criticised the pace.
- States run calendars (Kerala): data by 15 Jan → identification by 28 Feb → short-term report by 15 Apr → DPR by 1 Jun → permanent fix by 30 Sep. Maharashtra's 2019 GR separates temporary and permanent measures with estimates/drawings.
- Bengaluru Traffic Police and other city police use the identical 500 m / 5-crash / 10-fatality definition.

### 6.5 Supreme Court
- **S. Rajaseekaran v. UoI (W.P.(C) 295/2012)** – SCCoRS constituted 22.04.2014 (Justice K.S. Radhakrishnan; members S. Sundar, Dr Nishi Mittal; later Justice A.M. Sapre with Sanjay Mitra and Dr Nishi Mittal). **30.11.2017 order** directed every state to: adopt a road safety policy, constitute State Road Safety Council and **Lead Agency**, create a **Road Safety Fund**, form **DRSCs**, prepare district/state action plans, conduct **road safety audits**, apply engineering design standards, install traffic-calming, improve trauma care, and report. SCCoRS later (2017) recorded that road-owning agencies other than PWD had not complied with the RSA direction; 2022 letter on black-spot identification using the 4Es; Jan 2023 SC asked SCCoRS to frame state-specific frameworks; 2025 site inspections in MP (Indore, Bhopal 16 black spots, Jabalpur) with time-bound rectification orders.
- ***In Re: Phalodi Accident* (suo motu; order 13.04.2026, 2026 INSC 388)** – after 34 deaths in Phalodi (Rajasthan) and Rangareddy (Telangana) crashes of 2–3 Nov 2025, the Court held commuter safety on highways is an integral facet of **Article 21** and issued Article 142 interim directions: no licence/NOC/trade approval for premises in *highway safety zones* without NHAI/PWD clearance and review of existing ones within 30 days; **District Highway Safety Task Forces** within 15 days; NHAI tracked **24×7 route patrol vehicles at ≤50 km spacing**; black-spot identification, lighting, inter-agency coordination; MoRTH compliance reporting (60–75 days per different reports **[verify]**). Context cited: NHs ≈2 % of network but ≈30 % of deaths; 1.72–1.77 lakh road deaths/yr (2023–24).

### 6.6 Crash data: iRAD / eDAR
- **iRAD** (Integrated Road Accident Database; MoRTH, World Bank-funded, NIC + IIT Madras CoERS) rolled out 2021–22, all 36 States/UTs by Nov 2022; renamed/extended as **eDAR (electronic Detailed Accident Report)**, live 2024 (first station Kalyanpuri, Delhi). Stakeholders: Police, Health, Transport (RTO), Road-owning agencies (NHAI/PWD/ULB).
- **Ten forms**: First Accident Report (FAR), Driver, Owner, Interim Accident Report (IAR), Victim, Detailed Accident Report (DAR), Mechanical Inspection Report, hospital/medical, road-authority spot inspection, etc. Fields include GPS spot, date/time, road classification (NH → State/RO/PIU/UPC code/project name), description, vehicle & victim details, severity (Killed/Grievous/Minor/No injury), photos/video, and road-feature attributes (junction type, road feature, weather, light — **[field list verify against state user manuals]**).
- Used for MACT claims (interim report in 3 months), for MoRTH black-spot identification "with real-time eDAR data", and by CoERS "Sanjaya" hotspot platform and the **Data-Driven Hyperlocal Intervention** programme (100 high-risk districts). Our product should import eDAR exports (CSV) and reference eDAR accident IDs in findings.

### 6.7 Standards cited in findings (quick reference)
IRC:67-2022 (signs; Type XI micro-prismatic sheeting on NHs, Type IV minimum elsewhere; 10-yr warranty Class C) · IRC:35-2015 (markings) · IRC:119-2015 (traffic safety barriers; under revision) · IRC:99-2018 (traffic calming/speed humps) · IRC:103-2022 (pedestrian facilities) · IRC:11 (cycle tracks) · IRC:80 (bus bays) · IRC:SP:12 (parking) · IRC:SP:55 (work-zone safety) · IRC:SP:41 (at-grade junctions, rural) · IRC:65 (roundabouts) · IRC:SP:90 (grade separators) · IRC:93 (signals) · IRC:SP:84 (4-lane), IRC:SP:87 (6-lane), IRC:SP:73 (2-lane), IRC:SP:99 (expressways) · IRC:86 (urban cross-sections) · IRC:SP:50 (urban drainage), IRC:SP:42 (road drainage) · IRC:82 (maintenance) · IRC:52/IRC:SP:48 (hill roads) · IS 1944 (street lighting) · MoRTH Specifications for Road & Bridge Works Section 800 (traffic signs, markings, barriers materials) · ASTM D4956 / IS 15684 (retroreflective sheeting). **[Edition years to be confirmed against the IRC 2026 catalogue.]**

---

## 7. Proposed CFI report specification

### 7.1 Design principles
1. **IRC:SP:88-2019-shaped** so a Senior RSA can sign it and an EE/PD can file it.
2. **Every finding is a record**: location, evidence, risk, standard breached, recommendation, owner, cost class, timeframe, status.
3. **Three views from one dataset**: (a) formal RSA report (PDF/DOCX); (b) defect/action register (XLSX/CSV/API); (c) GIS layers (GeoJSON/Shapefile/KML/DXF).
4. **Human-signed**: machine findings are "draft" until a certified auditor accepts/edits them; the report records both the model version and the auditor.
5. **Repeatable**: same stretch re-run → change report (new / persisting / resolved).

### 7.2 Finding identifier
`CFI-RSA-<PROJECT>-<DIR>-<CHAINAGE>-<CAT>-<NN>`

- `PROJECT`: short project code (e.g. `NH48-PKG3`, `BBMP-ORR`).
- `DIR`: `A` = increasing chainage carriageway, `B` = decreasing, `L`/`R` for LHS/RHS on undivided roads, `J` for junction-level, `X` for both/cross-section.
- `CHAINAGE`: `KKK+MMM` (e.g. `012+350`); for roads without chainage, a derived chainage from the user-defined datum plus a `GEO` suffix carrying the H3 cell or rounded lat/long in metadata.
- `CAT`: category code from the checklist: `ALN` alignment/cross-section · `INT` intersection · `PED` pedestrian · `CYC` cyclist/NMT · `MTC` motorcyclist · `BUS` public transport · `PRK` parking · `SGN` signs · `MRK` markings/delineation · `LGT` lighting · `RSH` roadside hazard/barrier · `DRN` drainage/weather · `PVT` pavement surface · `TCM` traffic calming/speed · `SCH` school/hospital zone · `WZN` work zone · `MED` median/opening/U-turn · `ACC` access control · `VRU` vulnerable users (combined) · `NGT` night-specific · `ANM` animals · `ENC` encroachment/hawkers · `WSD` wrong-side driving · `TOL` toll/rest/emergency · `BRG` bridge/culvert/structure · `HIL` hill road.
- `NN`: sequence within that chainage+category.
- Example: `CFI-RSA-NH48-PKG3-A-012+350-MED-01` = first median-opening finding at km 12+350 on the increasing-chainage carriageway.

### 7.3 Severity / risk scheme (machine-proposed, auditor-confirmed)
- **Likelihood** (Austroads/IRC): Frequent / Probable / Occasional / Improbable — proposed from exposure proxies (AADT class, VRU flow, speed class, crash history in 500 m, observed conflicts in video).
- **Severity**: Catastrophic / Serious / Minor / Limited — proposed from operating speed, hazard type and road-user vulnerability (Safe System impact-speed thresholds: 30 km/h pedestrian, 50 km/h side impact, 70 km/h head-on).
- **Risk** = matrix cell → **Very High / High / Medium / Low** (IRC labels; Austroads cell shown in tooltip).
- **Priority label** = Essential / Highly Desirable / Desirable / Optional (IRC Table 4.3 wording; "Optional" for Low).
- **Timeframe** = Immediate (≤7 days) / Short (≤90 days) / Medium (≤12 months) / Long (DPR/capital).
- **Cost class** = C0 (<₹50k) / C1 (<₹5 lakh) / C2 (<₹50 lakh) / C3 (>₹50 lakh).
- **Confidence** = model confidence (High/Medium/Low) and *"Field verification required"* flag naming the instrument (retroreflectometer, lux meter, speed gun, skid tester, tape).
- **Legal flag** = `S198A-relevant` when the finding is a non-compliance with a notified standard that can cause death/disability; `BLACKSPOT` when within a MoRTH black spot or where the 500 m window test is met.
- **Indicative star band** (per 100 m, per user group) shown separately and clearly labelled "indicative, not an accredited iRAP rating".

### 7.4 Report sections (government-grade)

**Front matter**
1. Cover: title, road & stretch (from–to chainage, km), stage ("Stage 5 – Existing Road"), client, auditor organisation, report no./version, date, QR to online map.
2. Audit statement & signatures: Team Leader (Senior RSA, empanelment/certificate no.), team members, declaration of independence, statement that findings are the auditor's professional opinion; CFI model version and processing date.
3. Document control (revisions, distribution).
4. Executive summary (≤2 pages): counts by priority, top-10 Essential findings with chainage, black spots covered, headline recommendations, indicative star distribution, action-plan summary.

**Part A – Context**
5. Introduction: scope, ToR, stage, standards applied (IRC:SP:88-2019 + list), limitations (e.g. video-based; night pass date; items not measurable).
6. Road description: classification & function, length, carriageway configuration by section, design speed/posted speed, land use, structures, toll plazas, junction list (table), service roads, O&M regime (concession/EPC/departmental).
7. Data reviewed: drawings, previous audits, eDAR crash data (period, counts by severity and type, black-spot table with MoRTH test), traffic & speed data (source), complaints.
8. Methodology: drives (dates, times, weather, light, direction, vehicle, camera/GPS setup), walk-throughs, detection pipeline summary, checklist used (Annex), risk-rating method (matrix reproduced), QA by auditor.

**Part B – Findings**
9. Summary dashboard: findings by category × priority (matrix table), findings per km, map of all findings (strip map), category heat-strip along chainage.
10. **Findings register (main table)** — one row per finding, chainage-ordered, columns:
    `ID | Chainage (km+m) | Side/Dir | Lat,Long | Category | Sub-item (checklist ref) | Observation | Evidence (frame IDs, photo nos.) | Crash history within 500 m (eDAR count F/GI/MI) | Road users at risk | Likely crash type | Likelihood | Severity | Risk | Priority | Standard breached (code & clause) | Recommendation (short-term) | Recommendation (long-term) | Cost class | Timeframe | Responsible agency | Verification required | Legal flags | Status | Client response | Auditor remarks`
11. **Finding sheets** (one per Very High/High finding; grouped for Medium/Low): photo(s) in direction of travel with chainage overlay, map inset, description, risk cell, recommendation with sketch where useful, code citation, before/after placeholder.
12. **Black-spot dossiers**: for each MoRTH black spot or window-test hit — crash table, collision diagram (from eDAR), site findings, short-term & long-term measures in the 26.08.2019 proposal format.
13. **Junction dossiers**: per junction — type, control, approach speeds, VRU facilities, findings, layout sketch (DXF export).
14. **Night audit section**: lighting inventory (working/not), sign/marking visibility by chainage, unlit hazards.
15. **Indicative 100 m risk profile**: table/plot per user group; sections below 3★-equivalent highlighted.

**Part C – Action**
16. **Prioritised action plan**: Essential → Optional; per item: ID, measure, agency, cost class, timeframe, funding head (maintenance/road-safety fund/black-spot programme/concession O&M), dependency.
17. **Agency-wise action table** (DRSC format): NHAI/PWD/ULB/Police/Electricity/Forest/Traffic — findings assigned, deadlines, status.
18. **Response report template** (IRC/GG119 style): each finding with Accept / Accept with modification / Reject (reason) / Deferred — to be completed by the road authority; exception/decision log.
19. Monitoring & re-audit plan: change-detection re-run schedule; KPIs (findings closed, crashes 12/36 months).

**Annexures**
A. Completed IRC:SP:88 existing-road checklist (present/absent/deficient/NA per item, with evidence refs).
B. Photo log (all frames used; GPS, time, direction).
C. Crash data (eDAR extract, black-spot computation).
D. Traffic/speed data & method (if any).
E. Sign & marking inventory (type, IRC:67 code, condition, retroreflectivity estimate/flag).
F. Barrier & roadside hazard inventory (type, length, terminals, condition).
G. Lighting inventory.
H. Median openings & access inventory.
I. Encroachment/wrong-side observation log (time-stamped counts).
J. Glossary & standards list; model/version & limitations statement; auditor CVs/certificates.

### 7.5 Machine-readable schema (minimum fields per finding)
```
finding_id, project_code, road_name, road_class, stage, direction, chainage_m, chainage_label,
lat, lon, h3_r10, segment_100m_id, category_code, checklist_item_id, observation_text,
evidence_frame_ids[], photo_ids[], detected_by (model|auditor), model_confidence,
likelihood, severity, risk_level, priority_label, timeframe, cost_class,
standard_refs[] ({code, clause}), recommendation_short, recommendation_long,
road_users_at_risk[], likely_crash_types[], crash_hist_500m {fatal, grievous, minor, period},
blackspot_flag, s198a_flag, night_check_required, verification_required[] (instrument),
responsible_agency, status (open|accepted|rejected|in_progress|closed), client_response,
auditor_id, auditor_cert_no, created_at, updated_at, run_id, supersedes_finding_id
```
Exports: PDF/A (signed, hashed), DOCX, XLSX (register + action plan + inventories as sheets), CSV, GeoJSON (points + 100 m segments + junction polygons), Shapefile, KML/KMZ (for police/DRSC), DXF (junction sketches, chainage-referenced point layer), JSON API.

### 7.6 Quality gates before a report can be "issued"
- Night pass present (or explicit waiver noted in limitations).
- Both directions covered for divided roads.
- GPS gaps < 2 % of length; chainage calibration against ≥2 reference points.
- Every Very High/High finding has ≥1 clear photo and an auditor acceptance.
- eDAR import (or statement that crash data were unavailable).
- Checklist completeness ≥95 % of applicable items answered.
- Auditor signature with certificate number and independence declaration.

---

## 8. Sources

Primary standards & government (several hosts could not be opened directly from this sandbox; cited as located via search):
- IRC:SP:88-2019 Manual on Road Safety Audit (First Revision) – https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.088.2019.pdf ; archive copy https://archive.org/details/gov.in.irc.sp.088.2019 ; summaries https://infralens.in/code/IRC-SP-88-2019 , https://www.roadvision.ai/blog/irc-code-sp-88-2019---manual-on-road-safety-audit
- IRC:SP:88-2010 – https://law.resource.org/pub/in/bis/irc/irc.gov.in.sp.088.2010.pdf
- PMGSY RSA training sessions (approach/methodology; team qualifications) – https://pmgsy.nic.in/sites/default/files/RSA%20(Session%2015%20_%2016).pdf , https://pmgsy.nic.in/sites/default/files/RSA%20(Session%2017%20_%2018).pdf , https://pmgsy.nic.in/sites/default/files/RSA%20(Session%2013%20_%2014).pdf
- TRIPP-IIT Delhi / BRO training decks (stages, checklists) – https://tripc.iitd.ac.in/assets/training_material/V_Kovvali-SafetyAuditApproach.pdf , https://tripc.iitd.ac.in/assets/training_material/Design_RSA_Case%20Studies_2024.pdf , https://tripc.iitd.ac.in/assets/training_material/DJ-Blackspot%20Auditing%20on%20Hill%20Roadsy.pdf
- MoRTH circulars: 09.11.2020 All-stage RSA through Independent Road Safety Experts – https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/604.46-09.11.2020%20All%20stage%20Road%20Safety%20Audit%20through%20Indendent%20Road%20Safety%20Expert.pdf ; 04.07.2018 design-stage RSA – https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/604.40-04.07.2018.pdf ; 20.09.2019 Road Safety Measures on NHs – https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/604.44-20.09.2019%20Road%20Safety%20Measures%20on%20Stretches%20of%20National%20Highways-%20Regarding.pdf ; 26.08.2019 black-spot proposal/sanction – https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/606.9-26.08.2019-%20Rectification%20of%20Accident%20Black%20Spot%20Preparation%20of%20proposal%20and%20sanction%20approval%20regarding%20on%2026th%20august%202019.-min.pdf ; 2017 Kolkata workshop on black spots – https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/604.38-08.07.2017-RS-PPT-Implementation%20of%20Road%20Safety%20Engineering%20Improvements%20held%20on%2008th%20July%202017%20at%20Kolkata.pdf ; 19.10.2015 & 20.04.2017 engineering measures – https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/604.29-19.10.2015-Road%20Safety%20Engineering%20Measures.pdf , https://morth.gov.in/sites/default/files/comprehensive_compendium_circular/604.37-20.04.2017-Essential%20approach%20and%20principles%20to%20be%20followed%20for%20Road%20Safety%20Engineering%20works.pdf ; mandatory IAHE training 21.11.2025 – https://morth.nic.in/sites/default/files/circulars_document/Mandatory%20trg%20at%20IAHE%20letter21112025-merged.pdf ; RSA course circular – https://morth.nic.in/sites/default/files/circulars_document/Road%20safety%20Audit-course-Final.pdf ; Highway Rating circular – https://morth.nic.in/sites/default/files/circulars_document/Highway%20Rating%20Circular.pdf ; NSV policy – https://morth.nic.in/sites/default/files/comprehensive_compendium_circular/202.9-13.11.2019-%20Policy%20Guidelines%20on%20surveying%20%28NSV%29.pdf ; SCCoRS direction letter – https://morth.nic.in/sites/default/files/circulars_document/Direction%20of%20SCCoRS%20All%20States%20Letter.pdf
- MoRTH Black Spot MIS – https://www.blackspot.morth.gov.in/ ; protocol summary – https://roadsafetynetwork.in/protocols-for-identification-and-rectification-of-road-accident-black-spots-on-national-highways/ ; Kerala calendar – http://roadsafety.kerala.gov.in/blackspot ; Maharashtra revised protocol – https://gr.maharashtra.gov.in/Site/Upload/Government%20Resolutions/English/201901101701131918...pdf ; Springer sliding-window paper – https://link.springer.com/chapter/10.1007/978-981-96-8118-1_21
- NHAI Road Safety Expert ToR – https://nhai.gov.in/nhai/sites/default/files/vacancy_files/ToR_1.pdf ; NHAI Safety Consultant RFP (Schedule L) – https://www.scribd.com/document/596686952/RFP3rdCallTRYRSC ; NHAI audits 16,500 km / mandatory DPR RSA – https://bsppd.business-standard.com/article/current-affairs/nhai-lays-down-procedures-for-extensive-audits-to-enhance-road-safety-123011400011_1.html ; PIB on mandatory RSA – https://pib.gov.in/PressReleasePage.aspx?PRID=1989104
- CSIR-CRRI RSA certification course notices (991 auditors; NHAI 2016 circular) – https://crridom.gov.in/sites/default/files/events/rsa-17th-nov-2-dec-2025.pdf , https://crridom.gov.in/sites/default/files/events/rsa-April-2023.pdf ; IIT Roorkee/Guwahati courses – https://news.careers360.com/iit-roorkee-organizes-fourth-road-safety-auditors-certification-course-civil-engineering , https://news.careers360.com/iit-guwahati-begins-15-day-road-safety-auditors-certificate-course/amp
- Oct 2025 certification programme / IRF proposal – https://ehs.distilinfo.com/2025/12/02/india-advances-road-safety/ , https://indiairf.com/?p=32881 , https://www.psuconnect.in/road-and-transport-news/irf-offers-support-to-morth-to-strengthen-indias-road-safety-audit-certification-framework ; IRF global credential – https://www.irf.global/global-credential/
- Motor Vehicles (Amendment) Act 2019 text – https://prsindia.org/files/bills_acts/bills_parliament/2019/Motor%20Vehicles%20(Amendment)%20Act,%202019.pdf ; S.198A – https://lawgist.in/motor-vehicles-act/198A , https://orjur.com/laws/Motor%20Vehicles%20Act/198A ; Rajya Sabha answer quoting 198A – https://rsdebate.nic.in/bitstream/123456789/721078/1/PQ_254_09082021_S220_p45_p52.pdf ; enforcement commentary – https://www.nationpathindia.com/national/road-safety-section-198a-agency-accountability-india
- Supreme Court: Rajaseekaran committee constitution – https://www.livelaw.in/amp/sc-constitutes-committee-road-safety-names-sitting-judge-chairman-effect-date-retirementread-judgment ; 30.11.2017 order – https://lawdadi.in/news/supreme-court-order-road-safety-measures-recommendation-implementation-s-rajaseekaran-v-uoi-wp-c-295-of-2012-order-30-11-2017.html , https://transport.Uk.Gov.In/files/SC%20order%20Road%20Safety/24.11.2017.pdf ; SCCoRS DRSC letters – https://transport.Uk.Gov.In/files/RoadSafetyDocs/18-07-2018.pdf , https://transport.Uk.Gov.In/files/RoadSafetyDocs/24-09-2018.pdf ; Sapre MP inspections – https://www.theweek.in/wire-updates/national/2025/07/30/bes38-mp-road-blackspots.html , https://www.freepressjournal.in/bhopal/madhya-pradesh-road-safety-panel-chief-inspects-bhopals-16-black-spots-calls-for-urgent-safety-reforms ; Jan 2023 framework direction – https://www.insightsonindia.com/2023/01/07/sc-directs-the-committee-to-build-a-framework-to-ensure-road-safety/ ; *In Re: Phalodi Accident* – https://www.verdictum.in/supreme-court/in-re-phalodi-accident-v-national-highways-authority-of-india-2026-insc-388-safety-commuter-article-21-morth-1612354 , https://www.livelaw.in/top-stories/supreme-court-in-re-phalodi-accident-suo-motu-interim-directions-safety-of-commuter-integral-facet-of-article-21-right-to-live-with-dignity-530836 , https://www.scconline.com/blog/post/2026/04/20/commuter-safety-fundamental-right-article-21-interim-directions-highway-safety-issued-sc/
- DRSC composition – https://dhenkanal.odisha.gov.in/sites/default/files/2023-11/2022091380.pdf , https://wbxpress.com/district-road-safety-committee-west-bengal/ , https://rsdebate.nic.in/bitstream/123456789/757472/1/PQ_267_19032025_U2169_p304_p305.pdf , https://www.parisar.org/what-we-do/road-safety/advocacy/state-government-forms-district-road-safety-committees-in-violation-of-supreme-court-directions
- iRAD/eDAR – https://coers.iitm.ac.in/irad/ , https://dccentral.delhi.gov.in/sites/default/files/dccentral/generic_multiple_files/irad_overview.pdf , https://roadsafety.hp.gov.in/storage/files/iRAD/iRAD/usermanual-iRAD.pdf , https://gisnic.tn.nic.in/irad/downloads/iRAD_MANNUAL_april_2024.pdf , https://roadsafety.hp.gov.in/storage/files/Extra%20Menu/iRAD%20-%20eDAR.pdf , https://vajiramandravi.com/current-affairs/govt-to-map-highway-black-spots-with-real-time-e-dar-data/ ; CoERS/DDHI – https://coers.iitm.ac.in/coers , https://www.dtnext.in/news/chennai/iit-ms-data-driven-initiative-aims-to-tackle-road-accidents-834439
- CAG 2026 chapter on RSAs – https://cag.gov.in/uploads/download_audit_report/2026/Chapter-II-06a87dc29ab55b1.53710159.pdf ; Maharashtra 1 % RSA circular – https://cdnbbsr.s3waas.gov.in/s35dec707028b05bcbd3a1db5640f842c5/uploads/2025/03/202503101167485657.pdf
- MoRTH Highway Rating – https://indianinfrastructure.com/2021/03/13/morth-has-formulated-a-rating-mechanism-for-national-highways/ , https://factly.in/review-here-is-all-about-the-national-highways-rating-mechanism , https://swarajyamag.com/news-brief/indias-national-highways-to-undergo-performance-assessment-covering-potholes-safety-and-toll-plazas

Example Indian RSA reports and programmes:
- NH-220 existing-road RSA (Odisha) – https://www.scribd.com/document/471695756/NH220-RSA2 ; NH-44 J&K design RSA table – https://www.scribd.com/document/433183364/Road-Safety-Audit ; NHAI inception report (Gumla bypass HAM) – https://www.scribd.com/document/569306756/Inception-Report ; WCTRS NH-202 construction-stage audit – https://wctrs-society.com/wp-content/uploads/abstracts/rio/general/3570.pdf
- Samruddhi Expressway VNIT audit (IRC:SP:88-2019 existing-road checklist) – https://www.roadsafetynetwork.in//wp-content/uploads/2023/10/Samruddhi-Expressway-Safety-Audit-VNIT-2023-1.pdf ; SaveLIFE press release – https://savelifefoundation.org/wp-content/uploads/2025/02/Samruddhi-Mahamarg-Press-Release.pdf
- SaveLIFE Zero Fatality Corridor – https://rwjms.rutgers.edu/sites/default/files/2026-04/jason_hua.zfc_rutgers_global_health_fair_poster_final.pdf , https://www.outlookindia.com/national/zero-fatality-corridor-crash-deaths-down-by-583-on-mumbai-pune-e-way-since-2016-says-report , https://www.weforum.org/stories/geographies-in-depth/puede-india-reducir-a-cero-las-muertes-en-una-carretera-peligrosa-este-grupo-lo-intenta-es , https://savelifefoundation.org/grounded-action-tactical-redesign/
- Bengaluru Traffic Police black spots & 2023 report – https://www.deccanherald.com/india/karnataka/bengaluru/64-accident-black-spots-in-bengaluru-here-is-the-full-list-of-stretches-identified-by-traffic-police-3891968 , https://www.thenewsminute.com/karnataka/bengalurus-black-spots-tnm-visits-the-citys-deadliest-roads-for-pedestrians ; BBMP Suraksha 75 / WRI – https://citizenmatters.in/suraksha-75-mission-2023-to-redesign-major-junctions-in-the-city-109983 , https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fbengaluru%2Fsuraksha-75-bengalurus-junction-makeover-stuck-between-plans-and-pavements-3837496
- Delhi 420 km AI audit plan – https://theprint.in/india/govt-to-launch-ai-based-traffic-safety-audit-for-over-420-km-of-south-delhi-roads/3045806/ ; Pune SaferBraIn audit – https://newlayout.trafficinfratech.com/saferbrain-a-european-union-project/2 ; NIUA urban RSA – https://smartnet.niua.org/sites/default/files/resources/urban_road_safety_audit_200614.pdf
- World Bank: mainstreaming RSAs (NHIIP) – https://blogs.worldbank.org/en/transport/mainstreaming-road-safety-audits-making-indian-roads-safer ; Delivering Road Safety in India – https://documents1.worldbank.org/curated/en/827641581916488024/pdf/Delivering-Road-Safety-in-India-Leadership-Priorities-and-Initiatives-to-2030.pdf ; ITF Karnataka safe-system case study – https://www.itf-oecd.org/sites/default/files/itf-safe-system-case-study-karnataka.pdf

International methods:
- Austroads AGRS06-09 (superseded; matrix) – https://austroads.gov.au/publications/road-safety/agrs06-09/media/AGRS06-09_Guide_to_Road_Safety_Part_6_Road_Safety_Audit.pdf ; AGRS06-19 – https://austroads.gov.au/__data/assets/pdf_file/0026/171728/AGRS06-19-Guide_to_Road_Safety_Part_6_Managing_Road_Safety_Audits.pdf ; AGRS06-22 prompt lists – https://www.road-safety-audit-wa.org/images/AGRS6-Prompt-Lists.pdf ; existing-road checklist – https://www.road-safety-audit-wa.org/images/Road-Safety-Inspection-Existing-Road-Checklist.pdf ; 2022 edition copy – https://safesystemsolutions.com.au/wp-content/uploads/2024/06/2022-AGRS-Part-6.pdf ; JACRS risk assessment – https://journalofroadsafety.org/article/32744-mastering-the-art-of-risk-assessment.pdf ; sample 2022-based audits – https://hdp-au-prod-app-ston-connect-files.s3.ap-southeast-2.amazonaws.com/7416/8057/4753/Road_Safety_Audit_p1CFZjaJGk6cR1c55r9zmA.pdf , https://hdp-au-prod-app-waverley-yoursay-files.s3.ap-southeast-2.amazonaws.com/4616/8014/3941/Appendix_7_-_Road_Safety_Audit.pdf ; Austroads motorcycle infrastructure – https://austroads.gov.au/publications/road-safety/ap-r515-16
- ADB CAREC RSE Manual 1 (RSA; matrix variant, existing-road stage) – https://www.adb.org/sites/default/files/publication/404421/carec-rse-manual-1-road-safety-audit.pdf , https://www.carecprogram.org/uploads/CAREC-Manual-1_RSA_English_FIN.pdf ; Manual 5 star ratings for RSA – https://www.adb.org/node/806631
- UK GG 119 – https://www.theihe.org/wp-content/uploads/2020/02/GG-119-revision-2-Road-safety-audit.pdf , https://www.nottinghamshire.gov.uk/media/5083526/1284-gg119.pdf , https://www.standardsforhighways.co.uk/tses/attachments/69517ebd-ed8d-4558-b101-c1e80611000a ; CIHT/SoRSA certificate of competency – https://www.ciht.org.uk/sorsa/join-sorsa/certificate-of-competency/ ; Solihull RSA policy (Appendix D template) – https://www.solihull.gov.uk/sites/default/files/migrated/ParkingTravelRoads_Road-Safety-Audit-Policy.pdf ; TII audit team qualifications – https://www.tiipublications.ie/library/GE-STY-01025-02.pdf
- PIARC RSI guideline – https://piarc.org/en/order-library/18265-en-Road%20safety%20inspection%20guidelines%20for%20safety%20checks%20of%20existing%20roads ; Catalogue of design safety problems – https://www.piarc.org/ressources/documents/2690,2009R07-NewRelease-E.pdf ; Road Safety Manual proactive identification & checklists – https://roadsafety.piarc.org/en/planning-design-operation/risk-issue-identification/proactive-identification , https://roadsafety.piarc.org/en/planning-design-operation/appendices/appx-104-checklists ; Austrian RSI handbook – https://www.bmimi.gv.at/dam/jcr:017ef810-a122-4bb7-b893-270cff68f77a/38_rsi_handbuchEN.pdf
- FHWA RSA Guidelines & Prompt List 6 (existing roads) – https://highways.dot.gov/safety/data-analysis-tools/rsa/fhwa-road-safety-audit-guidelines/80-road-safety-audit-prompt-lists , https://highways.dot.gov/safety/data-analysis-tools/rsa/fhwa-road-safety-audit-guidelines/post-construction-phase-prompt ; pedestrian RSA prompts – https://highways.dot.gov/safety/data-analysis-tools/rsa/pedestrian-road-safety-audits
- iRAP: Fact Sheet 7 bands – https://www.southnorfolkandbroadland.gov.uk/asset-library/imported-assets/cd-8.25-irap-factsheet-7.pdf ; Star Rating & Investment Plan Manual – https://austroads.gov.au/__data/assets/pdf_file/0033/836295/iRAP_Star_Rating_and_Investment_Plan_Manual_English.pdf ; AusRAP methodology – https://austroads.gov.au/safety-and-design/road-safety/ausrap/ausrap-road-safety-star-rating ; model 3.10 – https://etsc.eu/irap-launches-updated-star-rating-model-for-road-infrastructure-safety/ ; IndiaRAP/NHAI – https://irap.org/?p=41554 , https://irap.org/irap-and-aitd-renew-partnership-to-drive-indiarap-to-new-heights/ ; iRAP toolkit on infrastructure safety management – https://toolkit.irap.org/management/infrastructure-safety-management-tools/
- Comparative review of RSA guidelines – https://journalofroadsafety.org/article/84295-road-safety-audit-rsa-guidelines-of-selected-nations-a-comparative-review

Competitors & technology:
- RoadMetrics – https://frontiertech.niti.gov.in/story/ai-driven-road-management-enhancing-indias-infrastructure-with-roadmetrics/ , https://thebetterindia.com/311278/bengaluru-startup-roadmetrics-dipen-babariya-finds-fixes-potholes-using-ai-road-safety , https://yourstory.com/2020/11/raise-2020-ai-deep-tech-startup-roadmetrics , https://www.ciol.com/roadmetrics-worlds-first-startup-mapping-road-conditions-scale
- Intents Mobi – https://www.here.com/learn/blog/intents-mobi-navigation-app , https://thenextweb.com/neural/2020/12/26/how-this-startup-is-mapping-indias-potholes-using-just-your-phone/ ; RoadBounce – https://www.cbinsights.com/company/roadbounce
- RoadBotics/Michelin – https://technical.ly/startups/roadbotics-acquired-by-michelin , https://www.automotiveworld.com/news-releases/michelin-acquires-roadbotics-a-start-up-specialized-in-road-infrastructure-computer-vision/
- Vaisala RoadAI – https://www.applytosupply.digitalmarketplace.service.gov.uk/g-cloud/services/581776053828682 , https://xweather.com/roadai , https://www.vaisala.com/en/blog/2018-07/video-analysis-computer-vision-ultimate-format-traffic-sign-inventories , https://xweather.com/blog/article/northumberland-county-x-roadai
- Mobileye/Ordnance Survey – https://www.intc.com/news-events/press-releases/detail/74/ordnance-survey-and-mobileye-begin-trials-to-map , https://www.cnbc.com/2019/05/08/mobileye-to-map-road-data-in-collaboration-with-ordnance-survey.html
- iRASTE – https://inai.iiit.ac.in/iraste-nagpur.html , https://dst.gov.in/ai-make-roads-india-safer-drive , https://indiaai.gov.in/case-study/using-predictive-ai-to-reimagine-road-safety-in-india , https://crridom.gov.in/node/1179 , https://scroll.in/article/1076265/india-has-the-worlds-highest-number-of-traffic-deaths-could-ai-help-save-lives
- RASSI / JP Research India – https://saemobilus.sae.org/content/2013-26-0031 , https://indiairf.com/wp-content/uploads/2024/06/31May2024-JPRI_Crash-Investigation-2-1.pdf , https://toolkit.irap.org/case-studies/case-study-pune-expressway-road-accident-study-mumbai-india/
- State AI pilots – https://themachinemaker.com/news/iti-limited-to-roll-out-indias-first-ai-based-road-safety-project-in-uttar-pradesh/ , https://letsdatascience.com/news/ai-system-identifies-384-andhra-pradesh-highway-corridors-b69af013 , https://indianinfrastructure.com/2025/01/06/safer-roads-technology-solutions-to-reduce-accidents/
- Signs/sheeting standards – https://www.scribd.com/document/700190819/IRC-67-2022-traffic-sign , https://morth.nic.in/sites/default/files/Section%20800.docx , https://reflectives.averydennison.com/en/home/learn/learn-sheeting/6-specifications.html ; IRC catalogue 2026 – https://www.irc.nic.in/WriteReadData/LINKS/Updated%20Catalogue,%202026(1)ed1ad28e-67a2-4bfe-82c1-4c3b75fa9107.pdf
