import cv2
import numpy as np
from typing import Optional
from effects.basic import basic

class invertDiff(basic):
    def apply(self,frame: np.ndarray,control: bool = False) -> Optional[np.ndarray]:
        diff = super().apply(frame, control)

        if diff is None:
            return None

        return cv2.bitwise_not(diff)