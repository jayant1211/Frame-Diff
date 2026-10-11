# renders original video and generated effects
# intermediate betwn main and effects

import cv2
import logging
from effects.basic import basic

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

def select_effect(effect_name: str) -> object: # or maybe return type should be Effect and define Effect protocol in new baseClass for all effects with inializing shared props, probably unnecessary #TODO
    if effect_name == 'basic':
        return basic()

    raise ValueError(f'Unknown effect: {effect_name}')

def render_effect(path: str, effect_name: str, control: bool) -> None:
    cap = cv2.VideoCapture(path)
    delay = prep(cap)
    effect = select_effect(effect_name)

    while True:
        ret, o_frame = cap.read()
        if not ret:
            logging.info('eof')
            break

        m_frame = effect.apply(o_frame, control)
        cv2.imshow("original", o_frame)
        if m_frame is None:
            continue
        cv2.imshow(f'{effect_name}',m_frame)

        if cv2.waitKey(delay) & 0xFF==ord('q'):
            break






        

    

    
