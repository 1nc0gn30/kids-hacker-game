# KidGame3

Section/scene-structured Python + Pygame story game.

Current build includes:
- Section 1
- Scene 1 (`Parrot OS desktop -> email alert -> opened warning email -> malware popup`)
- Scene 2 (`loopback tunnel raid` rendered with Ursina 3D)

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

## Controls

- Scene 1 still rewards fast typing, but each beat also has a highlighted keyword objective (`SCAN`, `OPEN`, `TRACE`, `ISOLATE`).
- Scene 2 now launches a 3D Ursina tunnel raid where you fly a drone with `WASD` or arrow keys and trigger objectives with `2`, `E`, `Q`, and `R`.
- Press `Esc` to quit.

## Status

- Section 1 Scene 1 is implemented.
- Section 1 Scene 2 is implemented.
- Story reference is tracked in `STORYLINE.md`.
- Scene 3 design reference is tracked in `SCENE03_DESIGN.md`.
# kids-hacker-game
