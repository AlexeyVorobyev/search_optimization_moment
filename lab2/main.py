import tkinter
import time
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Combobox, Notebook, Style

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from lab2.utils import make_data_lab_2, kp


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

    def draw_lab_2():
        fig.clf()

        x, y, z = make_data_lab_2()

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.7, cmap="rainbow")
        canvas.draw()

        x_cs = []
        y_cs = []
        z_cs = []

        for i, point in kp(0, 0):
            x_cs.append(point[0])
            y_cs.append(point[1])
            z_cs.append(point[2])

        for i in range(len(x_cs)):
            if i < (len(x_cs) - 1):
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="black", s=1, marker="s")
            else:
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="red")

            txt_tab_1.insert(INSERT, f"{i}) ({round(x_cs[i], 2)})({round(y_cs[i], 2)}) = {round(z_cs[i], 4)}\n")
            canvas.draw()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            window.update()
            delay = txt_3_tab_1.get()
            time.sleep(float(delay))
        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_2():
        txt_tab_1.delete(1.0, END)

    tab_1 = Frame(tab_control)
    tab_control.add(tab_1, text="LAB_1")

    main_f_tab_1 = LabelFrame(tab_1, text="Parameters")
    left_f_tab_1 = Frame(main_f_tab_1)
    right_f_tab_1 = Frame(main_f_tab_1)
    txt_f_tab_1 = LabelFrame(tab_1, text="Execution and results")

    lbl_3_tab_1 = Label(left_f_tab_1, text="Delay in seconds")
    lbl_5_tab_1 = Label(tab_1, text="Buta function")

    txt_3_tab_1 = Entry(right_f_tab_1)
    txt_3_tab_1.insert(0, "0.5")

    txt_tab_1 = scrolledtext.ScrolledText(txt_f_tab_1)
    btn_del_tab_1 = Button(tab_1, text="Clear", command=delete_lab_2, foreground="black", background="grey")
    btn_tab_1 = Button(tab_1, text="Execute", foreground="black", background="yellow", command=draw_lab_2)

    lbl_5_tab_1.pack(side=TOP, padx=5, pady=5)
    main_f_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_1.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_1.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_3_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_3_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_1.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    tab_control.pack(side=RIGHT, fill=BOTH, expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()
