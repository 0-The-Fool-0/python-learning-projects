[Русская версия](README.ru.md)

# Python Learning Projects

A collection of independent Python exercises, kept in separate folders to preserve their original scope and implementation choices.

## Projects

| Directory | Overview | Main technologies |
|---|---|---|
| `PythonProject/` | 10×10 Tkinter board prototype with alternating turns and move validation. Capture detection is not implemented. | Python, Tkinter |
| `PythonProject2/` | European roulette visual simulation. | Python, Pygame (not installed in the review environment) |
| `PythonProject4/` | Numerical-methods exercise covering interpolation and spline calculations. | Python, NumPy; Matplotlib and SciPy imports are optional |
| `PythonProject5/` | Bézier curve generation using the de Casteljau algorithm. | Python, NumPy, Matplotlib |
| `PythonYandex1/` | Small introductory exercise with text input/output. | Python |

`PythonProject3` was not included because no source files were present in the inspected snapshot. `PythonProject1` is intentionally kept outside this collection because its local Git state has unresolved changes.

## Getting started

Each exercise has its own entry point and dependency requirements. There is no root-level installer or unified runner. `PythonProject` uses Python and Tkinter; its logic tests run from that folder with `python -m unittest discover -s tests -t .`. For the other projects, install dependencies from the repository root with `python -m pip install -r PythonProject2/requirements.txt`, and similarly for `PythonProject4/requirements.txt` or `PythonProject5/requirements.txt`.

For example, the typical entry points are:

```bash
python PythonProject/main.py
python PythonProject2/main.py
python PythonProject4/mms.py
python PythonProject5/1.py
```

The roulette and Bézier commands start GUI/plot windows and were not launched in this review. The Tkinter interface is wired to the logic module; its display could not be smoke-tested in this non-interactive review session.

## Notes

This is a learning archive, not a single integrated application. The individual projects and variants have not been merged or designated as canonical. `PythonProject3` has no source files in this snapshot. Some exercises remain incomplete and should not be treated as maintained applications.
