"""IRC / MoRTH compliance rule engine.

Evaluates every rule in irc_rules.yaml against a RoadModel and returns (findings, compliance matrix).
Rules whose inputs are not available from the media (e.g. footpath width without segmentation/VLM) are
reported as *not_assessed* rather than silently passed - the coverage figure in the summary is honest.
"""
from __future__ import annotations

import logging
import math
from collections import defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

import yaml

from ..config import RULES_FILE
from ..geometry.road import irc_min_radius_table
from ..schemas import (Asset, AssetType, ComplianceItem, Evidence, Finding, Likelihood, Priority, RoadClass,
                       RoadModel, Segment, Severity)
from ..scoring.risk import risk_from

log = logging.getLogger(__name__)

CATEGORY_CODE = {
    "pavement": "PAV", "cross_section": "XS", "markings": "MRK", "pedestrian": "PED", "signs": "SGN",
    "traffic_calming": "TC", "intersection": "INT", "lighting": "LGT", "roadside": "RSH", "parking": "PRK",
    "encroachment": "ENC", "public_transport": "BUS", "work_zone": "WZ", "speed": "SPD", "cyclists": "NMT",
    "drainage": "DRN", "general": "GEN",
}
STATUTORY_SPEED = {  # MoRTH S.O.1522(E) 2018, M1 vehicles
    RoadClass.EXPRESSWAY: 120, RoadClass.NATIONAL_HIGHWAY: 100, RoadClass.STATE_HIGHWAY: 100,
    RoadClass.MAJOR_DISTRICT_ROAD: 80, RoadClass.OTHER_DISTRICT_ROAD: 70, RoadClass.VILLAGE_ROAD: 60,
    RoadClass.URBAN_ARTERIAL: 70, RoadClass.URBAN_SUB_ARTERIAL: 60, RoadClass.URBAN_COLLECTOR: 50, RoadClass.URBAN_LOCAL: 30,
}


CHECKLIST_FILE = RULES_FILE.parent / "irc_sp88_checklist.yaml"


def load_checklist(path=None) -> Dict[str, Any]:
    with open(path or CHECKLIST_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def evaluate_checklist(compliance: Sequence[ComplianceItem], path=None):
    """Roll the per-rule compliance matrix up to the 66 IRC:SP:88 Stage-5 checklist questions."""
    from ..schemas import ChecklistItem
    by_rule = {c.rule_id: c for c in compliance}
    out = []
    for sec in load_checklist(path)["sections"]:
        for it in sec["items"]:
            cs = [by_rule[r] for r in it.get("rules", []) if r in by_rule]
            nf = sum(c.n_findings for c in cs)
            statuses = {c.status for c in cs}
            if not cs:
                status = "manual"
            elif "non_compliant" in statuses:
                status = "deficient"
            elif "compliant" in statuses and statuses <= {"compliant", "not_applicable"}:
                status = "satisfactory"
            elif "compliant" in statuses:
                status = "partially_assessed"
            else:
                status = "not_assessed"
            if it.get("manual") and status in ("satisfactory", "not_assessed"):
                status = "partially_assessed" if status == "satisfactory" else "manual"
            detail = "; ".join(f"{c.rule_id}:{c.status}" + (f"({c.n_findings})" if c.n_findings else "") for c in cs)
            out.append(ChecklistItem(section=str(sec["id"]), section_title=sec["title"], n=int(it["n"]), question=it["q"],
                                     rules=list(it.get("rules", [])), manual=bool(it.get("manual", False)), status=status, n_findings=nf, detail=detail))
    return out


def load_rules(path=None) -> Dict[str, Any]:
    with open(path or RULES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _group(rc: RoadClass, groups: Dict[str, List[str]]) -> str:
    for g, members in groups.items():
        if rc.value in members:
            return g
    return "urban"


def _cmp(value, op: str, thr, tol: float = 0.0) -> bool:
    if op == "<":
        return value < thr - tol
    if op == ">" and tol:
        return value > thr + tol
    if op == "<=":
        return value <= thr
    if op == ">":
        return value > thr
    if op == ">=":
        return value >= thr
    if op == "==":
        return value == thr
    if op == "!=":
        return value != thr
    if op == "outside":
        lo, hi = thr
        return not (lo <= value <= hi)
    if op == "inside":
        lo, hi = thr
        return lo <= value <= hi
    if op == "in":
        return value in thr
    raise ValueError(op)


class RuleEngine:
    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        self.db = rules or load_rules()
        self.rules: List[Dict[str, Any]] = self.db["rules"]
        self.groups = self.db["meta"]["class_groups"]
        self._counter: Dict[str, int] = defaultdict(int)

    # ------------------------------------------------------------------ helpers
    def _threshold(self, rule: Dict, thr, rm: RoadModel):
        if isinstance(thr, dict):
            if rm.road_class.value in thr:
                return thr[rm.road_class.value]
            g = _group(rm.road_class, self.groups)
            if g in thr:
                return thr[g]
            if rm.terrain.value in thr:
                return thr[rm.terrain.value]
            return next(iter(thr.values()))
        if thr == "min_radius_for_design_speed":
            return irc_min_radius_table(rm.design_speed_kmph or 50)
        if thr == "sign_size_for_speed":
            v = rm.design_speed_kmph or 50
            return 0.6 if v <= 50 else 0.75 if v <= 65 else 0.9 if v <= 80 else 1.2
        if thr == "posted_or_statutory_plus_10":
            return (rm.posted_speed_kmph or STATUTORY_SPEED[rm.road_class]) + 10
        return thr

    def _applies(self, rule: Dict, rm: RoadModel) -> bool:
        at = rule.get("applies_to")
        return True if not at else rm.road_class.value in at

    def _severity(self, rule: Dict, asset: Optional[Asset] = None) -> Severity:
        sev = Severity(rule.get("severity", "medium"))
        sbs = rule.get("severity_by_size")
        if sbs and asset is not None and asset.size_m:
            for key, bands in sbs.items():
                val = asset.size_m[0] if key == "width_m" else asset.size_m[1]
                for lo, hi, s in bands:
                    if lo <= val < hi:
                        sev = Severity(s)
        return sev

    def _mk_finding(self, rule: Dict, rm: RoadModel, chainage: float, observed: str, asset: Optional[Asset] = None,
                    seg: Optional[Segment] = None, conf: float = 0.5, end: Optional[float] = None,
                    extra_tags: Sequence[str] = ()) -> Finding:
        sev = self._severity(rule, asset)
        lik = Likelihood(rule.get("likelihood", "occasional"))
        score, priority = risk_from(sev, lik)
        cat = rule["category"]
        code = CATEGORY_CODE.get(cat, "GEN")
        self._counter[code] += 1
        geo = asset.geo if asset else (seg.start_geo if seg else None)
        ev: List[Evidence] = []
        if asset and asset.best_frame_path:
            ev.append(Evidence(frame_index=asset.best_frame_index, frame_path=asset.best_frame_path, bbox=asset.bbox_in_best_frame,
                               note=f"{asset.asset.value} seen in {asset.n_observations} frame(s), conf {asset.confidence:.2f}"))
        elif seg and seg.frame_indices:
            fr = next((f for f in rm.frames if f.index == seg.frame_indices[len(seg.frame_indices) // 2]), None)
            if fr:
                ev.append(Evidence(frame_index=fr.index, frame_path=fr.path, note="representative frame of segment"))
        km = int(chainage // 1000); m = int(chainage % 1000)
        fid = f"CFI-RSA-{km:02d}+{m:03d}-{code}-{self._counter[code]:02d}"
        return Finding(
            finding_id=fid, rule_id=rule["id"], category=cat, title=rule["title"], description=rule["requirement"],
            standard_ref=rule["standard_ref"], requirement=rule["requirement"], observed=observed,
            chainage_m=float(chainage), chainage_end_m=end, geo=geo, side=asset.side if asset else None,
            severity=sev, likelihood=lik, risk_score=score, priority=priority,
            road_users_affected=list(rule.get("users", [])), recommendation=rule["recommendation"],
            responsible_agency=rule.get("agency", "Road owning agency"), confidence=float(conf), evidence=ev,
            tags=[rule.get("confidence", "medium") + "_standard_confidence", *extra_tags],
        )

    # ------------------------------------------------------------------ evaluation
    def evaluate(self, rm: RoadModel) -> Tuple[List[Finding], List[ComplianceItem]]:
        self._counter.clear()
        findings: List[Finding] = []
        compliance: List[ComplianceItem] = []
        assets_by = defaultdict(list)
        for a in rm.assets:
            assets_by[a.asset.value].append(a)
        for rule in self.rules:
            if not self._applies(rule, rm):
                compliance.append(ComplianceItem(rule_id=rule["id"], category=rule["category"], title=rule["title"],
                                                 standard_ref=rule["standard_ref"], status="not_applicable",
                                                 detail=f"not applicable to {rm.road_class.value}"))
                continue
            try:
                fs, status, detail = self._eval_rule(rule, rm, assets_by)
            except Exception as e:  # never let one rule kill the audit
                log.exception("rule %s failed", rule["id"])
                fs, status, detail = [], "not_assessed", f"engine error: {e}"
            findings.extend(fs)
            compliance.append(ComplianceItem(rule_id=rule["id"], category=rule["category"], title=rule["title"],
                                             standard_ref=rule["standard_ref"], status=status, detail=detail, n_findings=len(fs)))
        findings.sort(key=lambda f: (-f.risk_score, f.chainage_m))
        return findings, compliance

    def _eval_rule(self, rule, rm: RoadModel, assets_by) -> Tuple[List[Finding], str, str]:
        chk = rule["check"]
        t = chk["type"]
        fn = getattr(self, f"_chk_{t}", None)
        if fn is None:
            return [], "not_assessed", f"unknown check type {t}"
        return fn(rule, chk, rm, assets_by)

    def _can_detect(self, rm: RoadModel, *asset_names: str) -> bool:
        caps = rm.context.get("capabilities") or {}
        if not caps:
            return True   # no capability info -> assume assessable
        return any(caps.get(a, False) for a in asset_names)

    # ---- check implementations ------------------------------------------------
    def _chk_asset_conf(self, rule, chk, rm, assets_by):
        items = [a for a in assets_by.get(chk["asset"], []) if a.confidence >= chk.get("min_conf", 0.3)]
        if chk["asset"] == "pothole":   # footpath defects are reported under PED-011, carriageway potholes under PAV-*
            items = [a for a in items if a.attributes.get("where") != "footpath"]
        fs = []
        for a in items:
            size = f", size {a.size_m[0]:.2f} x {a.size_m[1]:.2f} m" if a.size_m else ""
            obs = f"{a.asset.value.replace('_', ' ')} detected at Ch. {a.chainage_m:.0f} m ({a.side}), confidence {a.confidence:.2f}{size}, seen in {a.attributes.get('n_frames', 1)} frame(s)"
            tags = ["low_confidence_detection"] if a.confidence < 0.5 else []
            fs.append(self._mk_finding(rule, rm, a.chainage_m, obs, asset=a, conf=a.confidence, extra_tags=tags))
        if not fs and not self._can_detect(rm, chk["asset"]):
            return fs, "not_assessed", f"no loaded detector / VLM pass can observe '{chk['asset']}'"
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)} instance(s)"

    def _chk_density(self, rule, chk, rm, assets_by):
        if rm.length_m < 200:
            return [], "not_assessed", "surveyed length < 200 m"
        n = len([a for a in assets_by.get(chk["asset"], []) if a.confidence >= chk.get("min_conf", 0.3) and a.attributes.get("where") != "footpath"])
        per_km = n / (rm.length_m / 1000.0)
        thr = chk["per_km_gt"]
        if per_km > thr:
            f = self._mk_finding(rule, rm, 0.0, f"{n} {chk['asset']}(s) over {rm.length_m:.0f} m = {per_km:.1f} per km (threshold {thr})", conf=0.7, end=rm.length_m)
            return [f], "non_compliant", f"{per_km:.1f}/km"
        return [], "compliant", f"{per_km:.1f}/km"

    def _chk_asset_attr(self, rule, chk, rm, assets_by):
        items = assets_by.get(chk["asset"], [])
        if chk["asset"] == "sign_unknown":
            items = [a for k, v in assets_by.items() if k.startswith("sign_") for a in v]
        items = [a for a in items if a.confidence >= chk.get("min_conf", 0.0)]
        if not items:
            return [], "not_assessed", f"no {chk['asset']} observed"
        thr = self._threshold(rule, chk["threshold"], rm)
        fs, assessed = [], 0
        for a in items:
            val = a.attributes.get(chk["attr"])
            if val is None:
                continue
            assessed += 1
            if _cmp(val, chk["op"], thr, float(chk.get("tolerance", 0.0))):
                obs = f"{chk['attr'].replace('_', ' ')} = {val} (required {chk['op']} {thr}) at Ch. {a.chainage_m:.0f} m"
                fs.append(self._mk_finding(rule, rm, a.chainage_m, obs, asset=a, conf=min(a.confidence, 0.8)))
        if assessed == 0:
            return [], "not_assessed", f"attribute {chk['attr']} not measurable from media"
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)}/{assessed} non-compliant"

    def _chk_asset_presence(self, rule, chk, rm, assets_by):
        if rm.length_m < chk.get("min_length_m", 0):
            return [], "not_assessed", f"surveyed length {rm.length_m:.0f} m < {chk.get('min_length_m')} m"
        if not self._can_detect(rm, chk["asset"], *chk.get("alt_assets", [])):
            return [], "not_assessed", f"no loaded detector / VLM pass can observe '{chk['asset']}'"
        n = len(assets_by.get(chk["asset"], []))
        for alt in chk.get("alt_assets", []):
            n += len([a for a in assets_by.get(alt, []) if a.attributes.get("text")])
        if n >= chk.get("min_count", 1):
            return [], "compliant", f"{n} found"
        f = self._mk_finding(rule, rm, 0.0, f"no {chk['asset'].replace('_', ' ')} detected over {rm.length_m:.0f} m", conf=0.55, end=rm.length_m)
        return [f], "non_compliant", "absent"

    def _chk_asset_requires(self, rule, chk, rm, assets_by):
        items = [a for a in assets_by.get(chk["asset"], []) if a.confidence >= chk.get("min_conf", 0.0)]
        if not items:
            return [], "not_assessed", f"no {chk['asset']} observed"
        if "requires_metric" in chk:
            k, v = next(iter(chk["requires_metric"].items()))
            vals = [s.metrics.get(k) for s in rm.segments if s.metrics.get(k) is not None]
            if not vals:
                return [], "not_assessed", f"{k} unavailable"
            if max(vals) < v:
                return [], "not_applicable", f"{k} < {v}"
        if "requires_speed_ge" in chk and (rm.posted_speed_kmph or rm.design_speed_kmph or 0) < chk["requires_speed_ge"]:
            return [], "not_applicable", "approach speed below threshold"
        req = chk["requires"]
        if not self._can_detect(rm, *req):
            return [], "not_assessed", f"no loaded detector / VLM pass can observe {' / '.join(req)}"
        pool = [a for r in req for a in assets_by.get(r, [])]
        fs = []
        for a in items:
            lo, hi = a.chainage_m - chk.get("upstream_m", 50), a.chainage_m + chk.get("downstream_m", 0)
            ok = any(lo <= b.chainage_m <= hi for b in pool)
            if not ok:
                obs = f"{a.asset.value.replace('_', ' ')} at Ch. {a.chainage_m:.0f} m without {' / '.join(r.replace('_', ' ') for r in req)} within {chk.get('upstream_m', 50)} m upstream"
                tags = ["needs_field_verification"]  # a sign may exist outside the camera's field of view
                fs.append(self._mk_finding(rule, rm, a.chainage_m, obs, asset=a, conf=min(0.75, a.confidence * 0.9), extra_tags=tags))
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)}/{len(items)} lacking"

    def _chk_asset_requires_metric(self, rule, chk, rm, assets_by):
        items = assets_by.get(chk["asset"], [])
        if not items:
            return [], "not_assessed", f"no {chk['asset']} observed"
        flag = chk.get("only_when_flag")
        fs, assessed = [], 0
        for a in items:
            seg = self._segment_at(rm, a.chainage_m)
            if seg is None or (flag and not seg.flags.get(flag)):
                continue
            val = seg.metrics.get(chk["metric"])
            if val is None:
                continue
            assessed += 1
            if not _cmp(val, chk["op"], chk["threshold"]):
                fs.append(self._mk_finding(rule, rm, a.chainage_m, f"{chk['metric']} = {val:.1f} at crossing (required {chk['op']} {chk['threshold']})", asset=a, seg=seg, conf=0.6))
        if assessed == 0:
            return [], "not_assessed", "condition not met (e.g. daytime footage)"
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)}/{assessed}"

    def _chk_segment_metric(self, rule, chk, rm, assets_by):
        thr = self._threshold(rule, chk["threshold"], rm)
        fs, assessed = [], 0
        for seg in rm.segments:
            val = seg.metrics.get(chk["metric"])
            if val is None:
                continue
            if "requires_metric" in chk:
                k, v = next(iter(chk["requires_metric"].items()))
                if (seg.metrics.get(k) or 0) < v:
                    continue
            if "requires_flag_false" in chk and seg.flags.get(chk["requires_flag_false"]):
                continue
            if "requires_count_zero" in chk and seg.counts.get(chk["requires_count_zero"], 0) > 0:
                continue
            assessed += 1
            if _cmp(val, chk["op"], thr, float(chk.get("tolerance", 0.0))):
                obs = f"{chk['metric'].replace('_', ' ')} = {val:.2f} in segment {seg.segment_id} (Ch. {seg.start_m:.0f}-{seg.end_m:.0f} m); limit {chk['op']} {thr}"
                fs.append(self._mk_finding(rule, rm, seg.start_m, obs, seg=seg, conf=0.55, end=seg.end_m))
        if assessed == 0:
            return [], "not_assessed", f"metric {chk['metric']} not available"
        fs = self._merge_adjacent(fs)
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)} segment group(s) of {assessed}"

    def _chk_segment_flag(self, rule, chk, rm, assets_by):
        fs, assessed = [], 0
        for seg in rm.segments:
            if seg.flags.get(chk["flag"]) != chk.get("equals", True):
                continue
            if "requires_metric_any" in chk:
                k, v = next(iter(chk["requires_metric_any"].items()))
                if (seg.metrics.get(k) or 0) < v:
                    continue
            assessed += 1
            bad = True
            obs_parts = [f"segment {seg.segment_id} (Ch. {seg.start_m:.0f}-{seg.end_m:.0f} m) flagged {chk['flag']}"]
            if "metric_lt" in chk:
                k, v = next(iter(chk["metric_lt"].items()))
                mv = seg.metrics.get(k)
                if mv is None:
                    assessed -= 1
                    continue
                bad = mv < v
                obs_parts.append(f"{k} = {mv:.2f} (< {v})")
            if "count_zero" in chk:
                bad = bad and all(seg.counts.get(c, 0) == 0 for c in chk["count_zero"])
                obs_parts.append("none of: " + ", ".join(chk["count_zero"]))
            if bad:
                fs.append(self._mk_finding(rule, rm, seg.start_m, "; ".join(obs_parts), seg=seg, conf=0.5, end=seg.end_m))
        if assessed == 0:
            return [], "not_assessed", f"no segment with {chk['flag']}"
        fs = self._merge_adjacent(fs)
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)} of {assessed}"

    def _chk_segment_requires_asset(self, rule, chk, rm, assets_by):
        thr = self._threshold(rule, chk["threshold"], rm)
        pool = [a for r in chk["requires"] for a in assets_by.get(r, [])]
        fs, assessed = [], 0
        for seg in rm.segments:
            val = seg.metrics.get(chk["metric"])
            if val is None:
                continue
            assessed += 1
            if _cmp(val, chk["op"], thr):
                w = chk.get("window_m", 150)
                if not any(seg.start_m - w <= b.chainage_m <= seg.end_m for b in pool):
                    fs.append(self._mk_finding(rule, rm, seg.start_m, f"curve radius ~{val:.0f} m (min {thr:.0f} m for {rm.design_speed_kmph:.0f} km/h) in {seg.segment_id} with no warning sign/chevron within {w} m", seg=seg, conf=0.5, end=seg.end_m, extra_tags=["needs_field_verification"]))
        if assessed == 0:
            return [], "not_assessed", "no GPS-derived curvature"
        fs = self._merge_adjacent(fs)
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)}"

    def _chk_spacing(self, rule, chk, rm, assets_by):
        if rm.length_m < chk.get("min_length_m", 400):
            return [], "not_assessed", "surveyed length too short"
        if not self._can_detect(rm, chk["asset"]):
            return [], "not_assessed", "asset class not observable"
        xs = sorted(a.chainage_m for a in assets_by.get(chk["asset"], []))
        pts = [0.0, *xs, rm.length_m]
        fs = []
        for a, b in zip(pts, pts[1:]):
            if b - a > chk["max_gap_m"]:
                fs.append(self._mk_finding(rule, rm, a, f"no {chk['asset'].replace('_', ' ')} between Ch. {a:.0f} m and Ch. {b:.0f} m ({b - a:.0f} m gap > {chk['max_gap_m']} m)", conf=0.5, end=b, extra_tags=["needs_field_verification"]))
        return fs, ("non_compliant" if fs else "compliant"), f"{len(fs)} gap(s)"

    # ---- utils
    @staticmethod
    def _segment_at(rm: RoadModel, ch: float) -> Optional[Segment]:
        for s in rm.segments:
            if s.start_m <= ch <= s.end_m:
                return s
        return rm.segments[-1] if rm.segments else None

    @staticmethod
    def _merge_adjacent(fs: List[Finding]) -> List[Finding]:
        if not fs:
            return fs
        fs.sort(key=lambda f: f.chainage_m)
        out = [fs[0]]
        for f in fs[1:]:
            last = out[-1]
            if last.chainage_end_m is not None and abs(f.chainage_m - last.chainage_end_m) < 1e-6:
                last.chainage_end_m = f.chainage_end_m
                last.observed += " | " + f.observed.split(";")[0]
                last.evidence.extend(f.evidence[:1])
            else:
                out.append(f)
        return out
