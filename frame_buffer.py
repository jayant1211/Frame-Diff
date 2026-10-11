# Manages shared frame history for effects, supporting frame-based
# and time-based access independently of the rendering logic.
# 
from collections import deque

# last n-frames
nFrames = deque(maxlen=100)