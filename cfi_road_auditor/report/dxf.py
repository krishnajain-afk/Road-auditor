"""AutoCAD-compatible DXF strip plan (ezdxf, R2010).

Layers: CFI_CENTRELINE (survey centreline in local metres, or straight chainage axis when no GPS),
CFI_EDGES (carriageway edges from measured widths), CFI_ASSETS_<TYPE> (point symbols + text), CFI_FINDINGS_<SEV>
(circles + leaders), CFI_CHAINAGE (ticks every 50 m), CFI_SEGMENTS (segment boxes with lane width text).
Units: metres; INSUNITS=6. Coordinates: local ENU from first track point, so the drawing can be georeferenced in
AutoCAD Map/Civil 3D via the inserted lat/lon origin note.
"""
from __future__ import annotations

import math
from typing import List, Tuple

import ezdxf
import numpy as np

from ..geometry.road import project_track
from ..schemas import AuditReport

_SEV_COLOR = {"critical": 1, "high": 30, "medium": 2, "low": 3, "info": 8}


def _axis(report: AuditReport) -> Tuple[np.ndarray, np.ndarray]:
    rm = report.road_model
    if len(rm.track) >= 2:
        xy = project_track(rm.track)
        s = np.r_[0, np.cumsum(np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1])))]
        return xy, s
    L = max(rm.length_m, 100.0)
    xy = np.array([[0.0, 0.0], [L, 0.0]])
    return xy, np.array([0.0, L])


def _at(xy, s, ch, offset=0.0):
    ch = float(np.clip(ch, s[0], s[-1]))
    x = np.interp(ch, s, xy[:, 0]); y = np.interp(ch, s, xy[:, 1])
    i = max(1, int(np.searchsorted(s, ch)))
    dx, dy = xy[min(i, len(xy) - 1)] - xy[i - 1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n, dx / n   # left normal
    return (x + nx * offset, y + ny * offset)


def write_dxf(report: AuditReport, path: str) -> str:
    rm = report.road_model
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 6
    msp = doc.modelspace()
    xy, s = _axis(report)
    for name, color in (("CFI_CENTRELINE", 7), ("CFI_EDGES", 8), ("CFI_CHAINAGE", 9), ("CFI_SEGMENTS", 4), ("CFI_NOTES", 7)):
        doc.layers.add(name, color=color)
    msp.add_lwpolyline([tuple(p) for p in xy], dxfattribs={"layer": "CFI_CENTRELINE"})
    # edges from carriageway width per segment
    left, right = [], []
    for seg in rm.segments:
        w = seg.metrics.get("carriageway_width_m") or (rm.context.get("default_carriageway_m") or 7.0)
        for ch in (seg.start_m, seg.end_m):
            left.append(_at(xy, s, ch, w / 2)); right.append(_at(xy, s, ch, -w / 2))
        lw = seg.metrics.get("lane_width_m")
        txt = f"{seg.segment_id}  CW {w:.1f} m" + (f"  lane {lw:.2f} m" if lw else "")
        p = _at(xy, s, (seg.start_m + seg.end_m) / 2, w / 2 + 3)
        msp.add_text(txt, dxfattribs={"layer": "CFI_SEGMENTS", "height": 1.2}).set_placement(p)
    if left:
        msp.add_lwpolyline(left, dxfattribs={"layer": "CFI_EDGES"})
        msp.add_lwpolyline(right, dxfattribs={"layer": "CFI_EDGES"})
    # chainage ticks
    for ch in np.arange(0, s[-1] + 1e-6, 50.0):
        a, b = _at(xy, s, ch, -2.0), _at(xy, s, ch, 2.0)
        msp.add_line(a, b, dxfattribs={"layer": "CFI_CHAINAGE"})
        msp.add_text(f"{int(ch // 1000)}+{int(ch % 1000):03d}", dxfattribs={"layer": "CFI_CHAINAGE", "height": 1.0}).set_placement(_at(xy, s, ch, -4.5))
    # assets
    for a in rm.assets:
        layer = f"CFI_ASSETS_{a.asset.value.upper()}"
        if layer not in doc.layers:
            doc.layers.add(layer, color=5)
        off = {"left": 4.0, "right": -4.0}.get(a.side or "centre", 0.0)
        p = _at(xy, s, a.chainage_m, off)
        msp.add_circle(p, 0.6, dxfattribs={"layer": layer})
        msp.add_text(f"{a.asset_id} {a.asset.value}", dxfattribs={"layer": layer, "height": 0.8}).set_placement((p[0] + 0.8, p[1] + 0.8))
    # findings
    for f in report.findings:
        layer = f"CFI_FINDINGS_{f.severity.value.upper()}"
        if layer not in doc.layers:
            doc.layers.add(layer, color=_SEV_COLOR[f.severity.value])
        off = {"left": 7.0, "right": -7.0}.get(f.side or "centre", 7.0)
        p0 = _at(xy, s, f.chainage_m, 0.0); p = _at(xy, s, f.chainage_m, off)
        msp.add_circle(p0, 1.0, dxfattribs={"layer": layer})
        msp.add_line(p0, p, dxfattribs={"layer": layer})
        msp.add_text(f"{f.finding_id}: {f.title}", dxfattribs={"layer": layer, "height": 1.0}).set_placement((p[0] + 1, p[1]))
        if f.chainage_end_m:
            p1 = _at(xy, s, f.chainage_end_m, 0.0)
            msp.add_lwpolyline([_at(xy, s, c, 0.0) for c in np.linspace(f.chainage_m, f.chainage_end_m, 10)], dxfattribs={"layer": layer, "const_width": 0.5})
    # notes
    origin = f"Origin lat/lon: {rm.track[0].lat:.6f}, {rm.track[0].lon:.6f} (local ENU metres)" if rm.track else "No GPS: X axis = chainage (m)"
    msp.add_text(f"{report.title} - {report.report_id} - CFI Road Auditor v{report.tool_version} - {origin}",
                 dxfattribs={"layer": "CFI_NOTES", "height": 1.5}).set_placement((xy[0][0], xy[0][1] - 15))
    doc.saveas(path)
    return path
