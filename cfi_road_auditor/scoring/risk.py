"""Risk rating per IRC:SP:88-2019 (which adopts the Austroads 4x4 likelihood x consequence matrix).

  Likelihood: Frequent (>= once/week) | Probable (>= once/year) | Occasional (5-10 yrs) | Improbable (> 10 yrs)
  Consequence: Catastrophic (fatal) | Serious (hospitalisation) | Minor | Limited (property damage)
  Cell -> Intolerable / High / Medium / Low
  Priority (IRC:SP:88): Essential (correct at any cost) / Highly Desirable (even if high cost) / Desirable
  (if moderate cost) / Optional (if low cost).

We map our Severity enum onto consequence: critical->Catastrophic, high->Serious, medium->Minor, low/info->Limited.
Also produces an iRAP-like 1-5 star band from a risk density index per 100 m (star bands are indicative only -
a true iRAP rating requires the full 50+ attribute coding and the iRAP model).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List, Sequence, Tuple

from ..schemas import AuditSummary, ComplianceItem, Finding, Likelihood, Priority, RoadModel, Severity

_SEV_IDX = {Severity.CRITICAL: 0, Severity.HIGH: 1, Severity.MEDIUM: 2, Severity.LOW: 3, Severity.INFO: 3}
_LIK_IDX = {Likelihood.FREQUENT: 0, Likelihood.PROBABLE: 1, Likelihood.OCCASIONAL: 2, Likelihood.IMPROBABLE: 3}
# rows: consequence (Catastrophic, Serious, Minor, Limited); cols: likelihood (Frequent, Probable, Occasional, Improbable)
RISK_MATRIX = [
    ["Intolerable", "Intolerable", "High", "Medium"],
    ["Intolerable", "High", "Medium", "Low"],
    ["High", "Medium", "Low", "Low"],
    ["Medium", "Low", "Low", "Low"],
]
_SCORE = {"Intolerable": 16, "High": 10, "Medium": 5, "Low": 2}
_PRIORITY = {"Intolerable": Priority.IMMEDIATE, "High": Priority.SHORT_TERM, "Medium": Priority.MEDIUM_TERM, "Low": Priority.LONG_TERM}
PRIORITY_LABEL = {
    Priority.IMMEDIATE: "Essential (correct at any cost) - within 30 days",
    Priority.SHORT_TERM: "Highly Desirable (even if high cost) - 1-6 months",
    Priority.MEDIUM_TERM: "Desirable (if moderate cost) - 6-18 months",
    Priority.LONG_TERM: "Optional (if low cost) - next maintenance cycle",
    Priority.MONITOR: "Monitor",
}
USER_GROUPS = {
    "vehicle_occupants": {"car occupants", "all", "heavy vehicles", "bus passengers"},
    "motorcyclists": {"motorcyclists", "all"},
    "pedestrians": {"pedestrians", "children", "persons with disabilities", "all"},
    "bicyclists": {"cyclists", "all"},
}


def risk_from(sev: Severity, lik: Likelihood) -> Tuple[int, Priority]:
    cell = RISK_MATRIX[_SEV_IDX[sev]][_LIK_IDX[lik]]
    if sev == Severity.INFO:
        return 1, Priority.MONITOR
    return _SCORE[cell], _PRIORITY[cell]


def risk_label(score: int) -> str:
    for k, v in _SCORE.items():
        if score >= v:
            return k
    return "Info"


def _stars_from_density(risk_per_100m: float) -> int:
    # indicative bands (not iRAP): calibrated so a road with one Intolerable finding per 100 m is 1-star
    if risk_per_100m < 1.0:
        return 5
    if risk_per_100m < 3.0:
        return 4
    if risk_per_100m < 7.0:
        return 3
    if risk_per_100m < 14.0:
        return 2
    return 1


def summarise(rm: RoadModel, findings: Sequence[Finding], compliance: Sequence[ComplianceItem]) -> AuditSummary:
    n_sev = Counter(f.severity.value for f in findings)
    n_cat = Counter(f.category for f in findings)
    length = max(rm.length_m, 30.0 if len(rm.frames) <= 1 else 100.0)   # single photo covers ~30 m of road
    total_risk = sum(f.risk_score for f in findings)
    per100 = total_risk / (length / 100.0)
    # score: 100 - penalty, with diminishing returns
    score = max(0.0, 100.0 * (1.0 / (1.0 + per100 / 8.0)))
    by_user: Dict[str, int] = {}
    for g, names in USER_GROUPS.items():
        r = sum(f.risk_score for f in findings if set(f.road_users_affected) & names)
        by_user[g] = _stars_from_density(r / (length / 100.0))
    assessed = [c for c in compliance if c.status in ("compliant", "non_compliant")]
    na = [c for c in compliance if c.status == "not_assessed"]
    applicable = [c for c in compliance if c.status != "not_applicable"]
    top = [f"{f.finding_id}: {f.title} @ Ch. {f.chainage_m:.0f} m" for f in sorted(findings, key=lambda f: -f.risk_score)[:5]]
    return AuditSummary(
        overall_score=round(score, 1), star_rating=_stars_from_density(per100), star_rating_by_user=by_user,
        n_findings=len(findings), n_by_severity=dict(n_sev), n_by_category=dict(n_cat), top_risks=top, length_m=rm.length_m,
        assessed_rules=len(assessed), compliant_rules=len([c for c in assessed if c.status == "compliant"]),
        not_assessed_rules=len(na), coverage_pct=round(100.0 * len(assessed) / max(1, len(applicable)), 1),
    )
