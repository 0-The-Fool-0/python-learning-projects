# Python Learning Projects

A collection of independent Python exercises, kept in separate folders to preserve their original scope and implementation choices.

## Projects

| Directory | Overview | Main technologies |
|---|---|---|
| `PythonProject/` | “Dots” board game with a Tkinter UI and separated game logic. Includes a small test directory. | Python, Tkinter |
| `PythonProject2/` | European roulette visual simulation. | Python, Pygame |
| `PythonProject4/` | Numerical-methods exercise covering interpolation and spline calculations. | Python, NumPy; plotting/verification dependencies may be optional |
| `PythonProject5/` | Bézier curve generation using the de Casteljau algorithm. | Python, NumPy, Matplotlib |
| `PythonYandex1/` | Small introductory exercise with text input/output. | Python |

`PythonProject3` was not included because no source files were present in the inspected snapshot. `PythonProject1` is intentionally kept outside this collection because its local Git state has unresolved changes.

## Getting started

Each exercise has its own entry point and dependency requirements. There is no root-level installer or unified runner. Start by opening the selected folder and reading any project-specific instructions; install only that exercise's dependencies.

For example, the typical entry points are:

```bash
python PythonProject/main.py
python PythonProject2/main.py
python PythonProject4/mms.py
python PythonProject5/1.py
```

The commands above reflect file layout and have not been executed as part of this repository review.

## Notes

This is a learning archive, not a single integrated application. The individual projects and variants have not been merged or designated as canonical. Test coverage and launch requirements vary by folder and need to be checked before treating any exercise as a maintained project.