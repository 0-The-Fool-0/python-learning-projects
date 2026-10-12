import numpy as np
import matplotlib.pyplot as plt


def de_casteljau(points, t):
    points = np.array(points)

    while len(points) > 1:
        points = (1 - t) * points[:-1] + t * points[1:]

    return points[0]


def bezier_curve(control_points, num_points=100):
    curve = []
    for t in np.linspace(0, 1, num_points):
        point = de_casteljau(control_points, t)
        curve.append(point)
    return np.array(curve)


def plot_bezier(control_points, title):
    curve = bezier_curve(control_points)

    cp = np.array(control_points)

    plt.plot(curve[:, 0], curve[:, 1], label="Bezier curve")
    plt.plot(cp[:, 0], cp[:, 1], 'o--', label="Control points")

    plt.title(title)
    plt.legend()
    plt.grid()
    plt.axis('equal')


# 4 набора точек
sets = [
    [(3, 1), (4, 3), (1, 4), (2, 2)],
    [(3, 1), (5, 0), (0, 3), (2, 2)],
    [(3, 1), (3, 5), (2, 0), (2, 2)],
    [(3, 1), (6, 2), (0, 2), (2, 2)]
]

plt.figure(figsize=(10, 8))

for i, s in enumerate(sets):
    plt.subplot(2, 2, i + 1)
    plot_bezier(s, f"Curve {i + 1}")

plt.tight_layout()
plt.show()