"""FastAPI service: upload a video/photo (+ optional GPS track) -> background audit job -> downloadable reports.

Run:  uvicorn cfi_road_auditor.api.app:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import json
import os
import shutil
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, Optional

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from ..config import AuditConfig, CameraDefaults, PerceptionConfig, SamplingConfig
from ..schemas import RoadClass, Terrain

JOBS_DIR = Path(os.environ.get("CFI_JOBS_DIR", "outputs/jobs"))
JOBS_DIR.mkdir(parents=True, exist_ok=True)
STATIC = Path(__file__).parent / "static"
app = FastAPI(title="CFI Road Auditor", version="0.1.0", description="Automated Road Safety Audit for Indian roads (IRC/MoRTH)")
_jobs: Dict[str, Dict] = {}
_lock = threading.Lock()


def _run_job(job_id: str, media: str, track: Optional[str], cfg: AuditConfig, context: Dict):
    from ..pipeline import audit
    with _lock:
        _jobs[job_id]["status"] = "running"; _jobs[job_id]["started"] = time.time()
    try:
        rep = audit(media, cfg, track, context)
        with _lock:
            _jobs[job_id].update(status="done", finished=time.time(), outputs=rep.outputs,
                                 summary=rep.summary.model_dump(), report_id=rep.report_id)
    except Exception as e:  # pragma: no cover
        with _lock:
            _jobs[job_id].update(status="failed", error=str(e), finished=time.time())
    (JOBS_DIR / job_id / "job.json").write_text(json.dumps(_jobs[job_id], default=str, indent=1))


@app.get("/", response_class=HTMLResponse)
def index():
    return (STATIC / "index.html").read_text(encoding="utf-8")


@app.post("/api/audits")
async def create_audit(background: BackgroundTasks, media: UploadFile = File(...), track: Optional[UploadFile] = File(None),
                       road_class: str = Form("urban_arterial"), terrain: str = Form("plain"), title: str = Form("Road Safety Audit"),
                       location: str = Form(""), design_speed: Optional[float] = Form(None), posted_speed: Optional[float] = Form(None),
                       camera_height: float = Form(1.3), camera_pitch: float = Form(2.0), hfov: float = Form(70.0),
                       interval: float = Form(1.0), max_frames: int = Form(600), segment: float = Form(50.0),
                       use_vlm: bool = Form(False), assumed_speed: float = Form(30.0), height_locked: bool = Form(False)):
    try:
        rc, tr = RoadClass(road_class), Terrain(terrain)
    except ValueError as e:
        raise HTTPException(400, str(e))
    job_id = uuid.uuid4().hex[:12]
    jd = JOBS_DIR / job_id; jd.mkdir(parents=True, exist_ok=True)
    mp = jd / ("input" + Path(media.filename or "video.mp4").suffix.lower())
    with open(mp, "wb") as f:
        shutil.copyfileobj(media.file, f)
    tp = None
    if track is not None and track.filename:
        tp = jd / ("track" + Path(track.filename).suffix.lower())
        with open(tp, "wb") as f:
            shutil.copyfileobj(track.file, f)
    cfg = AuditConfig(road_class=rc, terrain=tr, design_speed_kmph=design_speed, posted_speed_kmph=posted_speed,
                      perception=PerceptionConfig(use_vlm=use_vlm),
                      sampling=SamplingConfig(frame_interval_s=interval, max_frames=max_frames, segment_length_m=segment),
                      camera=CameraDefaults(height_m=camera_height, pitch_deg=camera_pitch, hfov_deg=hfov, height_locked=height_locked),
                      out_dir=jd / "report", title=title, verbose=False)
    with _lock:
        _jobs[job_id] = {"job_id": job_id, "status": "queued", "created": time.time(), "media": mp.name, "title": title}
    background.add_task(_run_job, job_id, str(mp), str(tp) if tp else None, cfg, {"location": location, "assumed_speed_kmph": assumed_speed})
    return {"job_id": job_id, "status": "queued"}


@app.get("/api/audits/{job_id}")
def get_audit(job_id: str):
    j = _jobs.get(job_id)
    if j is None:
        p = JOBS_DIR / job_id / "job.json"
        if not p.exists():
            raise HTTPException(404, "job not found")
        j = json.loads(p.read_text())
    return JSONResponse(json.loads(json.dumps(j, default=str)))


@app.get("/api/audits/{job_id}/report")
def get_report_json(job_id: str):
    p = JOBS_DIR / job_id / "report" / "audit_report.json"
    if not p.exists():
        raise HTTPException(404, "report not ready")
    return FileResponse(p, media_type="application/json")


_MIME = {"html": "text/html", "pdf": "application/pdf", "json": "application/json", "geojson": "application/geo+json",
         "kml": "application/vnd.google-earth.kml+xml", "dxf": "application/dxf", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "csv": "text/csv"}
_NAME = {"html": "audit_report.html", "pdf": "audit_report.pdf", "json": "audit_report.json", "geojson": "audit_findings.geojson",
         "kml": "audit_findings.kml", "dxf": "audit_strip_plan.dxf", "xlsx": "audit_register.xlsx", "csv": "audit_findings.csv"}


@app.get("/api/audits/{job_id}/download/{kind}")
def download(job_id: str, kind: str):
    if kind not in _NAME:
        raise HTTPException(400, f"kind must be one of {list(_NAME)}")
    p = JOBS_DIR / job_id / "report" / _NAME[kind]
    if not p.exists():
        raise HTTPException(404, "not available")
    return FileResponse(p, media_type=_MIME[kind], filename=f"{job_id}_{_NAME[kind]}")


@app.get("/api/audits/{job_id}/evidence/{name}")
def evidence(job_id: str, name: str):
    p = (JOBS_DIR / job_id / "report" / "evidence" / name).resolve()
    if not str(p).startswith(str((JOBS_DIR / job_id).resolve())) or not p.exists():
        raise HTTPException(404)
    return FileResponse(p)


@app.get("/api/rules")
def rules():
    from ..rules.engine import load_rules
    return load_rules()


@app.get("/api/health")
def health():
    return {"ok": True, "jobs": len(_jobs)}
