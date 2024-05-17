import tkinter
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Combobox, Notebook, Style

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.optimize import differential_evolution

from lab3.core import trigger, getFunc1


def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0, axis=0)


def make_data_lab_3():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)

    x_grid, y_grid = np.meshgrid(x, y)

    z = rosenbrock(np.array([x_grid, y_grid]))
    return x_grid, y_grid, z


def main():
    window = Tk()

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()

    window.geometry("%dx%d" % (width, height))

    window.title("SEARCH OPTIMISATION METHODS")

    fig = plt.figure(figsize=(11, 11))
    fig.add_subplot(projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

    style = Style()

    style.theme_create("dummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "#808080"},
            "map": {"background": [("selected", "FFFF00")],
                    "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_use("dummy")

    tab_control = Notebook(window)

    def draw_lab_3():
        fig.clf()

        x, y, z = make_data_lab_3()

        if combo_tab_3.get() == "Min":
            min_max = True
        else:
            min_max = False

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.3, cmap="inferno")
        canvas.draw()

        result = trigger()

        canvas.draw()
        window.update()

        # Эти 4 строки ниже это считай удалить точку/точки
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        for item in result:
            x = item.get("data")[0]
            y = item.get("data")[1]
            ax.scatter(x, y, getFunc1()[0](x, y), c="red")

            txt_tab_1.insert(INSERT,
                             f"{item.get('generation')}) ({round(x, 3)})({round(y, 3)}) = {getFunc1()[0](x, y)}\n")

        resultForRef = differential_evolution(rosenbrock, [(-5, 5), (-5, 5)])

        ax.scatter(resultForRef.x[0], resultForRef.x[1], resultForRef.fun, c="blue")

        txt_tab_1.insert(INSERT,
                         f"{1}) ({round(resultForRef.x[0], 2)})({round(resultForRef.x[1], 2)}) = {round(resultForRef.fun, 4)}\n")

        canvas.draw()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        window.update()

        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_3():
        txt_tab_1.delete(1.0, END)

    tab_1 = Frame(tab_control)
    tab_control.add(tab_1, text="LAB_1")

    main_f_tab_1 = LabelFrame(tab_1, text="Parameters")
    left_f_tab_1 = Frame(main_f_tab_1)
    right_f_tab_1 = Frame(main_f_tab_1)
    txt_f_tab_1 = LabelFrame(tab_1, text="Execution and results")

    lbl_5_tab_1 = Label(tab_1, text="Лаба 3")

    txt_tab_1 = scrolledtext.ScrolledText(txt_f_tab_1)
    btn_del_tab_1 = Button(tab_1, text="Clear", command=delete_lab_3, foreground="black", background="grey")
    btn_tab_1 = Button(tab_1, text="Execute", foreground="black", background="yellow", command=draw_lab_3)

    lbl_5_tab_1.pack(side=TOP, padx=5, pady=5)
    main_f_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_1.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_1.pack(side=RIGHT, fill=BOTH, expand=True)

    txt_tab_1.pack(padx=5, pady=5, fill=BOTH, expand=True)

    combo_tab_3 = Combobox(right_f_tab_1)
    combo_tab_3['values'] = ("Min", "Max")
    combo_tab_3.set("Min")

    btn_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    tab_control.pack(side=RIGHT, fill=BOTH, expand=True)
    window.mainloop()

    window.mainloop()


if __name__ == '__main__':
    main()
