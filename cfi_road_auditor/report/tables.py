"""XLSX / CSV registers for engineers (findings register, compliance matrix, asset inventory, segments)."""
from __future__ import annotations

import csv

from ..schemas import AuditReport
from ..scoring.risk import PRIORITY_LABEL

F_COLS = ["finding_id", "rule_id", "category", "title", "chainage_m", "chainage_end_m", "lat", "lon", "side", "severity",
          "likelihood", "risk_score", "priority", "standard_ref", "requirement", "observed", "recommendation",
          "responsible_agency", "road_users_affected", "confidence", "tags", "evidence_frame", "client_response", "action_taken", "closure_date"]


def _row(f):
    return [f.finding_id, f.rule_id, f.category, f.title, round(f.chainage_m, 1), round(f.chainage_end_m, 1) if f.chainage_end_m else "",
            f.geo.lat if f.geo else "", f.geo.lon if f.geo else "", f.side or "", f.severity.value, f.likelihood.value, f.risk_score,
            PRIORITY_LABEL[f.priority], f.standard_ref, f.requirement, f.observed, f.recommendation, f.responsible_agency,
            ", ".join(f.road_users_affected), round(f.confidence, 2), ", ".join(f.tags),
            (f.evidence[0].crop_path or f.evidence[0].frame_path) if f.evidence else "", "", "", ""]


def write_csv(report: AuditReport, path: str) -> str:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(F_COLS)
        for f in report.findings:
            w.writerow(_row(f))
    return path


def write_xlsx(report: AuditReport, path: str) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active; ws.title = "Findings"
    ws.append(F_COLS)
    for f in report.findings:
        ws.append(_row(f))
    fills = {"critical": "F4B6B2", "high": "F9D3B4", "medium": "FBEBB5", "low": "CDE8CF", "info": "E0E0E0"}
    for r in range(2, ws.max_row + 1):
        sev = ws.cell(r, 10).value
        if sev in fills:
            ws.cell(r, 10).fill = PatternFill("solid", fgColor=fills[sev])
    ws2 = wb.create_sheet("Compliance")
    ws2.append(["rule_id", "category", "title", "standard_ref", "status", "detail", "n_findings"])
    for c in report.compliance:
        ws2.append([c.rule_id, c.category, c.title, c.standard_ref, c.status, c.detail, c.n_findings])
    ws3 = wb.create_sheet("Assets")
    ws3.append(["asset_id", "type", "chainage_m", "lat", "lon", "side", "confidence", "n_obs", "width_m", "length_m", "attributes"])
    for a in report.road_model.assets:
        ws3.append([a.asset_id, a.asset.value, round(a.chainage_m, 1), a.geo.lat if a.geo else "", a.geo.lon if a.geo else "", a.side,
                    round(a.confidence, 2), a.n_observations, round(a.size_m[0], 2) if a.size_m else "", round(a.size_m[1], 2) if a.size_m else "", str(a.attributes)])
    ws4 = wb.create_sheet("Segments")
    keys = sorted({k for s in report.road_model.segments for k in s.metrics})
    ws4.append(["segment_id", "start_m", "end_m", *keys, "assets"])
    for s in report.road_model.segments:
        ws4.append([s.segment_id, s.start_m, s.end_m, *[round(s.metrics[k], 3) if k in s.metrics else "" for k in keys], str(s.counts)])
    ws5 = wb.create_sheet("Summary")
    sm = report.summary
    for k, v in (("report_id", report.report_id), ("title", report.title), ("generated_at", report.generated_at), ("overall_score", sm.overall_score),
                 ("star_rating", sm.star_rating), ("n_findings", sm.n_findings), ("length_m", sm.length_m), ("coverage_pct", sm.coverage_pct)):
        ws5.append([k, v])
    for w in wb.worksheets:
        for c in w[1]:
            c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True)
        w.freeze_panes = "A2"
    wb.save(path)
    return path
