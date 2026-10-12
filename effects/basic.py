import cv2
import numpy as np
from frame_buffer import nFrames
from typing import Optional
from effects.baseClass import Effect

class basic(Effect):
    def init_controls(self) -> None:
        cv2.namedWindow(self.control_window, cv2.WINDOW_NORMAL)
        cv2.createTrackbar('alpha(10x) ', self.control_window, 10, 50, lambda x: None) # controls contrast
        cv2.createTrackbar('beta', self.control_window, 0, 255, lambda x: None) # controls overall brightness
        self.control_init = True

    def get_values(self) -> tuple[float, float]:
            return cv2.getTrackbarPos('alpha(10x) ', self.control_window)/10, float(cv2.getTrackbarPos('beta', self.control_window))

    def apply(self, frame: np.ndarray, control: bool = False,) -> Optional[np.ndarray]:
        nFrames.append(frame)
        if len(nFrames)<=1:
            return

        res = cv2.absdiff(nFrames[-1], nFrames[-2])
        
        if control:
            if not self.control_init: 
                self.init_controls()
                
            a, b = self.get_values()
            res = cv2.convertScaleAbs(res, alpha = a, beta=b)

        return res