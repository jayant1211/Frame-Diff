# entry point for code
# controls selecting video and selecting effect, enables control toggling
# passes req to render.py

from render import render_effect

EFFECTS = [
    'basic',
    # 'motionTrails',
    # 'frameEchoes',
]

def start(path: str = 'vids/1.mp4', effect: str = EFFECTS[0], control: bool = False, displayScale: float = 1.0) -> None:
    render_effect(path,
                  effect,
                  control,
                  displayScale)

if __name__ == "__main__":
    start(control=True, displayScale=.3)