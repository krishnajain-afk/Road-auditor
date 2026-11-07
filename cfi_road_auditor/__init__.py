"""CFI Road Auditor - automated Road Safety Audit for Indian roads.

Pipeline: media ingest -> perception (detectors / segmentation / classical CV / VLM)
-> geometry (camera model, inverse-perspective mapping, GPS track analytics)
-> road model (chainage-indexed assets & measurements) -> IRC/MoRTH rule engine
-> risk scoring (IRC:SP:88 style) -> reports (PDF / HTML / JSON / GeoJSON / DXF / XLSX).
"""
__version__ = "0.1.0"
