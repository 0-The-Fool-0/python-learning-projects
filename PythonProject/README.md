# Dots — Tkinter coursework prototype

This folder contains a small 10×10 Tkinter board prototype. Players take turns placing points by clicking an empty cell. The **New game** button clears the board and starts again with Player 1.

## Run

Python 3 with Tkinter is required. From this directory:

```bash
python main.py
```

Run the logic tests from this directory with:

```bash
python -m unittest discover -s tests -t .
```

## Current limits

The board, turn order, and move validation are implemented. The original capture-detection method remains a placeholder, so captures and score changes are not implemented. `graphics.py`, `events.py`, and `widgets.py` are separate experiments and are not used by the current `main.py` interface; `graphics.py` additionally requires Pillow.
