import cv2
import numpy as np
from frame_buffer import nFrames
from typing import Optional
from effects.baseClass import Effect

class basic(Effect):
    def __init__(self):
        super().__init__()
        self.gap = 1
        self.alpha = 2.4
        self.beta = 0    

    def init_controls(self) -> None:
        cv2.namedWindow(self.control_window, cv2.WINDOW_NORMAL)
        # alpha and beta
        cv2.createTrackbar('alpha(10x) ', self.control_window, 24, 50, lambda x: None) # controls contrast
        cv2.createTrackbar('beta', self.control_window, 0, 255, lambda x: None) # controls overall brightness

        #gaps
        cv2.createTrackbar('frame gap', self.control_window, 1, 50, lambda x: None)
        cv2.setTrackbarMin('frame gap', self.control_window, 1)
        self.control_init = True

    def update_values(self) -> None:
        self.gap = cv2.getTrackbarPos('frame gap', self.control_window)
        self.alpha = cv2.getTrackbarPos('alpha(10x) ', self.control_window)/10
        self.beta = float(cv2.getTrackbarPos('beta', self.control_window))

    def apply(self, frame: np.ndarray, control: bool = False) -> Optional[np.ndarray]:
        nFrames.append(frame)
        if len(nFrames)<=self.gap:
            return

        res = cv2.absdiff(nFrames[-1], nFrames[-1-self.gap])
        
        if control:
            if not self.control_init: 
                self.init_controls()
                
            self.update_values()
            res = cv2.convertScaleAbs(res, alpha= self.alpha, beta= self.beta)

        return res