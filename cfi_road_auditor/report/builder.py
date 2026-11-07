"""Compile the AuditReport and write every output format (JSON, HTML, PDF, GeoJSON, KML, DXF, XLSX, CSV)."""
from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import __version__
from ..schemas import AuditReport, AuditSummary, ComplianceItem, Finding, Priority, RoadModel
from ..scoring.risk import PRIORITY_LABEL
from .annotate import annotate_finding

TEMPLATES = Path(__file__).parent / "templates"


def build_report(rm: RoadModel, findings: List[Finding], compliance: List[ComplianceItem], summary: AuditSummary,
                 title: str, methodology: Dict, limitations: List[str]) -> AuditReport:
    ts = datetime.now(timezone.utc)
    rid = "CFI-" + ts.strftime("%Y%m%d-%H%M%S")
    return AuditReport(report_id=rid, title=title, generated_at=ts.strftime("%Y-%m-%d %H:%M UTC"), tool_version=__version__,
                       road_model=rm, findings=findings, compliance=compliance, summary=summary, methodology=methodology,
                       limitations=limitations)


def write_all_outputs(report: AuditReport, out_dir: str, segment_len: float = 50.0, pdf: bool = True) -> Dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)
    ev_dir = os.path.join(out_dir, "evidence")
    for f in report.findings:
        p = annotate_finding(f, ev_dir)
        if p and f.evidence:
            f.evidence[0].crop_path = p
    outputs: Dict[str, str] = {}
    # JSON (full machine-readable)
    jp = os.path.join(out_dir, "audit_report.json")
    with open(jp, "w", encoding="utf-8") as fh:
        fh.write(report.model_dump_json(indent=2, exclude={"road_model": {"frames"}}))
    outputs["json"] = jp
    # HTML
    hp = os.path.join(out_dir, "audit_report.html")
    write_html(report, hp, segment_len)
    outputs["html"] = hp
    # GeoJSON / KML
    if any(f.geo for f in report.findings) or report.road_model.track:
        from .geo import write_geojson, write_kml
        outputs["geojson"] = write_geojson(report, os.path.join(out_dir, "audit_findings.geojson"))
        outputs["kml"] = write_kml(report, os.path.join(out_dir, "audit_findings.kml"))
    # DXF (CAD strip plan)
    try:
        from .dxf import write_dxf
        outputs["dxf"] = write_dxf(report, os.path.join(out_dir, "audit_strip_plan.dxf"))
    except Exception as e:  # pragma: no cover
        outputs["dxf_error"] = str(e)
    # XLSX / CSV registers
    try:
        from .tables import write_xlsx, write_csv
        outputs["xlsx"] = write_xlsx(report, os.path.join(out_dir, "audit_register.xlsx"))
        outputs["csv"] = write_csv(report, os.path.join(out_dir, "audit_findings.csv"))
    except Exception as e:  # pragma: no cover
        outputs["xlsx_error"] = str(e)
    # PDF
    if pdf:
        try:
            from .pdf import write_pdf
            outputs["pdf"] = write_pdf(report, os.path.join(out_dir, "audit_report.pdf"))
        except Exception as e:  # pragma: no cover
            outputs["pdf_error"] = str(e)
    report.outputs = outputs
    with open(jp, "w", encoding="utf-8") as fh:
        fh.write(report.model_dump_json(indent=2, exclude={"road_model": {"frames"}}))
    return outputs


def _action_plan(findings: List[Finding]):
    plan = defaultdict(list)
    for f in findings:
        plan[f.priority].append(f"{f.finding_id} {f.title} (Ch. {f.chainage_m:.0f} m)")
    order = [Priority.IMMEDIATE, Priority.SHORT_TERM, Priority.MEDIUM_TERM, Priority.LONG_TERM, Priority.MONITOR]
    return [(p, plan[p]) for p in order if plan[p]]


def write_html(report: AuditReport, path: str, segment_len: float) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=select_autoescape(["html"]))
    tpl = env.get_template("report.html")
    base = os.path.dirname(os.path.abspath(path))
    def rel(p):
        try:
            return os.path.relpath(p, base)
        except Exception:
            return p
    html = tpl.render(r=report, s=report.summary, rm=report.road_model, f=report.findings, m=report.methodology,
                      plabel=PRIORITY_LABEL, plan=_action_plan(report.findings), rel=rel, seglen=int(segment_len))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path
