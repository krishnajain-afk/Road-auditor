"""GPS / sensor track ingestion and alignment to frames.

Supported inputs
  * GPX / KML / CSV side-car files (phone GPS loggers, Strava, Open Camera, GPS Logger)
  * QuickTime 'com.apple.quicktime.location.ISO6709' single tag (iPhone - one fix per clip)
  * DJI Osmo / Mavic .SRT subtitle sidecars (per-frame [latitude: ..] [longitude: ..])
  * GoPro GPMF (via `gpmf` python pkg if installed, else ffmpeg extraction of GPS5 is not attempted)
  * NMEA text logs
A track is a list of GeoPoint with t = seconds from media start. If the track clock is absolute
(GPX time), the media creation_time is used to align; otherwise the first point maps to t=0.
"""
from __future__ import annotations

import csv
import json
import math
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import numpy as np

from ..schemas import FrameRef, GeoPoint, MediaMeta

EARTH_R = 6371008.8


def haversine_m(lat1, lon1, lat2, lon2) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R * math.asin(math.sqrt(a))


def bearing_deg(lat1, lon1, lat2, lon2) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


# ------------------------------------------------------------------ parsers
def _parse_iso(ts: str) -> Optional[datetime]:
    ts = ts.strip().replace("Z", "+00:00")
    for fmt in (None, "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S%z", "%Y:%m:%d %H:%M:%S"):
        try:
            d = datetime.fromisoformat(ts) if fmt is None else datetime.strptime(ts, fmt)
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            return d
        except Exception:
            continue
    return None


def parse_gpx(path: str) -> List[Tuple[Optional[datetime], float, float, Optional[float]]]:
    import gpxpy  # type: ignore
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        g = gpxpy.parse(f)
    pts = []
    for trk in g.tracks:
        for seg in trk.segments:
            for p in seg.points:
                t = p.time
                if t is not None and t.tzinfo is None:
                    t = t.replace(tzinfo=timezone.utc)
                pts.append((t, p.latitude, p.longitude, p.elevation))
    if not pts:
        for p in g.waypoints:
            pts.append((p.time, p.latitude, p.longitude, p.elevation))
    return pts


def parse_csv(path: str):
    pts = []
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        rd = csv.DictReader(f)
        cols = {c.lower(): c for c in rd.fieldnames or []}
        def pick(*names):
            for n in names:
                if n in cols:
                    return cols[n]
            return None
        clat = pick("lat", "latitude"); clon = pick("lon", "lng", "longitude")
        ct = pick("time", "timestamp", "datetime", "date time", "utc", "t", "seconds")
        calt = pick("alt", "altitude", "ele", "elevation", "alt_m")
        if not clat or not clon:
            raise ValueError("CSV needs lat/lon columns")
        for row in rd:
            try:
                lat, lon = float(row[clat]), float(row[clon])
            except Exception:
                continue
            t = None
            if ct:
                raw = row[ct]
                try:
                    t = float(raw)
                except Exception:
                    t = _parse_iso(raw)
            alt = None
            if calt:
                try:
                    alt = float(row[calt])
                except Exception:
                    pass
            pts.append((t, lat, lon, alt))
    return pts


_SRT_LAT = re.compile(r"\[?latitude\s*[:=]\s*(-?\d+\.\d+)", re.I)
_SRT_LON = re.compile(r"\[?longitude\s*[:=]\s*(-?\d+\.\d+)", re.I)
_SRT_ALT = re.compile(r"(?:rel_alt|abs_alt|altitude)\s*[:=]\s*(-?\d+\.?\d*)", re.I)
_SRT_GPS = re.compile(r"GPS\s*\(\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.?\d*)\s*\)", re.I)
_SRT_TIME = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->")


def parse_dji_srt(path: str):
    """DJI SRT: blocks with timecode and '[latitude: x] [longitude: y]' or 'GPS (lon, lat, alt)'."""
    pts = []
    txt = Path(path).read_text(encoding="utf-8", errors="ignore")
    for block in re.split(r"\n\s*\n", txt):
        mt = _SRT_TIME.search(block)
        if not mt:
            continue
        t = int(mt[1]) * 3600 + int(mt[2]) * 60 + int(mt[3]) + int(mt[4]) / 1000
        mlat, mlon = _SRT_LAT.search(block), _SRT_LON.search(block)
        alt = None
        if mlat and mlon:
            lat, lon = float(mlat[1]), float(mlon[1])
        else:
            mg = _SRT_GPS.search(block)
            if not mg:
                continue
            lon, lat, alt = float(mg[1]), float(mg[2]), float(mg[3])
        ma = _SRT_ALT.search(block)
        if ma:
            alt = float(ma[1])
        pts.append((t, lat, lon, alt))
    return pts


def parse_nmea(path: str):
    pts = []
    for line in Path(path).read_text(errors="ignore").splitlines():
        if "$GPRMC" in line or "$GNRMC" in line:
            f = line.split(",")
            if len(f) > 6 and f[2] == "A":
                try:
                    lat = float(f[3][:2]) + float(f[3][2:]) / 60 * (1 if f[4] == "N" else -1)
                    lon = float(f[5][:3]) + float(f[5][3:]) / 60 * (1 if f[6] == "E" else -1)
                    hh, mm, ss = int(f[1][:2]), int(f[1][2:4]), float(f[1][4:])
                    pts.append((hh * 3600 + mm * 60 + ss, lat, lon, None))
                except Exception:
                    pass
    return pts


def parse_iso6709(s: str) -> Optional[Tuple[float, float, Optional[float]]]:
    m = re.match(r"([+-]\d+\.?\d*)([+-]\d+\.?\d*)([+-]\d+\.?\d*)?", s.strip())
    if not m:
        return None
    lat, lon = float(m[1]), float(m[2])
    alt = float(m[3]) if m[3] else None
    return lat, lon, alt


def extract_gpmf_track(video_path: str):
    """GoPro: use `gpmf` if installed (pip install gpmf). Returns [] when unavailable."""
    try:
        import gpmf  # type: ignore
        stream = gpmf.io.extract_gpmf_stream(video_path)
        gps_blocks = gpmf.gps.extract_gps_blocks(stream)
        pts = []
        for b in gps_blocks:
            d = gpmf.gps.parse_gps_block(b)
            for i, (lat, lon, alt, *_rest) in enumerate(d.latitude and zip(d.latitude, d.longitude, d.altitude) or []):
                pts.append((None, lat, lon, alt))
        return pts
    except Exception:
        return []


# ------------------------------------------------------------------ public API
def _to_track(raw, media: Optional[MediaMeta]) -> List[GeoPoint]:
    """Normalise raw tuples to GeoPoints with t = seconds from media start."""
    if not raw:
        return []
    times = [r[0] for r in raw]
    t0_media = None
    if media and media.captured_at:
        t0_media = _parse_iso(media.captured_at)
    pts: List[GeoPoint] = []
    if all(isinstance(t, datetime) for t in times):
        t_ref = t0_media or times[0]
        for t, lat, lon, alt in raw:
            pts.append(GeoPoint(lat=lat, lon=lon, alt_m=alt, t=(t - t_ref).total_seconds()))
    elif all(isinstance(t, (int, float)) for t in times):
        t_first = float(times[0])
        for t, lat, lon, alt in raw:
            pts.append(GeoPoint(lat=lat, lon=lon, alt_m=alt, t=float(t) - t_first))
    else:  # no timing: spread uniformly over media duration
        dur = media.duration_s if media else float(len(raw) - 1)
        n = max(1, len(raw) - 1)
        for i, (_t, lat, lon, alt) in enumerate(raw):
            pts.append(GeoPoint(lat=lat, lon=lon, alt_m=alt, t=dur * i / n))
    pts.sort(key=lambda p: p.t)
    # drop exact duplicates in time
    out = []
    for p in pts:
        if out and abs(out[-1].t - p.t) < 1e-6:
            continue
        out.append(p)
    return _annotate_speed_heading(out)


def _annotate_speed_heading(pts: List[GeoPoint]) -> List[GeoPoint]:
    for i, p in enumerate(pts):
        j = i + 1 if i + 1 < len(pts) else i
        k = i - 1 if i > 0 else i
        if j == k:
            continue
        d = haversine_m(pts[k].lat, pts[k].lon, pts[j].lat, pts[j].lon)
        dt = (pts[j].t - pts[k].t) or 1e-6
        p.speed_mps = d / dt
        p.heading_deg = bearing_deg(pts[k].lat, pts[k].lon, pts[j].lat, pts[j].lon)
    return pts


def load_track(path: str, media: Optional[MediaMeta] = None) -> List[GeoPoint]:
    ext = Path(path).suffix.lower()
    if ext == ".gpx":
        raw = parse_gpx(path)
    elif ext == ".csv":
        raw = parse_csv(path)
    elif ext == ".srt":
        raw = parse_dji_srt(path)
    elif ext in {".nmea", ".txt", ".log"}:
        raw = parse_nmea(path)
    elif ext == ".json":
        data = json.loads(Path(path).read_text())
        raw = [(d.get("t"), d["lat"], d["lon"], d.get("alt")) for d in data]
    else:
        raise ValueError(f"Unsupported track format {ext}")
    return _to_track(raw, media)


def track_from_video(media: MediaMeta) -> List[GeoPoint]:
    """Pull whatever GPS is embedded: a sidecar SRT next to the file, QuickTime single fix, GoPro GPMF."""
    p = Path(media.path)
    for cand in (p.with_suffix(".SRT"), p.with_suffix(".srt"), p.with_suffix(".gpx"), p.with_suffix(".GPX")):
        if cand.exists():
            try:
                tr = load_track(str(cand), media)
                if tr:
                    return tr
            except Exception:
                pass
    tags = (media.extra or {}).get("tags", {}) if media.extra else {}
    if media.kind == "image":
        ex = (media.extra or {}).get("exif", {})
        if "lat" in ex:
            return [GeoPoint(lat=ex["lat"], lon=ex["lon"], alt_m=ex.get("alt_m"), t=0.0)]
        return []
    loc = tags.get("com.apple.quicktime.location.ISO6709") or tags.get("location") or tags.get("location-eng")
    if loc:
        r = parse_iso6709(loc)
        if r:
            lat, lon, alt = r
            return [GeoPoint(lat=lat, lon=lon, alt_m=alt, t=0.0)]
    gp = extract_gpmf_track(media.path)
    if gp:
        return _to_track(gp, media)
    return []


def cumulative_chainage(track: Sequence[GeoPoint]) -> np.ndarray:
    ch = np.zeros(len(track))
    for i in range(1, len(track)):
        ch[i] = ch[i - 1] + haversine_m(track[i - 1].lat, track[i - 1].lon, track[i].lat, track[i].lon)
    return ch


def interpolate_at(track: Sequence[GeoPoint], t: float) -> Optional[GeoPoint]:
    if not track:
        return None
    ts = np.array([p.t for p in track])
    if t <= ts[0]:
        return track[0].model_copy()
    if t >= ts[-1]:
        return track[-1].model_copy()
    i = int(np.searchsorted(ts, t) - 1)
    a, b = track[i], track[i + 1]
    f = (t - a.t) / ((b.t - a.t) or 1e-6)
    return GeoPoint(
        lat=a.lat + f * (b.lat - a.lat), lon=a.lon + f * (b.lon - a.lon),
        alt_m=(a.alt_m + f * (b.alt_m - a.alt_m)) if (a.alt_m is not None and b.alt_m is not None) else a.alt_m,
        t=t, speed_mps=a.speed_mps, heading_deg=a.heading_deg,
    )


def sync_track_to_frames(frames: List[FrameRef], track: Sequence[GeoPoint]) -> List[FrameRef]:
    """Attach geo + chainage to frames. Without a track, chainage is left None (time-indexed audit)."""
    if not track:
        return frames
    ch = cumulative_chainage(track)
    ts = np.array([p.t for p in track])
    for fr in frames:
        g = interpolate_at(track, fr.t)
        fr.geo = g
        fr.chainage_m = float(np.interp(fr.t, ts, ch))
    return frames


def estimate_chainage_without_gps(frames: List[FrameRef], assumed_speed_kmph: float = 30.0) -> List[FrameRef]:
    v = assumed_speed_kmph / 3.6
    for fr in frames:
        fr.chainage_m = fr.t * v
    return frames
