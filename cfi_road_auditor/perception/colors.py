"""HSV colour masks tuned for Indian road furniture (white/yellow markings, red/blue signs, black-yellow kerbs)."""
from __future__ import annotations

import cv2
import numpy as np


def hsv(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def white_mask(img_bgr: np.ndarray, v_min: int = 110, s_max: int = 80, rel_min: int = 28) -> np.ndarray:
    """White paint = locally brighter than the surrounding surface, low saturation, above an absolute floor.

    Relative thresholding (vs a 61x61 local mean) keeps thin, blurred far-field lines and night-time markings;
    the absolute floor rejects noise on very dark surfaces."""
    h = hsv(img_bgr)
    v = h[:, :, 2]
    local = cv2.blur(v, (61, 61))
    rel = (v.astype(np.int16) - local.astype(np.int16))
    m = (rel > rel_min) & (v >= v_min) & (h[:, :, 1] <= s_max)
    m |= (v >= 225) & (h[:, :, 1] <= 45)
    return m.astype(np.uint8) * 255


def normalise_exposure(img_bgr: np.ndarray) -> np.ndarray:
    """Night / under-exposed frames: CLAHE on luminance + gain so colour masks keep working."""
    g = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    if g.mean() >= 70:
        return img_bgr
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    out = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    gain = min(2.5, 110.0 / max(20.0, g.mean()))
    return cv2.convertScaleAbs(out, alpha=gain, beta=0)


def yellow_mask(img_bgr: np.ndarray) -> np.ndarray:
    h = hsv(img_bgr)
    return cv2.inRange(h, (15, 70, 110), (38, 255, 255))


def red_mask(img_bgr: np.ndarray) -> np.ndarray:
    h = hsv(img_bgr)
    m1 = cv2.inRange(h, (0, 90, 70), (8, 255, 255))
    m2 = cv2.inRange(h, (168, 90, 70), (180, 255, 255))
    return cv2.bitwise_or(m1, m2)


def blue_mask(img_bgr: np.ndarray) -> np.ndarray:
    h = hsv(img_bgr)
    return cv2.inRange(h, (100, 110, 70), (128, 255, 255))


def green_mask(img_bgr: np.ndarray) -> np.ndarray:
    h = hsv(img_bgr)
    return cv2.inRange(h, (45, 90, 110), (85, 255, 255))


def dark_mask(img_bgr: np.ndarray, v_max: int = 60) -> np.ndarray:
    h = hsv(img_bgr)
    return (h[:, :, 2] <= v_max).astype(np.uint8) * 255
