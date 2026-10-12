# abstract base class for all effects
# handles init and cleanup for controls

from abc import ABC, abstractmethod
import cv2
import numpy as np
from typing import Optional

class Effect(ABC):
    def __init__(self):
        self.control_init = False
        self.control_window = "Controls"

    def init_controls(self) -> None:
        pass

    @abstractmethod
    def apply(self, frame: np.ndarray, control: bool = False) -> Optional[np.ndarray]:
        '''apply effect to givem frame'''
        pass
