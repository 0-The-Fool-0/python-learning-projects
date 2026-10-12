import numpy as np

# Matplotlib is optional: on some Windows/Python builds it may be unavailable.
try:
    import matplotlib.pyplot as plt  # type: ignore
except ModuleNotFoundError:
    plt = None
# SciPy is optional: CubicSpline was only used for verification and isn't required.
try:
    from scipy.interpolate import CubicSpline  # type: ignore  # noqa: F401
except ModuleNotFoundError:
    CubicSpline = None  # type: ignore


# Функции варианта 2
def f1(x):
    return x ** 2 * np.sin(2 * x)


def f2(x):
    return np.sqrt(np.abs(x) + 4)


# Производные для граничных условий сплайна (вторые производные)
def f1_second(x):
    # f1''(x) = 2*sin(2x) + 4x*cos(2x) - 4x^2*sin(2x) ? Проверим:
    # f1' = 2x sin(2x) + 2x^2 cos(2x)
    # f1'' = 2 sin(2x) + 4x cos(2x) + 4x cos(2x) - 4x^2 sin(2x) = 2 sin(2x) + 8x cos(2x) - 4x^2 sin(2x)
    return 2 * np.sin(2 * x) + 8 * x * np.cos(2 * x) - 4 * x ** 2 * np.sin(2 * x)


def f2_second(x):
    # f2(x) = sqrt(|x|+4). На концах отрезка x=±2, модуль раскрывается однозначно.
    # Для x>0: f2 = sqrt(x+4), f2'' = -1/(4 (x+4)^(3/2))
    # Для x<0: f2 = sqrt(4-x), f2'' = -1/(4 (4-x)^(3/2))
    if x >= 0:
        return -1 / (4 * (x + 4) ** (3 / 2))
    else:
        return -1 / (4 * (4 - x) ** (3 / 2))


# Генерация равномерных узлов
def uniform_nodes(a, b, n):
    return np.linspace(a, b, n + 1)


# Генерация чебышевских узлов
def chebyshev_nodes(a, b, n):
    k = np.arange(n + 1)
    x = np.cos((2 * k + 1) * np.pi / (2 * (n + 1)))
    return (a + b) / 2 + (b - a) / 2 * x


# Вычисление разделённых разностей
def divided_differences(x, y):
    n = len(x)
    coef = np.copy(y).astype(float)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    return coef


# Построение многочлена Ньютона по коэффициентам и узлам
def newton_poly(coef, x_nodes, x):
    n = len(coef) - 1
    res = coef[n]
    for i in range(n - 1, -1, -1):
        res = res * (x - x_nodes[i]) + coef[i]
    return res


# Получение символьного представления многочлена степени 2 (для вывода)
def newton_symbolic(coef, x_nodes):
    # coef = [f[x0], f[x0,x1], f[x0,x1,x2]]
    a0 = coef[0]
    a1 = coef[1]
    a2 = coef[2]
    # P(x) = a0 + a1*(x-x0) + a2*(x-x0)*(x-x1)
    # Раскрываем в стандартную форму: p2*x^2 + p1*x + p0
    x0, x1 = x_nodes[0], x_nodes[1]
    p2 = a2
    p1 = a1 - a2 * (x0 + x1)
    p0 = a0 - a1 * x0 + a2 * x0 * x1
    return f"P(x) = {p2:.6f} x^2 + {p1:.6f} x + {p0:.6f}"


# Построение кубического сплайна с заданными вторыми производными на концах
def cubic_spline(x_nodes, y_nodes, fpp_left, fpp_right):
    n = len(x_nodes) - 1
    h = np.diff(x_nodes)
    # Система для вторых производных (метод прогонки)
    alpha = np.zeros(n + 1)
    beta = np.zeros(n + 1)
    A = np.zeros(n + 1)
    B = np.zeros(n + 1)
    C = np.zeros(n + 1)
    F = np.zeros(n + 1)

    # Подготовка коэффициентов
    for i in range(1, n):
        A[i] = h[i - 1]
        B[i] = 2 * (h[i - 1] + h[i])
        C[i] = h[i]
        F[i] = 6 * ((y_nodes[i + 1] - y_nodes[i]) / h[i] - (y_nodes[i] - y_nodes[i - 1]) / h[i - 1])

    # Граничные условия (вторая производная задана)
    # m0 = fpp_left, mn = fpp_right
    # Для i=1: A[1]*m0 + B[1]*m1 + C[1]*m2 = F[1] -> переносим A[1]*m0 в правую часть
    # Аналогично для i=n-1
    F[1] -= A[1] * fpp_left
    F[n - 1] -= C[n - 1] * fpp_right
    B[1] -= 0  # уже учтено? Обычно A[1] не обнуляется, но мы перенесли.
    # Теперь система для m1..m_{n-1} с трёхдиагональной матрицей, где A[1] и C[n-1] остаются.
    # Используем прогонку.
    # Прямой ход
    for i in range(2, n):
        xi = A[i] / B[i - 1]
        B[i] -= xi * C[i - 1]
        F[i] -= xi * F[i - 1]
    # Обратный ход
    m = np.zeros(n + 1)
    m[n] = fpp_right
    m[n - 1] = (F[n - 1] - C[n - 1] * m[n]) / B[n - 1]
    for i in range(n - 2, 0, -1):
        m[i] = (F[i] - C[i] * m[i + 1]) / B[i]
    m[0] = fpp_left

    # Вычисление коэффициентов сплайна на каждом отрезке
    a = y_nodes[:-1]
    b = np.zeros(n)
    c = m[:-1] / 2
    d = np.zeros(n)
    for i in range(n):
        d[i] = (m[i + 1] - m[i]) / (6 * h[i])
        b[i] = (y_nodes[i + 1] - y_nodes[i]) / h[i] - h[i] * (m[i + 1] + 2 * m[i]) / 6

    # Функция, вычисляющая сплайн в точке x
    def spline_func(x):
        # Определяем индекс отрезка
        if x < x_nodes[0] or x > x_nodes[-1]:
            return np.nan
        i = np.searchsorted(x_nodes, x) - 1
        if i == n:  # точно правый край
            i = n - 1
        dx = x - x_nodes[i]
        return a[i] + b[i] * dx + c[i] * dx ** 2 + d[i] * dx ** 3

    return spline_func


# Основная программа
a, b = -2, 2
ns = [2, 4, 8, 16]
funcs = [f1, f2]
func_names = ['f1(x) = x^2 sin(2x)', 'f2(x) = sqrt(|x|+4)']

for idx_func, f in enumerate(funcs):
    print(f"\n=== {func_names[idx_func]} ===")

    # Задание 1: равномерные узлы
    print("\n--- Равномерная сетка (задание 1) ---")
    for n in ns:
        x_nodes = uniform_nodes(a, b, n)
        y_nodes = f(x_nodes)
        coef = divided_differences(x_nodes, y_nodes)
        # Для n=2 выводим аналитическое представление
        if n == 2:
            print(f"n=2: {newton_symbolic(coef, x_nodes)}")

        # Построение графика (сохраняем в файл)
        x_plot = np.linspace(a, b, 500)
        y_true = f(x_plot)
        y_interp = [newton_poly(coef, x_nodes, xi) for xi in x_plot]

        if plt is not None:
            plt.figure(figsize=(8, 5))
            plt.plot(x_plot, y_true, 'k-', label='Исходная функция')
            plt.plot(x_plot, y_interp, 'r--', label=f'Ньютон (n={n})')
            plt.plot(x_nodes, y_nodes, 'bo', label='Узлы')
            plt.legend()
            plt.title(f'{func_names[idx_func]}, равномерная сетка, n={n}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig(f'fig1_{idx_func + 1}_uniform_n{n}.png')
            plt.close()

    # Задание 2: чебышевские узлы
    print("\n--- Чебышевская сетка (задание 2) ---")
    for n in ns:
        x_nodes = chebyshev_nodes(a, b, n)
        y_nodes = f(x_nodes)
        coef = divided_differences(x_nodes, y_nodes)
        if n == 2:
            print(f"n=2: {newton_symbolic(coef, x_nodes)}")

        x_plot = np.linspace(a, b, 500)
        y_true = f(x_plot)
        y_interp = [newton_poly(coef, x_nodes, xi) for xi in x_plot]

        if plt is not None:
            plt.figure(figsize=(8, 5))
            plt.plot(x_plot, y_true, 'k-', label='Исходная функция')
            plt.plot(x_plot, y_interp, 'r--', label=f'Ньютон (n={n})')
            plt.plot(x_nodes, y_nodes, 'bo', label='Узлы')
            plt.legend()
            plt.title(f'{func_names[idx_func]}, чебышевская сетка, n={n}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig(f'fig2_{idx_func + 1}_cheb_n{n}.png')
            plt.close()

    # Задание 3: кубический сплайн (равномерная сетка)
    print("\n--- Кубический сплайн (задание 3) ---")
    # Вычисляем граничные вторые производные
    fpp_left = f1_second(a) if idx_func == 0 else f2_second(a)
    fpp_right = f1_second(b) if idx_func == 0 else f2_second(b)
    print(f"Граничные условия: f''({a}) = {fpp_left:.6f}, f''({b}) = {fpp_right:.6f}")

    for n in ns:
        x_nodes = uniform_nodes(a, b, n)
        y_nodes = f(x_nodes)
        spline = cubic_spline(x_nodes, y_nodes, fpp_left, fpp_right)

        x_plot = np.linspace(a, b, 500)
        y_true = f(x_plot)
        y_spline = [spline(xi) for xi in x_plot]

        if plt is not None:
            plt.figure(figsize=(8, 5))
            plt.plot(x_plot, y_true, 'k-', label='Исходная функция')
            plt.plot(x_plot, y_spline, 'r--', label=f'Сплайн (n={n})')
            plt.plot(x_nodes, y_nodes, 'bo', label='Узлы')
            plt.legend()
            plt.title(f'{func_names[idx_func]}, кубический сплайн, n={n}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig(f'fig3_{idx_func + 1}_spline_n{n}.png')
            plt.close()

if plt is None:
    print("\n[info] matplotlib не установлена — графики не строились (расчёты выполнены).")