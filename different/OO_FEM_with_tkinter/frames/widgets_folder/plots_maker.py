import tkinter as tk
from tkinter import ttk, messagebox

from extra_files.example_data import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

matplotlib_axes_logger.setLevel('ERROR')



class Plots_Maker(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.controller = controller

        self["style"] = "Main_Screen.TFrame"

        self.notebook_frame = ttk.Frame(self, style="Main_Screen.TFrame")


    def creation_elements(self):
        self.notebook_frame = ttk.Frame(self, style="Main_Screen.TFrame")

        self.buttons_frame = ttk.Frame(self, style="Main_Screen.TFrame")

        # BUTTONS
        self.forward_button = ttk.Button(self.buttons_frame, text="Finish", command=self.controller.destroy, style="button_main.TButton")

        self.back_button = ttk.Button(self.buttons_frame, text="Go back",
                                      command=self.go_back_button_func, style="button_main.TButton")

        self.exit_button = ttk.Button(self.buttons_frame, text="Exit", command=self.controller.destroy, style="button_main.TButton")

        self.my_notebook = ttk.Notebook(self.notebook_frame, style='TNotebook')

        for i in range(len(self.controller.plot_options.values())):
            setattr(self, f'my_notebook_page_{i + 1}', ttk.Frame(self.my_notebook))

    def check_button(self, var):
        if var == '':
            return 0
        else:
            return 1

    def go_back_button_func(self):
        from widgets_folder.ask_plots import Ask_Plots

        for item in self.notebook_frame.winfo_children():
            item.destroy()

        for widgets in self.winfo_children():
            widgets.destroy()

        self.configure(width=20, height=10)


        self.controller.frames[Ask_Plots].change_buttons()
        self.controller.show_frame(Ask_Plots)

    def plot_activation(self, undeformed_loc, deformed_loc):
        undeformed = self.check_button(undeformed_loc)
        deformed = self.check_button(deformed_loc)
        if undeformed == 1 or deformed == 1:
            self.plot_activation_final(undeformed, deformed)
        else:
            messagebox.showinfo(title="Error", message="Yoy have not chosen any Plot. Please, choose at least one.")


    def plot_activation_final(self, undeformed, deformed):

        self.creation_elements()

        self.notebook_frame.grid(row=0, column=0)
        self.buttons_frame.grid(row=1, column=0)
        self.forward_button.grid(row=0, column=1, padx=7, pady=7)
        self.back_button.grid(row=0, column=0, padx=7, pady=7)
        self.exit_button.grid(row=1, column=0, columnspan=2, padx=7, pady=7)
        self.my_notebook.grid(row=0, column=0, padx=7, pady=7)

        for i in range(len(self.controller.plot_options.values())):
            if undeformed and i == 0:
                self.my_notebook.add(getattr(self, f'my_notebook_page_{i + 1}'),
                                     text=f'{list(self.controller.plot_options.keys())[i]}')
                self.undeformed_func(getattr(self, f'my_notebook_page_{i + 1}'))
            if deformed and i == 1:
                self.my_notebook.add(getattr(self, f'my_notebook_page_{i + 1}'),
                                     text=f'{list(self.controller.plot_options.keys())[i]}')
                self.deformed_func(getattr(self, f'my_notebook_page_{i + 1}'))


        self.controller.show_frame(Plots_Maker)


    def deformed_func(self, notebook_page):
        fig_deformed = Figure(figsize=(5, 4), dpi=130)
        canvas_deformed = FigureCanvasTkAgg(fig_deformed, master=notebook_page)
        canvas_deformed.draw()
        ax_deformed = fig_deformed.add_subplot(111, projection="3d")
        self.controller.structure.visualize_deformed(fig_deformed, canvas_deformed, ax_deformed)
        toolbar_deformed = NavigationToolbar2Tk(canvas_deformed, notebook_page)
        toolbar_deformed.update()
        canvas_deformed.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def undeformed_func(self, notebook_page):
        fig_undeformed = Figure(figsize=(5, 4), dpi=130)
        canvas_undeformed = FigureCanvasTkAgg(fig_undeformed, master=notebook_page)
        canvas_undeformed.draw()
        ax_undeformed = fig_undeformed.add_subplot(111, projection="3d")
        self.controller.structure.visualize(fig_undeformed, canvas_undeformed, ax_undeformed)
        toolbar_undeformed = NavigationToolbar2Tk(canvas_undeformed, notebook_page)
        toolbar_undeformed.update()
        canvas_undeformed.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
