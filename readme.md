# FrameDiff

Real-time video effects built on OpenCV and NumPy, using temporal frame history to isolate, amplify, and transform motion dynamics.

---

## Implemented Effects

### 1. Basic Frame Differencing (`basic`)
Computes the absolute difference between frames across a configurable temporal gap (`t` vs `t - gap`). Highlights moving edges and motion contours while canceling out static backgrounds.

* **Controls**:
  * `alpha (10x)`: Contrast amplification.
  * `beta`: Brightness offset.
  * `frame gap`: Distance in time between compared frames (from 1 to 50 frames).

https://github.com/user-attachments/assets/basicDifferencing.mp4

<video src="output/basicDifferencing.mp4" controls="controls" width="100%"></video>

---

### 2. Pixel Displacement (`pixelDisplacement`)
Extracts motion via dynamic thresholding, smooths edges with Gaussian blur, and accumulates moving pixels into a decaying temporal buffer. Moving subjects leave fading, long-exposure light trails while stationary areas remain crisp.

* **Controls**:
  * `trail decay (10x)`: Speed at which historical motion trails fade out.
  * `mask thresh`: Minimum difference magnitude required to register motion.
  * `kernel size`: Gaussian blur radius for softening motion boundaries.
  * `org blend (10x)` / `trail blend (10x)`: Mix ratio between live footage and accumulated ghost trails.

https://github.com/user-attachments/assets/pixelDifferencing.mp4

<video src="output/pixelDifferencing.mp4" controls="controls" width="100%"></video>

---

## Core Architecture

```
main.py ──► render.py ──► effects/<effect_name>.py
                 │                     │
                 ▼                     ▼
          OpenCV Display        frame_buffer.py (deque history)
```

* **Modular Base Class (`effects/baseClass.py`)**: All effects inherit from the abstract `Effect` interface, enforcing a unified `.apply(frame, control)` contract.
* **Dynamic Plugin Loading (`render.py`)**: Effects are imported and instantiated at runtime via `importlib` based on their name — no manual import lists required.
* **Unified Display Layout**: Renders the original footage and effect side-by-side (`hstack`), automatically normalizing channel depth (`to_bgr`) and preventing window overflow with safe scaling (`displayScale`).
* **Interactive Controls**: Real-time OpenCV trackbars allow live parameter experimentation without restarting playback.
* **Recording**: Optional MP4 output export matching source FPS and dimensions via OpenCV's `VideoWriter`.

---

## Getting Started

### Prerequisites
* Python 3.10+
* `opencv-python`
* `numpy`

```bash
pip install opencv-python numpy
```

### Running

Configure parameters and select an effect in `main.py`:

```python
# main.py
start(
    path='vids/1.mp4',
    effect='basic',       # 'basic', 'pixelDisplacement', 'invertDiff'
    control=True,         # Open interactive sliders
    displayScale=0.4,     # Scale display window to fit monitor
    grayscale=False,      # Process in BGR color or grayscale
    save=False            # Export processed video to output/
)
```

Run:
```bash
python main.py
```
* Press **`q`** at any time to exit cleanly and close all windows.