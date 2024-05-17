import math
import random
import numpy as np
import copy


def my_function(x, y, limits_x, limits_y):
    if x < limits_x[0] or x > limits_x[1]:
        return 10000 + math_function(x, y)

    if y < limits_y[0] or y > limits_y[1]:
        return 10000 + math_function(x, y)

    return math_function(x, y)


def math_function(x, y):
    return (-x * np.sin(np.sqrt(abs(x)))) + (-y * np.sin(np.sqrt(abs(y))))


def trigger():
    particles_count = 300  # Количество частиц
    iterations_count = 50  # Количество итераций
    limits_x = (-10, 10)  # Ограничения X
    limits_y = (-10, 10)  # Ограничения Y
    coeff_personal = 2  # Фи пе (коэффициент при своем лучшем значении)
    coeff_global = 9  # Фи ге (коэффициент при глобальном лучшем значении)
    coeff_speed = 0.4  # Общий коэффициент скорости (от 0 до 1)

    # Создание первоначального роя частиц
    particles = []
    global_best = (None, None, None)
    if coeff_personal + coeff_global < 4:
        s = coeff_personal + coeff_global
        coeff_personal = coeff_personal * (4 / s)
        coeff_global = coeff_global * (4 / s)
    for i in range(particles_count):
        particle_x = random.uniform(limits_x[0], limits_x[1])
        particle_y = random.uniform(limits_y[0], limits_y[1])
        particle_value = my_function(particle_x, particle_y, limits_x, limits_y)

        # Задаём конфигурацию каждой частице
        particles.append({
            'x': particle_x,
            'y': particle_y,
            'value': particle_value,
            # Скорость в декартовом пространстве (вектор)
            'speed': (random.uniform(limits_x[0] - particle_x, limits_x[1] - particle_x),
                      random.uniform(limits_y[0] - particle_y, limits_y[1] - particle_y)),
            'best': (particle_x, particle_y, particle_value)
        })

        # Устанавливаем наилучший глобальный минимум
        if (global_best[2] is None) or (particle_value < global_best[2]):
            global_best = (particle_x, particle_y, particle_value)

    x, y = [], []

    result = []
    iterations = []
    iterations.append({
        "iteration": 1,
        "data": particles
    })

    print(particles)

    # Итерации
    for j in range(iterations_count):
        particles_copy = copy.deepcopy(particles)
        x.clear()
        y.clear()

        # Проход по каждой частице
        for i in range(particles_count):
            particle = particles_copy[i]

            # Считаем лучшее собственное значение
            particle_value = my_function(particle['x'], particle['y'], limits_x, limits_y)
            if particle_value < particle['best'][2]:
                particle['best'] = (particle['x'], particle['y'], particle_value)

            # Считаем лучшее глобальное значение
            if particle_value < global_best[2]:
                global_best = (particle['x'], particle['y'], particle_value)

            # Считаем новый вектор скорости
            particle_coords = (particle['x'], particle['y'])
            rand_personal = random.uniform(0, 1)
            rand_global = random.uniform(0, 1)
            coeff_sum = coeff_personal + coeff_global
            tmp = (2 * coeff_speed) / abs(2 - coeff_sum - math.sqrt(coeff_sum * coeff_sum - 4 * coeff_sum))
            new_speed = []
            for coord_i in range(len(particle['speed'])):
                v = particle['speed'][coord_i]
                new_speed.append(tmp * (v + coeff_personal * rand_personal * (
                            particle['best'][coord_i] - particle_coords[coord_i]) + coeff_global * rand_global * (
                                                     global_best[coord_i] - particle_coords[coord_i])))
            new_speed = tuple(new_speed)
            particle['speed'] = new_speed

            # Двигаем частицу
            particle['x'] += particle['speed'][0]
            particle['y'] += particle['speed'][1]
            particle['value'] = my_function(particle['x'], particle['y'], limits_x, limits_y)

            x.append(particle['x'])
            y.append(particle['y'])


        result.append({
            "iteration": j,
            "x": global_best[0],
            "y": global_best[1],
            "z": global_best[2]
        })

        iterations.append({
            "iteration": j,
            "data": particles_copy
        })

        particles = particles_copy

        print(f'Итерация {j} => Best: {global_best}')

    print(f'Итоговый минимум: {global_best}')
    return (result, iterations)


if __name__ == '__main__':
    trigger()
