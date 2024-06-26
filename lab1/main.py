import tkinter
import time
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Combobox, Notebook, Style

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from lab1.grad import make_data_lab_1, funct_consider


def main():
    window = Tk()

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()

    window.geometry("%dx%d" % (width, height))

    window.title("SEARCH OPTIMISATION METHODS")

    fig = plt.figure(figsize=(12, 12))
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

    # Лаба 1

    def display_lab_1():
        fig.clf()

        x, y, z = make_data_lab_1()

        print(x,y,z)

        ax = fig.add_subplot(projection='3d')

        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        res_x = txt_1_tab_1.get()
        res_y = txt_2_tab_1.get()
        res_step = txt_3_tab_1.get()
        res_iterations = txt_4_tab_1.get()

        x_cs, y_cs, z_cs = funct_consider(float(res_x), float(res_y), float(res_step), int(res_iterations))

        for i in range(len(x_cs)):
            if i < (len(x_cs) - 1):
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="black", s=1, marker="s")
            else:
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="red")

            canvas.draw()
            txt_tab_1.insert(INSERT, f"{i}) ({round(x_cs[i], 2)})({round(y_cs[i], 2)}) = {z_cs[i]}\n")

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            window.update()
            delay = txt_5_tab_1.get()
            time.sleep(float(delay))

        messagebox.showinfo('Message', 'Completed')

    def delete_lab_1():
        txt_tab_1.delete(1.0, END)

    tab_1 = Frame(tab_control)
    tab_control.add(tab_1, text="LAB_1")

    main_f_tab_1 = LabelFrame(tab_1, text="Parameters")
    left_f_tab_1 = Frame(main_f_tab_1)
    right_f_tab_1 = Frame(main_f_tab_1)
    txt_f_tab_1 = LabelFrame(tab_1, text="Execution and results")

    lbl_1_tab_1 = Label(left_f_tab_1, text="X")
    lbl_2_tab_1 = Label(left_f_tab_1, text="Y")
    lbl_3_tab_1 = Label(left_f_tab_1, text="Initial step")
    lbl_4_tab_1 = Label(left_f_tab_1, text="Iteration amount")
    lbl_5_tab_1 = Label(tab_1, text="Buta function")
    lbl_6_tab_1 = Label(left_f_tab_1, text="Delay in seconds")

    txt_1_tab_1 = Entry(right_f_tab_1)
    txt_1_tab_1.insert(0, "-1")

    txt_2_tab_1 = Entry(right_f_tab_1)
    txt_2_tab_1.insert(0, "-1")

    txt_3_tab_1 = Entry(right_f_tab_1)
    txt_3_tab_1.insert(0, "0.5")

    txt_4_tab_1 = Entry(right_f_tab_1)
    txt_4_tab_1.insert(0, "100")

    txt_5_tab_1 = Entry(right_f_tab_1)
    txt_5_tab_1.insert(0, "0.5")

    txt_tab_1 = scrolledtext.ScrolledText(txt_f_tab_1)
    btn_del_tab_1 = Button(tab_1, text="Clear", command=delete_lab_1, foreground="black", background="grey")
    btn_tab_1 = Button(tab_1, text="Execute", foreground="black", background="yellow", command=display_lab_1)

    lbl_5_tab_1.pack(side=TOP, padx=5, pady=5)
    main_f_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_1.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_1.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_1_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_2_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_3_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_4_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_6_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_3_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_4_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_5_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_1.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    tab_control.pack(side=RIGHT, fill=BOTH, expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()
