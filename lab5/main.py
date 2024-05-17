import time
import tkinter as tk
from random import uniform
from tkinter import messagebox
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Функция Химмельблау
def himmelblau_function(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Градиент функции Химмельблау
def gradient_himmelblau(x, y):
    dx = 4 * x * (x**2 + y - 11) + 2 * (x + y**2 - 7)
    dy = 2 * (x**2 + y - 11) + 4 * y * (x + y**2 - 7)
    return dx, dy

# Функция сферы
def sphere_function(x, y):
    return x**2 + y**2

# Градиент функции сферы
def gradient_sphere(x, y):
    dx = 2 * x
    dy = 2 * y
    return dx, dy

# Функция Бута
def booth_function(x, y):
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2

# Градиент функции Бута
def booth_gradient(x, y):
    dx = 2 * (x + 2*y - 7) + 4 * (2*x + y - 5)
    dy = 4 * (x + 2*y - 7) + 2 * (2*x + y - 5)
    return dx, dy

# Функция Розенброка
def rosenbrock(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

# Задача для симплекс метода
def simplex_task(x, y):
    return 2*x**2 + 2*x*y + 2*y**2 - 4*x - 6*y

# Функция Растригина
def rastrigin(x, y):
    return (x**2 - 10 * np.cos(2 * np.pi * x)) + (y**2 - 10 * np.cos(2 * np.pi * y)) + 20

def choose_function(name_function):
    '''
    Выбор функции по её названию
    '''
    if name_function == "Химмельблау":
        return himmelblau_function
    elif name_function == "Сфера":
        return sphere_function
    elif name_function == "Функция Бута":
        return booth_function
    elif name_function == "Розенброк":
        return rosenbrock
    elif name_function == "Растригина":
        return rastrigin
    else:
        messagebox.showerror("Ошибка", "Выбранная функция пока не поддерживается")
        return False

# Создание GUI окна
root = tk.Tk()
root.title("Визуализация функции с методом оптимизации")


points_var = tk.StringVar(value=100)
points_var_3 = tk.StringVar(value=100)
individual_var_3 = tk.StringVar(value=20)

# Для симплекс метода
point_x_simplex = tk.StringVar(value=2)
point_y_simplex = tk.StringVar(value=2)

# Создание вкладок
tab_control = ttk.Notebook(root)
tab5 = ttk.Frame(tab_control)

tab_control.add(tab5, text='Пчелиный алгоритм')
tab_control.pack(expand=1, fill='both')

# 5 лаба, основной вызов функции

points_var_5 = tk.StringVar(value=200)
scout_var_5 = tk.StringVar(value=20)
perspective_bee_var_5 = tk.StringVar(value=10)
best_bee_var_5 = tk.StringVar(value=20)
perspective_var_5 = tk.StringVar(value=3)
best_var_5 = tk.StringVar(value=1)
size_var_5 = tk.StringVar(value=0.5)

def visualize_5():
    selected_function = function_var_5.get()
    function = choose_function(selected_function)
    if (function == False):
        return

    points_text_5.delete("1.0", tk.END)
    x = np.linspace(-5, 5, 500)
    y = np.linspace(-5, 5, 500)
    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)
    ax5.cla()
    ax5.plot_surface(X, Y, Z, cmap='inferno', alpha=0.5)
    ax5.set_xlabel('X')
    ax5.set_ylabel('Y')
    ax5.set_zlabel('Z')
    ax5.set_title("Пчелинный алгоритм")
    ax5.view_init(elev=30, azim=45)


    n_point = int(points_var_5.get()) # количество итераций
    n_scout = int(scout_var_5.get()) # количество разведчиков
    n_perspective_bee = int(perspective_bee_var_5.get()) # количество пчёл на перспективном участке
    n_best_bee = int(best_bee_var_5.get()) # кол-во пчёл на элитных участках
    n_perspective = int(perspective_var_5.get()) # кол-во перспективных участков
    n_best = int(best_var_5.get()) # кол-во элитных участков
    size = float(size_var_5.get()) # размер участка

    def scout_spawn(n_scout):
        '''
        Функция получения участков с помощью пчёл разведчиков
        '''
        scouts = [[0] * 3 for i in range(n_scout)]
        for i in range(n_scout):
            scouts[i][1] = uniform(-5,5)
            scouts[i][2] = uniform(-5,5)
            scouts[i][0] = function(scouts[i][1], scouts[i][2])
        return scouts

    def best_bee_spawn(bp, n_best_bee, size):
        '''
        Функция выборки точек на лучших участках
        '''
        bb = [[0] * 3 for i in range(n_best_bee)]
        bb[0][1] = bp[1]
        bb[0][2] = bp[2]
        bb[0][0] = function(bb[0][1], bb[0][2])
        for i in range(1, n_best_bee):
            bb[i][1] = bp[1] + uniform(-size, size)
            bb[i][2] = bp[2] + uniform(-size, size)
            bb[i][0] = function(bb[i][1], bb[i][2])
        return bb

    def perspective_bee_spawn(pp, n_perspective_bee, size):
        '''
        Функция выборки точек на перспективных учатсках
        '''
        pb = [[0] * 3 for i in range(n_perspective_bee)]
        pb[0][1] = pp[1]
        pb[0][2] = pp[2]
        pb[0][0] = function(pb[0][1], pb[0][2])
        for i in range(1, n_perspective_bee):
            pb[i][1] = pp[1] + uniform(-size, size)
            pb[i][2] = pp[2] + uniform(-size, size)
            pb[i][0] = function(pb[i][1], pb[i][2])
        return pb

    scouts = scout_spawn(n_scout) # сначала отправляем разведчиков
    points=[]
    for i in range(n_scout):
        point = ax5.scatter(scouts[i][1], scouts[i][2], function(scouts[i][1], scouts[i][2]), c="b", alpha=0.3)
        points.append(point)
    scouts.sort() # сортируем полученные ими участки по значению фитнес-функции
    points_text_5.insert(tk.END, f"0. x= {scouts[0][1]:.4f}, y= {scouts[0][2]:.4f} f= {scouts[0][0]:.4f}\n")
    canvas5.draw()
    root.update()
    time.sleep(0.01)
    best_point = []
    perspective_point = []
    for i in range(n_best): # первые n участков считаем элитными, добавляем их центральные точки в список
        best_point.append(scouts[i])
    for i in range(n_best,n_best+n_perspective): # остальные считаем перспективными
        perspective_point.append(scouts[i])
    for point in points:
        point.remove()

    for i in range(n_point):
        points = []
        best_bee = [[0] for i in range(n_best)]
        perspective_bee= [[0] for i in range(n_perspective)]
        for j in range(n_best):
            best_bee[j] = best_bee_spawn(best_point[j], n_best_bee, size) # выбираем точки среди элитных участков
        for j in range(n_perspective):
            perspective_bee[j] = perspective_bee_spawn(perspective_point[j], n_perspective_bee, size) # затем выбираем точки среди перспективных участков
        scouts = scout_spawn(n_scout) # заново отправляем разведчиков

        for j in range(n_scout): # отрисовка разведчиков
            point = ax5.scatter(scouts[j][1], scouts[j][2], function(scouts[j][1], scouts[j][2]), c="b", alpha=0.3)
            points.append(point)
        for j in range(n_best): # отрисовка элитных
            for q in range(n_best_bee):
                point = ax5.scatter(best_bee[j][q][1], best_bee[j][q][2], function(best_bee[j][q][1], best_bee[j][q][2]), c="b", alpha=0.3)
                points.append(point)
        for j in range(n_perspective): # отрисовка перспективных
            for q in range(n_perspective_bee):
                point = ax5.scatter(perspective_bee[j][q][1], perspective_bee[j][q][2], function(perspective_bee[j][q][1], perspective_bee[j][q][2]), c="b", alpha=0.3)
                points.append(point)

        b = [] # собираем все точки в 1 список и сортируем
        for j in range(n_perspective):
            b.extend(perspective_bee[j])
        for j in range(n_best):
            b.extend(best_bee[j])
        for j in range(n_scout):
            b.extend(scouts)

        b.sort()

        # заново формируем список с элитными и с перспективными точками
        best_point = []
        perspective_point = []
        for j in range(n_best):
            best_point.append(b[j])
        for j in range(n_best, n_best + n_perspective):
            perspective_point.append(b[j])

        point = ax5.scatter(best_point[0][1], best_point[0][2], function(best_point[0][1], best_point[0][2]), c="r", alpha=1)
        points.append(point)
        points_text_5.insert(tk.END, f"{i}. x= {best_point[0][1]:.4f}, y= {best_point[0][2]:.4f} f= {best_point[0][0]:.4f}\n")
        canvas5.draw()
        root.update()
        time.sleep(0.001)
        if i != n_point - 1:
            for point in points:
                point.remove()

# 6 лаба - основной вызов

points_var_6 = tk.StringVar(value=200)
anti_var_6 = tk.StringVar(value=50)
best_var_6 = tk.StringVar(value=10)
clone_var_6 = tk.StringVar(value=20)
cmut_var_6 = tk.StringVar(value=0.2)
rand_var_6 = tk.StringVar(value=10)

# Создание 5 вкладки
fig = plt.figure(figsize=(8, 6), dpi=100)
ax5 = fig.add_subplot(111, projection='3d')
canvas5 = FigureCanvasTkAgg(fig, master=tab5)
canvas5.draw()
canvas5.get_tk_widget().pack()

function_label_5 = tk.Label(tab5, text="Функция:")
function_label_5.place(x=10, y=10)
function_var_5 = tk.StringVar(value="Химмельблау")
function_dropdown_5 = tk.OptionMenu(tab5, function_var_5, "Химмельблау", "Сфера", "Функция Бута", "Розенброк", "Растригина")
function_dropdown_5.place(x=200, y=10)

points_label_5 = tk.Label(tab5, text="Количество итераций:")
points_label_5.place(x=10, y=50)
points_entry_5 = tk.Entry(tab5, textvariable=points_var_5)
points_entry_5.place(x=200, y=50)

scout_label_5 = tk.Label(tab5, text="Количество разведчиков:")
scout_label_5.place(x=10, y=90)
scout_entry_5 = tk.Entry(tab5, textvariable=scout_var_5)
scout_entry_5.place(x=200, y=90)

perspective_bee_label_5 = tk.Label(tab5, text="Пчёл на перспективном участке:")
perspective_bee_label_5.place(x=10, y=130)
perspective_bee_entry_5 = tk.Entry(tab5, textvariable=perspective_bee_var_5)
perspective_bee_entry_5.place(x=200, y=130)

best_bee_label_5 = tk.Label(tab5, text="Пчел на лучшем участке:")
best_bee_label_5.place(x=10, y=170)
best_bee_entry_5 = tk.Entry(tab5, textvariable=best_bee_var_5)
best_bee_entry_5.place(x=200, y=170)

perspective_label_5 = tk.Label(tab5, text="Перспективных участков:")
perspective_label_5.place(x=10, y=210)
perspective_entry_5 = tk.Entry(tab5, textvariable=perspective_var_5)
perspective_entry_5.place(x=200, y=210)

best_label_5 = tk.Label(tab5,text="Лучших участков:")
best_label_5.place(x=10, y=250)
best_entry_5 = tk.Entry(tab5, textvariable=best_var_5)
best_entry_5.place(x=200, y=250)

size_label_5 = tk.Label(tab5,text="Размер участков:")
size_label_5.place(x=10, y=290)
size_entry_5 = tk.Entry(tab5, textvariable=size_var_5)
size_entry_5.place(x=200, y=290)

visualize_button_5 = tk.Button(tab5, text="Визуализировать", command=visualize_5)
visualize_button_5.place(x=100, y=350)

points_text_5 = tk.Text(tab5, height=10, width=40)
points_text_5.place(x=10, y=380)

# Запуск GUI
root.mainloop()
