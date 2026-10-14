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


---

### 2. Pixel Displacement (`pixelDisplacement`)
Extracts motion via dynamic thresholding, smooths edges with Gaussian blur, and accumulates moving pixels into a decaying temporal buffer. Moving subjects leave fading, long-exposure light trails while stationary areas remain crisp.

* **Controls**:
  * `trail decay (10x)`: Speed at which historical motion trails fade out.
  * `mask thresh`: Minimum difference magnitude required to register motion.
  * `kernel size`: Gaussian blur radius for softening motion boundaries.
  * `org blend (10x)` / `trail blend (10x)`: Mix ratio between live footage and accumulated ghost trails.


---

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