# visualize pixel displacement in fading trail
import cv2
import numpy as np
from effects.baseClass import Effect
from frame_buffer import nFrames

class pixelDisplacement(Effect):
    def __init__(self):
        super().__init__()
        self.trail = None
        self.trail_decay = 0.9 #this is multipliying effect 
        self.motion_mask_threshold = 20 #minimum thresh
        self.motion_mask_blur = 5 #kernel size
        self.alpha = .65
        self.beta = .7 # this doesnt hadve to add to 1 - it'll clip if exceeded, darker if under <1, 1 is mathematically perfect blend
        #print("Effect Initialized")

    def init_controls(self) -> None:
        cv2.namedWindow(self.control_window, cv2.WINDOW_NORMAL)
        cv2.createTrackbar('trail decay (10x) ', self.control_window, 9, 10, lambda x: None) 
        cv2.createTrackbar('mask thresh', self.control_window, 20, 30, lambda x: None) 
        cv2.createTrackbar('kernel size', self.control_window, 5, 15, lambda x: None) 
        cv2.createTrackbar('org blend (10x)', self.control_window, 6, 10, lambda x: None) 
        cv2.createTrackbar('trail blend (10x)', self.control_window, 7, 10, lambda x: None) 
        cv2.setTrackbarMin('kernel size', self.control_window, 3)
        cv2.setTrackbarMin('mask thresh', self.control_window, 10)
        #cv2.setTrackbarMin('trail decay (10x) ', self.control_window, 5)
       
        self.control_init = True

    def update_values(self) -> None:
        self.trail_decay = cv2.getTrackbarPos('trail decay (10x) ', self.control_window)/10
        self.motion_mask_threshold = cv2.getTrackbarPos('mask thresh', self.control_window)
        self.motion_mask_blur = cv2.getTrackbarPos('kernel size', self.control_window)
        self.alpha = cv2.getTrackbarPos('org blend (10x)', self.control_window)/10
        self.beta = cv2.getTrackbarPos('trail blend (10x)', self.control_window)/10
        if self.motion_mask_blur%2==0:
            self.motion_mask_blur+=1

    def apply(self, frame, control = False):
        nFrames.append(frame)
        if len(nFrames) < 2:
            self.trail = np.zeros_like(frame, dtype=np.float32)
            print(self.trail.shape)
            return None

        if control:
            if not self.control_init:
                self.init_controls()
            self.update_values()
        
        diff = cv2.absdiff(nFrames[-1], nFrames[-2])

        #mask 
        _, motion_mask = cv2.threshold(diff, self.motion_mask_threshold, 255, cv2.THRESH_BINARY)
        motion_mask = cv2.GaussianBlur(motion_mask, (self.motion_mask_blur, self.motion_mask_blur), 0)

        mask = motion_mask.astype(np.float32)/255.0

        #trail decay
        self.trail *= self.trail_decay

        self.trail = self.trail*(1-mask) + frame*mask # Update trail pixel-wise: preserve the decayed trail where there's no motion,
                                                      # and replace it with the current frame where motion is detected.

        result = cv2.addWeighted(frame, self.alpha, self.trail.astype(np.uint8), self.beta, 0)

        return result