# renders original video and generated effects
# intermediate betwn main and effects

import cv2
import logging
import numpy as np
from effects.baseClass import Effect
import importlib

logging.basicConfig(level=logging.INFO,
                    format= "%(levelname)s : %(message)s")

def prep(cap: cv2.VideoCapture) -> int:
    if not cap.isOpened():
        raise RuntimeError(f'Could not load video')

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps<=0:
        logging.warning('Unable to get fps. defaulting to 24')
        fps = 24

    return int(1000/fps)

def select_effect(effect_name: str) -> Effect:
    try:
        module = importlib.import_module(f"effects.{effect_name}")
        effect = getattr(module, effect_name)
        return effect()
    except (ModuleNotFoundError, AttributeError):
        raise ValueError(f"Unknown effect: {effect_name} ")

def render_effect(path: str, effect_name: str, control: bool, displayScale: float = 1.0) -> None:

    
    cap = cv2.VideoCapture(path)
    
    if displayScale<=0 or displayScale>1.5:
        logging.warning('displayScale invalid/too large. defaulting to 1.0')
        displayScale = 1.0
    
    delay = prep(cap)
    effect = select_effect(effect_name)

    window_name = f"original vs {effect_name}"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, o_frame = cap.read()
            if not ret:
                logging.info('eof')
                break
    
            m_frame = effect.apply(o_frame, control)
            
            if m_frame is None:
                continue

            combined = np.hstack((o_frame,m_frame))
            if displayScale!=1.0:
                combined = cv2.resize(combined,(0,0),fx=displayScale, fy=displayScale)
            
            cv2.imshow(window_name, combined)
    
            if cv2.waitKey(delay) & 0xFF==ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()






        

    

    
