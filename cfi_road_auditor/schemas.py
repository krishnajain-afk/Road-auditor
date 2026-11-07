"""Core data model shared by every stage of the pipeline (pydantic v2)."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------------------
# Enumerations
# --------------------------------------------------------------------------------------
class RoadClass(str, Enum):
    """Road classification used to select IRC thresholds.

    Urban (IRC:86 / IRC:103 / IRC:SP:88) and rural (IRC:73 / IRC:SP:84 / 87 / 99) classes.
    """
    EXPRESSWAY = "expressway"
    NATIONAL_HIGHWAY = "national_highway"       # NH, rural, IRC:73 / IRC:SP:84 / IRC:SP:87
    STATE_HIGHWAY = "state_highway"
    MAJOR_DISTRICT_ROAD = "major_district_road"
    OTHER_DISTRICT_ROAD = "other_district_road"
    VILLAGE_ROAD = "village_road"
    URBAN_ARTERIAL = "urban_arterial"           # IRC:86
    URBAN_SUB_ARTERIAL = "urban_sub_arterial"
    URBAN_COLLECTOR = "urban_collector"
    URBAN_LOCAL = "urban_local"

    @property
    def is_urban(self) -> bool:
        return self.value.startswith("urban")


class Terrain(str, Enum):
    PLAIN = "plain"
    ROLLING = "rolling"
    MOUNTAINOUS = "mountainous"
    STEEP = "steep"


class AssetType(str, Enum):
    """Everything the perception layer can emit. Names are stable API."""
    # pavement condition
    POTHOLE = "pothole"
    CRACK_LONGITUDINAL = "crack_longitudinal"
    CRACK_TRANSVERSE = "crack_transverse"
    CRACK_ALLIGATOR = "crack_alligator"
    PATCH = "patch"
    RAVELLING = "ravelling"
    RUTTING = "rutting"
    EDGE_DROP = "edge_drop"
    WATERLOGGING = "waterlogging"
    DEBRIS = "debris"
    OPEN_MANHOLE = "open_manhole"
    MANHOLE = "manhole"
    # markings
    LANE_LINE = "lane_line"
    EDGE_LINE = "edge_line"
    CENTRE_LINE = "centre_line"
    STOP_LINE = "stop_line"
    ZEBRA_CROSSING = "zebra_crossing"
    GIVE_WAY_MARKING = "give_way_marking"
    ARROW_MARKING = "arrow_marking"
    HATCHING = "hatching"
    YELLOW_BOX = "yellow_box"
    RUMBLE_STRIP = "rumble_strip"
    # vertical signs / signals
    SIGN_MANDATORY = "sign_mandatory"
    SIGN_CAUTIONARY = "sign_cautionary"
    SIGN_INFORMATORY = "sign_informatory"
    SIGN_STOP = "sign_stop"
    SIGN_GIVE_WAY = "sign_give_way"
    SIGN_SPEED_LIMIT = "sign_speed_limit"
    SIGN_PEDESTRIAN_CROSSING = "sign_pedestrian_crossing"
    SIGN_SPEED_BREAKER = "sign_speed_breaker"
    SIGN_SCHOOL = "sign_school"
    SIGN_UNKNOWN = "sign_unknown"
    TRAFFIC_SIGNAL = "traffic_signal"
    PEDESTRIAN_SIGNAL = "pedestrian_signal"
    BLINKER = "blinker"
    # traffic calming / furniture
    SPEED_HUMP = "speed_hump"
    SPEED_TABLE = "speed_table"
    BOLLARD = "bollard"
    GUARDRAIL = "guardrail"
    CRASH_BARRIER = "crash_barrier"
    MEDIAN = "median"
    MEDIAN_OPENING = "median_opening"
    KERB = "kerb"
    FOOTPATH = "footpath"
    REFUGE_ISLAND = "refuge_island"
    STREET_LIGHT = "street_light"
    POLE = "pole"
    TREE = "tree"
    BUS_STOP = "bus_stop"
    BUS_BAY = "bus_bay"
    DELINEATOR = "delineator"
    CHEVRON = "chevron"
    OBJECT_MARKER = "object_marker"
    DRAIN = "drain"
    CULVERT = "culvert"
    BRIDGE = "bridge"
    # road users / hazards
    PEDESTRIAN = "pedestrian"
    CYCLIST = "cyclist"
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    AUTO_RICKSHAW = "auto_rickshaw"
    BUS = "bus"
    TRUCK = "truck"
    ANIMAL = "animal"
    PARKED_VEHICLE = "parked_vehicle"
    HAWKER_ENCROACHMENT = "hawker_encroachment"
    CONSTRUCTION = "construction"
    WRONG_SIDE_VEHICLE = "wrong_side_vehicle"
    # context
    INTERSECTION = "intersection"
    ROUNDABOUT = "roundabout"
    SCHOOL_ZONE = "school_zone"
    HOSPITAL_ZONE = "hospital_zone"
    WORK_ZONE = "work_zone"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    """IRC:SP:88 style severity of a deficiency."""
    CRITICAL = "critical"     # likely fatal / serious injury; immediate action
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"             # observation / good practice


class Likelihood(str, Enum):
    FREQUENT = "frequent"
    PROBABLE = "probable"
    OCCASIONAL = "occasional"
    IMPROBABLE = "improbable"


class Priority(str, Enum):
    """Action priority from the risk matrix."""
    IMMEDIATE = "P1_immediate"       # 0-30 days
    SHORT_TERM = "P2_short_term"     # 1-6 months
    MEDIUM_TERM = "P3_medium_term"   # 6-18 months
    LONG_TERM = "P4_long_term"       # programme / next resurfacing
    MONITOR = "P5_monitor"


class Source(str, Enum):
    YOLO = "yolo"
    SEGMENTATION = "segmentation"
    CLASSICAL = "classical_cv"
    OCR = "ocr"
    VLM = "vlm"
    GPS = "gps"
    MANUAL = "manual"
    FUSED = "fused"


# --------------------------------------------------------------------------------------
# Geometry primitives
# --------------------------------------------------------------------------------------
class GeoPoint(BaseModel):
    lat: float
    lon: float
    alt_m: Optional[float] = None
    t: Optional[float] = None          # seconds from media start
    speed_mps: Optional[float] = None
    heading_deg: Optional[float] = None
    hdop: Optional[float] = None


class BBox(BaseModel):
    """Axis aligned pixel bounding box (x1, y1, x2, y2)."""
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def w(self) -> float:
        return max(0.0, self.x2 - self.x1)

    @property
    def h(self) -> float:
        return max(0.0, self.y2 - self.y1)

    @property
    def area(self) -> float:
        return self.w * self.h

    @property
    def cx(self) -> float:
        return (self.x1 + self.x2) / 2

    @property
    def cy(self) -> float:
        return (self.y1 + self.y2) / 2

    @property
    def bottom_centre(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2, self.y2)

    def iou(self, other: "BBox") -> float:
        ix1, iy1 = max(self.x1, other.x1), max(self.y1, other.y1)
        ix2, iy2 = min(self.x2, other.x2), min(self.y2, other.y2)
        inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
        union = self.area + other.area - inter
        return inter / union if union > 0 else 0.0


class CameraModel(BaseModel):
    """Pinhole camera used for inverse perspective mapping (IPM)."""
    width_px: int
    height_px: int
    fx: float
    fy: float
    cx: float
    cy: float
    height_m: float = 1.3          # camera height above road surface (dash-mounted phone ~1.2-1.5 m)
    pitch_deg: float = 0.0         # +ve = looking down
    yaw_deg: float = 0.0
    roll_deg: float = 0.0
    hfov_deg: Optional[float] = None
    source: str = "default"        # exif | device_db | vanishing_point | default
    confidence: float = 0.5


# --------------------------------------------------------------------------------------
# Media & frames
# --------------------------------------------------------------------------------------
class MediaMeta(BaseModel):
    path: str
    kind: str                       # "video" | "image"
    width: int
    height: int
    duration_s: float = 0.0
    fps: float = 0.0
    n_frames: int = 0
    device_make: Optional[str] = None
    device_model: Optional[str] = None
    captured_at: Optional[str] = None
    has_embedded_gps: bool = False
    extra: Dict[str, Any] = Field(default_factory=dict)


class FrameRef(BaseModel):
    index: int
    t: float                        # seconds
    path: str                       # extracted frame image path
    chainage_m: Optional[float] = None
    geo: Optional[GeoPoint] = None
    brightness: Optional[float] = None   # mean luma 0-255 (night-time detection)
    is_night: Optional[bool] = None


# --------------------------------------------------------------------------------------
# Perception outputs
# --------------------------------------------------------------------------------------
class Detection(BaseModel):
    asset: AssetType
    label: str                              # raw model label (e.g. "D40", "traffic light")
    confidence: float
    bbox: Optional[BBox] = None
    polygon: Optional[List[Tuple[float, float]]] = None    # pixel polygon (segmentation)
    frame_index: int
    frame_t: float
    source: Source
    attributes: Dict[str, Any] = Field(default_factory=dict)  # e.g. {"text": "40", "colour": "red"}
    ground_xy_m: Optional[Tuple[float, float]] = None       # (lateral, longitudinal) wrt camera via IPM
    ground_size_m: Optional[Tuple[float, float]] = None     # (width, length) on road plane
    geo: Optional[GeoPoint] = None
    chainage_m: Optional[float] = None
    track_id: Optional[int] = None


class Measurement(BaseModel):
    """A measured road-geometry quantity at a chainage, with units and uncertainty."""
    name: str                     # e.g. carriageway_width_m, lane_width_m, curve_radius_m, gradient_pct
    value: float
    unit: str
    chainage_m: float
    uncertainty: Optional[float] = None
    method: str = "ipm"           # ipm | gps | vlm | manual
    confidence: float = 0.5
    frame_index: Optional[int] = None
    geo: Optional[GeoPoint] = None
    extra: Dict[str, Any] = Field(default_factory=dict)


class Asset(BaseModel):
    """A de-duplicated, geo-referenced physical asset or defect built from many detections."""
    asset_id: str
    asset: AssetType
    chainage_m: float
    chainage_end_m: Optional[float] = None
    geo: Optional[GeoPoint] = None
    side: Optional[str] = None            # left | right | centre | both
    confidence: float
    n_observations: int = 1
    best_frame_index: Optional[int] = None
    best_frame_path: Optional[str] = None
    bbox_in_best_frame: Optional[BBox] = None
    size_m: Optional[Tuple[float, float]] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    sources: List[Source] = Field(default_factory=list)


# --------------------------------------------------------------------------------------
# Road model
# --------------------------------------------------------------------------------------
class Segment(BaseModel):
    """Homogeneous audit section (default 50 m) with aggregated metrics."""
    segment_id: str
    start_m: float
    end_m: float
    start_geo: Optional[GeoPoint] = None
    end_geo: Optional[GeoPoint] = None
    metrics: Dict[str, float] = Field(default_factory=dict)      # medians/means of Measurements
    counts: Dict[str, int] = Field(default_factory=dict)         # asset counts by type
    flags: Dict[str, bool] = Field(default_factory=dict)         # has_footpath, is_night, is_intersection...
    frame_indices: List[int] = Field(default_factory=list)


class RoadModel(BaseModel):
    """Chainage-indexed digital twin of the surveyed road."""
    road_class: RoadClass
    terrain: Terrain = Terrain.PLAIN
    design_speed_kmph: Optional[float] = None
    posted_speed_kmph: Optional[float] = None
    length_m: float = 0.0
    track: List[GeoPoint] = Field(default_factory=list)
    frames: List[FrameRef] = Field(default_factory=list)
    segments: List[Segment] = Field(default_factory=list)
    assets: List[Asset] = Field(default_factory=list)
    measurements: List[Measurement] = Field(default_factory=list)
    camera: Optional[CameraModel] = None
    media: Optional[MediaMeta] = None
    context: Dict[str, Any] = Field(default_factory=dict)    # user supplied: name, junction, authority, etc.


# --------------------------------------------------------------------------------------
# Audit findings
# --------------------------------------------------------------------------------------
class Evidence(BaseModel):
    frame_index: Optional[int] = None
    frame_path: Optional[str] = None
    bbox: Optional[BBox] = None
    crop_path: Optional[str] = None
    note: Optional[str] = None


class Finding(BaseModel):
    finding_id: str                        # CFI-RSA-<chainage>-<CAT>-<n>
    rule_id: str
    category: str
    title: str
    description: str
    standard_ref: str                      # e.g. "IRC:103-2012 Cl. 5.2"
    requirement: str                       # what the standard requires
    observed: str                          # what we measured/saw
    chainage_m: float
    chainage_end_m: Optional[float] = None
    geo: Optional[GeoPoint] = None
    side: Optional[str] = None
    severity: Severity
    likelihood: Likelihood
    risk_score: int                        # 1..16 from matrix
    priority: Priority
    road_users_affected: List[str] = Field(default_factory=list)
    recommendation: str
    responsible_agency: str = "Road owning agency"
    indicative_cost: Optional[str] = None  # low / medium / high or INR band
    confidence: float = 0.5
    evidence: List[Evidence] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class ComplianceItem(BaseModel):
    """One checklist line in the compliance matrix."""
    rule_id: str
    category: str
    title: str
    standard_ref: str
    status: str                 # compliant | non_compliant | not_assessed | not_applicable
    detail: str = ""
    n_findings: int = 0


class ChecklistItem(BaseModel):
    """IRC:SP:88-2019 Stage-5 checklist line with the status derived from the mapped automated rules."""
    section: str
    section_title: str
    n: int
    question: str
    rules: List[str] = Field(default_factory=list)
    manual: bool = False
    status: str = "manual"          # deficient | satisfactory | partially_assessed | not_assessed | manual
    n_findings: int = 0
    detail: str = ""


class AuditSummary(BaseModel):
    overall_score: float                 # 0-100
    star_rating: int                     # 1-5 (iRAP-like, vehicle occupants + VRUs blended)
    star_rating_by_user: Dict[str, int] = Field(default_factory=dict)
    n_findings: int
    n_by_severity: Dict[str, int] = Field(default_factory=dict)
    n_by_category: Dict[str, int] = Field(default_factory=dict)
    top_risks: List[str] = Field(default_factory=list)
    length_m: float = 0.0
    assessed_rules: int = 0
    compliant_rules: int = 0
    not_assessed_rules: int = 0
    coverage_pct: float = 0.0            # fraction of applicable rules that could be assessed from the media
    checklist_counts: Dict[str, int] = Field(default_factory=dict)   # IRC:SP:88 items by status


class AuditReport(BaseModel):
    report_id: str
    title: str
    generated_at: str
    tool_version: str
    road_model: RoadModel
    findings: List[Finding]
    compliance: List[ComplianceItem]
    checklist: List[ChecklistItem] = Field(default_factory=list)
    summary: AuditSummary
    methodology: Dict[str, Any] = Field(default_factory=dict)
    limitations: List[str] = Field(default_factory=list)
    outputs: Dict[str, str] = Field(default_factory=dict)   # kind -> path
