"""Runtime configuration."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from .schemas import RoadClass, Terrain

PKG_DIR = Path(__file__).resolve().parent
REPO_DIR = PKG_DIR.parent
DATA_DIR = Path(os.environ.get("CFI_DATA_DIR", REPO_DIR / "data"))
MODELS_DIR = Path(os.environ.get("CFI_MODELS_DIR", DATA_DIR / "models"))
RULES_FILE = PKG_DIR / "rules" / "data" / "irc_rules.yaml"


class PerceptionConfig(BaseModel):
    yolo_weights: Optional[str] = None            # path or well-known name (yolov8n.pt ...)
    yolo_conf: float = 0.25
    yolo_iou: float = 0.5
    yolo_imgsz: int = 640
    damage_weights: Optional[str] = None          # RDD2022-style road-damage YOLO
    sign_weights: Optional[str] = None            # Indian traffic sign YOLO
    seg_weights: Optional[str] = None             # road/footpath segmentation
    use_classical: bool = True                    # classical CV fallbacks
    use_ocr: bool = False
    use_vlm: bool = False                         # Claude vision checklist pass
    vlm_model: str = "claude-fable-5-1"
    vlm_max_frames: int = 24
    vlm_cache_dir: Optional[str] = None           # directory of <frame_stem>.json checklists (offline / reviewed VLM results)
    device: str = "cpu"


class SamplingConfig(BaseModel):
    frame_interval_s: float = 1.0                 # time based when no GPS
    frame_interval_m: float = 5.0                 # distance based when GPS is available
    max_frames: int = 1500
    segment_length_m: float = 50.0
    resize_long_edge: int = 1280
    reuse_frames_dir: Optional[str] = None        # reuse frames (and manifest) extracted by a previous run of the same media


class CameraDefaults(BaseModel):
    height_m: float = 1.3
    pitch_deg: float = 2.0
    hfov_deg: float = 70.0            # typical phone main camera (26 mm eq) ~ 69-72 deg
    height_locked: bool = False       # True = user measured the camera height; skip zebra-based scale calibration


class AuditConfig(BaseModel):
    survey_mode: str = "drive"        # drive = camera in/on a vehicle on the carriageway; walk = auditor walking the footpath
    road_class: RoadClass = RoadClass.URBAN_ARTERIAL
    terrain: Terrain = Terrain.PLAIN
    design_speed_kmph: Optional[float] = None
    posted_speed_kmph: Optional[float] = None
    perception: PerceptionConfig = Field(default_factory=PerceptionConfig)
    sampling: SamplingConfig = Field(default_factory=SamplingConfig)
    camera: CameraDefaults = Field(default_factory=CameraDefaults)
    out_dir: Path = Path("outputs")
    title: str = "Road Safety Audit"
    authority: str = ""
    auditor: str = "CFI Road Auditor (automated)"
    keep_frames: bool = True
    verbose: bool = True
