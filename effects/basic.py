import cv2
import numpy as np
from frame_buffer import nFrames
from typing import Optional

class basic:
    def __init__(self):
        self.control_init = False

    def _init_controls(self) -> None:
        cv2.namedWindow("Controls", cv2.WINDOW_NORMAL)
        cv2.imshow("Controls", np.zeros((300,500,3),dtype=np.uint8)) # initilization avoids trackbar overflow 
        cv2.createTrackbar('alpha*10', "Controls", 10, 50, lambda x: None) # controls contrast
        cv2.createTrackbar('beta', "Controls", 0, 255, lambda x: None) # controls overall brightness
        self.control_init = True

    def _get_values(self) -> tuple[float, float]:
        return cv2.getTrackbarPos('alpha*10', "Controls")/10, float(cv2.getTrackbarPos('beta', "Controls"))

    def apply(self, frame:np.array, control: bool) -> Optional[np.array]:
        # playback builds the buffer
        nFrames.append(frame)
        if len(nFrames)<=1:
            return

        res = cv2.absdiff(nFrames[-1], nFrames[-2])
        
        if control:
            if not self.control_init: 
                self._init_controls()
                
            a, b = self._get_values()
            res = cv2.convertScaleAbs(res, alpha = a, beta=b)

        return res

    