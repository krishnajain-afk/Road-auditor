from __future__ import annotations

from typing import List, Optional

import numpy as np

from ..schemas import CameraModel, Detection, FrameRef


class Detector:
    """Interface: every perception backend maps a frame to Detections (pixel space)."""
    name: str = "base"
    enabled: bool = True

    def detect(self, img: np.ndarray, frame: FrameRef, cam: Optional[CameraModel] = None) -> List[Detection]:
        raise NotImplementedError

    def warmup(self) -> None:  # optional
        pass
