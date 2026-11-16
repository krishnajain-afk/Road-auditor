"""Corridor summary: merge several audit_report.json files (e.g. consecutive walks / drives of one corridor) into one
authority-facing summary (Markdown + JSON): findings by rule and severity, per-video table, agency-wise action list.

Usage: python -m cfi_road_auditor.corridor --out outputs/batch1/corridor_summary outputs/batch1/*/audit_report.json
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from .scoring.risk import PRIORITY_LABEL
from .schemas import Priority


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cfi-corridor")
    ap.add_argument("reports", nargs="+")
    ap.add_argument("--out", default="outputs/corridor_summary")
    ap.add_argument("--title", default="Corridor summary")
    a = ap.parse_args(argv)
    reps = []
    for p in a.reports:
        with open(p, encoding="utf-8") as f:
            reps.append((p, json.load(f)))
    by_rule = Counter(); by_sev = Counter(); by_agency = defaultdict(list); rows = []; total_len = 0.0
    rule_meta = {}
    for p, r in reps:
        s = r["summary"]; total_len += s["length_m"]
        rows.append((Path(p).parent.name, s["length_m"], s["overall_score"], s["n_findings"], s["n_by_severity"], s["coverage_pct"], s.get("checklist_counts", {})))
        for f in r["findings"]:
            by_rule[f["rule_id"]] += 1; by_sev[f["severity"]] += 1
            rule_meta.setdefault(f["rule_id"], (f["title"], f["standard_ref"], f["recommendation"], f["severity"], f["priority"]))
            by_agency[f["responsible_agency"]].append(f"{Path(p).parent.name}: {f['finding_id']} {f['title']} (Ch. {f['chainage_m']:.0f} m)")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    L = [f"# {a.title}", "", f"{len(reps)} survey file(s), {total_len:.0f} m surveyed, {sum(by_rule.values())} findings "
         f"(critical {by_sev.get('critical', 0)}, high {by_sev.get('high', 0)}, medium {by_sev.get('medium', 0)}, low {by_sev.get('low', 0)}).", "",
         "## Per survey", "", "| Survey | Length | Score | Findings | C / H / M / L | Rule coverage | Checklist deficient / satisfactory / manual |", "|---|---|---|---|---|---|---|"]
    for name, ln, sc, nf, sev, cov, ck in rows:
        L.append(f"| {name} | {ln:.0f} m | {sc} | {nf} | {sev.get('critical', 0)} / {sev.get('high', 0)} / {sev.get('medium', 0)} / {sev.get('low', 0)} | {cov}% | {ck.get('deficient', 0)} / {ck.get('satisfactory', 0)} / {ck.get('manual', 0)} |")
    L += ["", "## Systemic deficiencies (by rule, across all surveys)", "", "| Rule | Deficiency | Count | Severity | Standard | Recommendation |", "|---|---|---|---|---|---|"]
    for rid, n in by_rule.most_common():
        t, ref, rec, sev, pri = rule_meta[rid]
        L.append(f"| {rid} | {t} | {n} | {sev} | {ref} | {rec} |")
    L += ["", "## Action list by agency", ""]
    for ag, items in sorted(by_agency.items(), key=lambda kv: -len(kv[1])):
        L.append(f"### {ag} ({len(items)})")
        L += [f"- {i}" for i in items[:40]]
        if len(items) > 40:
            L.append(f"- ... and {len(items) - 40} more (see the individual registers)")
        L.append("")
    L += ["## Priority key", ""] + [f"- {p.value}: {PRIORITY_LABEL[p]}" for p in Priority]
    (out / "corridor_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (out / "corridor_summary.json").write_text(json.dumps({"surveys": [dict(zip(("name", "length_m", "score", "findings", "by_severity", "coverage_pct", "checklist"), r)) for r in rows],
                                                            "by_rule": by_rule, "by_severity": by_sev, "by_agency": {k: len(v) for k, v in by_agency.items()}}, indent=1))
    print("\n".join(L[:30]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
