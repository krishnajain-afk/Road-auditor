"""GeoJSON / KML exports for GIS (QGIS, ArcGIS, Google Earth, MoRTH black-spot MIS uploads)."""
from __future__ import annotations

import json
from xml.sax.saxutils import escape

from ..schemas import AuditReport


def write_geojson(report: AuditReport, path: str) -> str:
    feats = []
    rm = report.road_model
    if rm.track:
        feats.append({"type": "Feature", "properties": {"kind": "survey_track", "length_m": rm.length_m},
                      "geometry": {"type": "LineString", "coordinates": [[p.lon, p.lat] for p in rm.track]}})
    for f in report.findings:
        if not f.geo:
            continue
        feats.append({"type": "Feature", "properties": {
            "kind": "finding", "id": f.finding_id, "rule": f.rule_id, "title": f.title, "category": f.category,
            "severity": f.severity.value, "risk": f.risk_score, "priority": f.priority.value, "chainage_m": round(f.chainage_m, 1),
            "standard": f.standard_ref, "observed": f.observed, "recommendation": f.recommendation, "agency": f.responsible_agency,
            "confidence": round(f.confidence, 2)}, "geometry": {"type": "Point", "coordinates": [f.geo.lon, f.geo.lat]}})
    for a in rm.assets:
        if a.geo:
            feats.append({"type": "Feature", "properties": {"kind": "asset", "id": a.asset_id, "type": a.asset.value,
                          "chainage_m": round(a.chainage_m, 1), "confidence": round(a.confidence, 2), "side": a.side, **{k: v for k, v in a.attributes.items() if isinstance(v, (int, float, str, bool))}},
                          "geometry": {"type": "Point", "coordinates": [a.geo.lon, a.geo.lat]}})
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": feats}, fh, indent=1)
    return path


_COL = {"critical": "ff1e26b3", "high": "ff0f48d9", "medium": "ff0081b5", "low": "ff327d2f", "info": "ff8b7d60"}


def write_kml(report: AuditReport, path: str) -> str:
    rm = report.road_model
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
             f"<name>{escape(report.title)}</name>"]
    for k, c in _COL.items():
        parts.append(f'<Style id="{k}"><IconStyle><color>{c}</color><scale>1.1</scale></IconStyle></Style>')
    if rm.track:
        coords = " ".join(f"{p.lon},{p.lat},0" for p in rm.track)
        parts.append(f"<Placemark><name>Survey track</name><Style><LineStyle><color>ff00a5ff</color><width>4</width></LineStyle></Style><LineString><coordinates>{coords}</coordinates></LineString></Placemark>")
    for f in report.findings:
        if f.geo:
            desc = escape(f"{f.standard_ref}\nObserved: {f.observed}\nRecommendation: {f.recommendation}\nRisk {f.risk_score} - {f.priority.value}")
            parts.append(f'<Placemark><name>{escape(f.finding_id)} {escape(f.title)}</name><styleUrl>#{f.severity.value}</styleUrl><description>{desc}</description><Point><coordinates>{f.geo.lon},{f.geo.lat},0</coordinates></Point></Placemark>')
    parts.append("</Document></kml>")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    return path
