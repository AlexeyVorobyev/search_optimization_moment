import numpy
import numpy as np
import numdifftools as nd

def buta(x, y):
    return numpy.power((x + 2 * y - 7), 2) + numpy.power((2 * x + y - 5), 2)

def himmel(x,y):
    return numpy.power((numpy.power(x, 2) + y - 11), 2) + numpy.power((x + numpy.power(y, 2) - 7), 2)

def make_data_lab_1():
    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
    x = numpy.linspace(-10, 10, 100)
    y = numpy.linspace(-10, 10, 100)

    # Создаем двумерную матрицу-сетку
    x_grid, y_grid = numpy.meshgrid(x, y)

    # В узлах рассчитываем значение функции
    z = buta(x_grid, y_grid)
    return x_grid, y_grid, z


def funct_consider(res_x, res_y, res_step, res_iterations):
    x_list = []
    y_list = []
    z_list = []

    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
    for item in gradient_descent(buta, res_x, res_y, res_step, res_iterations):
        x_list.append(item[0])
        y_list.append(item[1])
        z_list.append(item[3])

    return x_list, y_list, z_list


def partial_function(f___, input, pos, value):
    tmp = input[pos]
    input[pos] = value
    ret = f___(*input)
    input[pos] = tmp
    return ret


def gradient(function, input):
    """Частная производная по каждому из параметров функции f(т.е. градиент)"""

    ret = np.empty(len(input))
    for i in range(len(input)):
        f_g = lambda x: partial_function(function, input, i, x)
        ret[i] = nd.Derivative(f_g)(input[i])
    return ret


def next_point(x, y, gx, gy, step) -> tuple:
    return x - step * gx, y - step * gy


def gradient_descent(function, x0, y0, tk, m):
    yield x0, y0, 0, function(x0, y0)

    e1 = 0.0001
    e2 = 0.0001

    k = 0
    while True:
        (gx, gy) = gradient(function, [x0, y0])  # 3

        if np.linalg.norm((gx, gy)) < e1:  # Шаг 4. Проверить выполнение критерия окончания
            break

        if k >= m:  # Шаг 5
            break

        x1, y1 = next_point(x0, y0, gx, gy, tk)  # 7
        f1 = function(x1, y1)
        f0 = function(x0, y0)
        while not f1 < f0:  # 8 условие
            tk = tk / 2
            x1, y1 = next_point(x0, y0, gx, gy, tk)
            f1 = function(x1, y1)
            f0 = function(x0, y0)

        if np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) < e2 and abs(f1 - f0) < e2:  # 9
            break
        else:
            k += 1
            x0, y0 = x1, y1
            yield x0, y0, k, f1
