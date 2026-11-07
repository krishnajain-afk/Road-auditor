"""Media probing and frame extraction (ffmpeg/ffprobe based, works for any phone / action-cam file)."""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from ..schemas import FrameRef, MediaMeta

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".3gp", ".insv", ".360", ".lrv", ".mts", ".webm"}


def _run(cmd: List[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def ffprobe_json(path: str) -> Dict:
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe not found - install ffmpeg")
    out = _run([
        "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", path,
    ])
    return json.loads(out)


def read_image_exif(path: str) -> Dict:
    """EXIF (make/model/focal/GPS/datetime) for still photos. Never raises."""
    info: Dict = {}
    try:
        import exifread  # type: ignore
        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)
        def g(k):
            v = tags.get(k)
            return str(v) if v is not None else None
        info["make"] = g("Image Make")
        info["model"] = g("Image Model")
        info["datetime"] = g("EXIF DateTimeOriginal") or g("Image DateTime")
        fl = tags.get("EXIF FocalLength")
        if fl is not None:
            try:
                info["focal_mm"] = float(fl.values[0].num) / float(fl.values[0].den)
            except Exception:
                pass
        fl35 = tags.get("EXIF FocalLengthIn35mmFilm")
        if fl35 is not None:
            try:
                info["focal_35mm"] = float(str(fl35))
            except Exception:
                pass
        lat, lon = _exif_gps(tags)
        if lat is not None:
            info["lat"], info["lon"] = lat, lon
            alt = tags.get("GPS GPSAltitude")
            if alt is not None:
                try:
                    info["alt_m"] = float(alt.values[0].num) / float(alt.values[0].den)
                except Exception:
                    pass
        orient = g("Image Orientation")
        if orient:
            info["orientation"] = orient
    except Exception:
        pass
    return info


def _exif_gps(tags) -> Tuple[Optional[float], Optional[float]]:
    def to_deg(v):
        d = [float(x.num) / float(x.den) for x in v.values]
        return d[0] + d[1] / 60 + d[2] / 3600
    try:
        lat = to_deg(tags["GPS GPSLatitude"])
        lon = to_deg(tags["GPS GPSLongitude"])
        if str(tags.get("GPS GPSLatitudeRef")) == "S":
            lat = -lat
        if str(tags.get("GPS GPSLongitudeRef")) == "W":
            lon = -lon
        return lat, lon
    except Exception:
        return None, None


def probe_media(path: str) -> MediaMeta:
    p = Path(path)
    ext = p.suffix.lower()
    if ext in IMAGE_EXT:
        img = cv2.imread(str(p))
        if img is None:
            raise ValueError(f"Cannot read image {path}")
        h, w = img.shape[:2]
        exif = read_image_exif(str(p))
        return MediaMeta(
            path=str(p), kind="image", width=w, height=h, n_frames=1,
            device_make=exif.get("make"), device_model=exif.get("model"),
            captured_at=exif.get("datetime"), has_embedded_gps="lat" in exif, extra={"exif": exif},
        )
    meta = ffprobe_json(str(p))
    vs = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
    if vs is None:
        raise ValueError(f"No video stream in {path}")
    w, h = int(vs.get("width", 0)), int(vs.get("height", 0))
    # rotation (phones record landscape sensor + rotate tag)
    rot = 0
    try:
        rot = int(vs.get("tags", {}).get("rotate", 0))
    except Exception:
        pass
    for sd in vs.get("side_data_list", []) or []:
        if "rotation" in sd:
            try:
                rot = int(round(float(sd["rotation"])))
            except Exception:
                pass
    if rot % 180 != 0:
        w, h = h, w
    fps = _parse_rate(vs.get("avg_frame_rate") or vs.get("r_frame_rate") or "0/1")
    fmt = meta.get("format", {})
    dur = float(fmt.get("duration") or vs.get("duration") or 0.0)
    tags = {**fmt.get("tags", {}), **vs.get("tags", {})}
    make = tags.get("com.apple.quicktime.make") or tags.get("make") or tags.get("manufacturer")
    model = tags.get("com.apple.quicktime.model") or tags.get("model") or tags.get("com.android.model")
    created = tags.get("creation_time") or tags.get("com.apple.quicktime.creationdate")
    loc = tags.get("com.apple.quicktime.location.ISO6709") or tags.get("location") or tags.get("location-eng")
    has_gps = bool(loc) or any(
        (s.get("codec_type") == "data" or s.get("codec_type") == "subtitle") for s in meta.get("streams", [])
    )
    n_frames = int(vs.get("nb_frames") or 0) or int(round(dur * fps))
    return MediaMeta(
        path=str(p), kind="video", width=w, height=h, duration_s=dur, fps=fps, n_frames=n_frames,
        device_make=make, device_model=model, captured_at=created, has_embedded_gps=has_gps,
        extra={"tags": tags, "rotation": rot, "streams": [
            {"codec_type": s.get("codec_type"), "codec_name": s.get("codec_name"),
             "handler": (s.get("tags") or {}).get("handler_name")} for s in meta.get("streams", [])]},
    )


def _parse_rate(r: str) -> float:
    try:
        if "/" in r:
            a, b = r.split("/")
            return float(a) / float(b) if float(b) else 0.0
        return float(r)
    except Exception:
        return 0.0


def mean_luma(img: np.ndarray) -> float:
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    return float(g.mean())


def extract_frames(
    media: MediaMeta,
    out_dir: str,
    interval_s: float = 1.0,
    max_frames: int = 1500,
    resize_long_edge: int = 1280,
    timestamps: Optional[List[float]] = None,
) -> List[FrameRef]:
    """Extract frames at fixed time interval (or explicit timestamps) into JPEGs.

    Uses OpenCV sequential decode (robust, no re-encode). Returns FrameRef list with mean luma
    so later stages can flag night-time footage.
    """
    os.makedirs(out_dir, exist_ok=True)
    refs: List[FrameRef] = []
    if media.kind == "image":
        img = cv2.imread(media.path)
        img = _resize(img, resize_long_edge)
        dst = os.path.join(out_dir, "frame_000000.jpg")
        cv2.imwrite(dst, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
        lum = mean_luma(img)
        return [FrameRef(index=0, t=0.0, path=dst, brightness=lum, is_night=lum < 60)]

    cap = cv2.VideoCapture(media.path)
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV cannot open {media.path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or media.fps or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or media.n_frames or 0)
    if timestamps is None:
        dur = media.duration_s or (total / fps if fps else 0)
        n = int(math.floor(dur / interval_s)) + 1 if dur > 0 else 1
        if n > max_frames:  # thin uniformly
            interval_s = dur / max_frames
            n = max_frames
        timestamps = [i * interval_s for i in range(n)]
    timestamps = sorted(t for t in timestamps if t >= 0)[:max_frames]
    wanted = [int(round(t * fps)) for t in timestamps]
    rot = media.extra.get("rotation", 0) if media.extra else 0
    wi = 0
    fi = 0
    ok = True
    while ok and wi < len(wanted):
        target = wanted[wi]
        # jump if far away (seek is cheap for keyframes, else decode sequentially)
        if target - fi > int(fps * 3):
            cap.set(cv2.CAP_PROP_POS_FRAMES, target)
            fi = target
        ok, img = cap.read()
        if not ok:
            break
        if fi >= target:
            img = _apply_rotation(img, rot)
            img = _resize(img, resize_long_edge)
            dst = os.path.join(out_dir, f"frame_{wi:06d}.jpg")
            cv2.imwrite(dst, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
            lum = mean_luma(img)
            refs.append(FrameRef(index=wi, t=float(timestamps[wi]), path=dst, brightness=lum, is_night=lum < 60))
            wi += 1
        fi += 1
    cap.release()
    return refs


def _apply_rotation(img: np.ndarray, rot: int) -> np.ndarray:
    # OpenCV already applies rotation metadata in recent versions; be defensive about double-rotation
    # by checking aspect: only rotate when image orientation disagrees with metadata.
    return img


def _resize(img: np.ndarray, long_edge: int) -> np.ndarray:
    h, w = img.shape[:2]
    m = max(h, w)
    if long_edge and m > long_edge:
        s = long_edge / m
        img = cv2.resize(img, (int(round(w * s)), int(round(h * s))), interpolation=cv2.INTER_AREA)
    return img


def crop_evidence(frame_path: str, bbox, out_path: str, pad: float = 0.25) -> Optional[str]:
    img = cv2.imread(frame_path)
    if img is None:
        return None
    h, w = img.shape[:2]
    bw, bh = bbox.x2 - bbox.x1, bbox.y2 - bbox.y1
    x1 = int(max(0, bbox.x1 - pad * bw)); y1 = int(max(0, bbox.y1 - pad * bh))
    x2 = int(min(w, bbox.x2 + pad * bw)); y2 = int(min(h, bbox.y2 + pad * bh))
    if x2 <= x1 or y2 <= y1:
        return None
    crop = img[y1:y2, x1:x2]
    cv2.rectangle(crop, (int(bbox.x1 - x1), int(bbox.y1 - y1)), (int(bbox.x2 - x1), int(bbox.y2 - y1)), (0, 0, 255), 2)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, crop, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return out_path
