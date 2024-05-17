from scipy.optimize import minimize
import numpy as np
import numpy


def make_data_lab_2():
    x = numpy.linspace(-10, 10, 100)
    y = numpy.linspace(-10, 10, 100)

    x_grid, y_grid = numpy.meshgrid(x, y)

    z = 2 * x_grid * x_grid + 2 * x_grid * y_grid + 2* y_grid*y_grid - 4*x_grid - 6*y_grid
    return x_grid, y_grid, z


def kp(x, y):
    #   global points
    points = []

    def fun(x_i):  # Функция
        x = x_i[0]
        y = x_i[1]
        return 2 * x * x + 2 * x * y + 2* y*y - 4*x - 6*y

    def callback(x_w):
        g_list = np.ndarray.tolist(x_w)
        g_list.append(fun(x_w))
        points.append(g_list)

    b = (0, float("inf"))  # диапазон поиска
    bounds = (b, b)
    con = (
        {'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
        {'type': 'ineq', 'fun': lambda x: 2 - x[0] - 2 * x[1]}
    )

    res = minimize(fun, _, method="SLSQP", bounds=bounds,
                   constraints=con, callback=callback)

    glist = np.ndarray.tolist(res.x)
    glist.append(res.fun)
    points.append(glist)

    for iteration, point in enumerate(points):
        yield iteration, point






















_ = (0,0)