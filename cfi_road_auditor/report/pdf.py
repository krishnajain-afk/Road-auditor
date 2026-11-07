"""PDF report (reportlab platypus) mirroring the HTML structure - printable for DRSC / PWD files."""
from __future__ import annotations

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from ..schemas import AuditReport
from ..scoring.risk import PRIORITY_LABEL

_SEV = {"critical": colors.HexColor("#b3261e"), "high": colors.HexColor("#d9480f"), "medium": colors.HexColor("#b58100"),
        "low": colors.HexColor("#2f7d32"), "info": colors.HexColor("#607d8b")}


def _p(txt, st):
    return Paragraph(str(txt).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), st)


def write_pdf(report: AuditReport, path: str) -> str:
    ss = getSampleStyleSheet()
    small = ParagraphStyle("small", parent=ss["BodyText"], fontSize=7.5, leading=9.5, alignment=TA_LEFT)
    body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9, leading=12)
    h1, h2, h3 = ss["Title"], ss["Heading2"], ss["Heading3"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=14 * mm, bottomMargin=14 * mm,
                            title=report.title, author="CFI Road Auditor")
    rm, s = report.road_model, report.summary
    el = [_p(report.title, h1), _p(f"Report {report.report_id} | {report.generated_at} | CFI Road Auditor v{report.tool_version} | Stage-5 RSA per IRC:SP:88-2019", small), Spacer(1, 6)]
    el.append(_p("1. Executive summary", h2))
    kp = [["Safety score", f"{s.overall_score}/100"], ["Indicative star band", "*" * s.star_rating + f" ({s.star_rating}/5, not an official iRAP rating)"],
          ["Findings", f"{s.n_findings} (critical {s.n_by_severity.get('critical', 0)}, high {s.n_by_severity.get('high', 0)}, medium {s.n_by_severity.get('medium', 0)}, low {s.n_by_severity.get('low', 0)})"],
          ["Surveyed length", f"{s.length_m:.0f} m"], ["Road class / design speed", f"{rm.road_class.value} / {rm.design_speed_kmph} km/h"],
          ["Checklist coverage", f"{s.coverage_pct}% ({s.assessed_rules} assessed, {s.not_assessed_rules} not assessable from media)"]]
    t = Table([[_p(a, body), _p(b, body)] for a, b in kp], colWidths=[55 * mm, 120 * mm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f5f8"))]))
    el += [t, Spacer(1, 6), _p("Top risks", h3)]
    for x in s.top_risks:
        el.append(_p("- " + x, body))
    el += [_p("2. Methodology and limitations", h2)]
    for k, v in report.methodology.items():
        el.append(_p(f"<b>{k}</b>: {v if not isinstance(v, list) else '; '.join(map(str, v))}", body))
    for l in report.limitations:
        el.append(_p("- " + l, small))
    el += [PageBreak(), _p(f"3. Findings register ({len(report.findings)})", h2)]
    rows = [[_p(x, small) for x in ("ID", "Ch. (m)", "Finding / observed", "Standard", "Sev.", "Risk", "Priority")]]
    for f in report.findings:
        rows.append([_p(f.finding_id, small), _p(f"{f.chainage_m:.0f}" + (f"-{f.chainage_end_m:.0f}" if f.chainage_end_m else ""), small),
                     _p(f"<b>{f.title}</b><br/>{f.observed}", small), _p(f.standard_ref, small), _p(f.severity.value, small), _p(f.risk_score, small),
                     _p(PRIORITY_LABEL[f.priority].split(" - ")[0], small)])
    t = Table(rows, colWidths=[27 * mm, 14 * mm, 62 * mm, 40 * mm, 13 * mm, 9 * mm, 20 * mm], repeatRows=1)
    st = [("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9edf2")), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for i, f in enumerate(report.findings, 1):
        st.append(("TEXTCOLOR", (4, i), (4, i), _SEV[f.severity.value]))
    t.setStyle(TableStyle(st)); el.append(t)
    el += [PageBreak(), _p("4. Finding sheets", h2)]
    for f in report.findings:
        el.append(_p(f"<b>{f.finding_id} - {f.title}</b> [{f.severity.value.upper()}, risk {f.risk_score}] Ch. {f.chainage_m:.0f} m" + (f" ({f.geo.lat:.6f}, {f.geo.lon:.6f})" if f.geo else ""), body))
        rows = [[_p("Standard", small), _p(f.standard_ref, small)], [_p("Requirement", small), _p(f.requirement, small)], [_p("Observed", small), _p(f.observed, small)],
                [_p("Recommendation", small), _p(f.recommendation, small)], [_p("Agency / priority", small), _p(f"{f.responsible_agency} / {PRIORITY_LABEL[f.priority]}", small)],
                [_p("Confidence / tags", small), _p(f"{f.confidence:.0%} / {', '.join(f.tags)}", small)]]
        t = Table(rows, colWidths=[32 * mm, 148 * mm]); t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        el.append(t)
        if f.evidence and f.evidence[0].crop_path and os.path.exists(f.evidence[0].crop_path):
            try:
                el.append(Image(f.evidence[0].crop_path, width=120 * mm, height=68 * mm, kind="proportional"))
            except Exception:
                pass
        el.append(Spacer(1, 8))
    el += [PageBreak(), _p("5. Compliance matrix", h2)]
    rows = [[_p(x, small) for x in ("Rule", "Check", "Standard", "Status", "Detail")]]
    for c in report.compliance:
        rows.append([_p(c.rule_id, small), _p(c.title, small), _p(c.standard_ref, small), _p(c.status, small), _p(c.detail, small)])
    t = Table(rows, colWidths=[16 * mm, 55 * mm, 60 * mm, 20 * mm, 34 * mm], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9edf2")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    el.append(t)
    el += [Spacer(1, 10), _p("This automated audit supports and does not replace a certified Road Safety Auditor (IRC:SP:88-2019). Items tagged needs_field_verification must be confirmed on site.", small)]
    doc.build(el)
    return path
