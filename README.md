# KidGame3

Section/scene-structured Python + Pygame story game.

Current build includes:
- Section 1
- Scene 1 (`Parrot OS desktop -> email alert -> opened warning email -> malware popup`)
- Scene 2 (`loopback packet capture review`)

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

## Controls

- Scene 1 still rewards fast typing, but each beat also has a highlighted keyword objective (`SCAN`, `OPEN`, `TRACE`, `ISOLATE`).
- Scene 2 now uses guided packet-triage prompts: choose filters with number keys, type investigation words like `MIRROR`, and make response choices such as `Q` for quarantine.
- Press `Esc` to quit.

## Status

- Section 1 Scene 1 is implemented.
- Section 1 Scene 2 is implemented.
- Story reference is tracked in `STORYLINE.md`.
- Scene 3 design reference is tracked in `SCENE03_DESIGN.md`.
# kids-hacker-game
