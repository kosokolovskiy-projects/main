import tkinter as tk
from tkinter import ttk

from extra_files.example_data import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger

matplotlib_axes_logger.setLevel('ERROR')


class Ask_Plots(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.configure(style="Main_Screen.TFrame")

        self.change_buttons()
        self.controller = controller

    def change_buttons(self):
        from widgets_folder.plots_maker import Plots_Maker
        from widgets_folder.result_data import Result_Data

        label_enter = ttk.Label(self, text="Choose the plots you want to see: ", style="Text_add.TLabel")
        label_enter.pack(side='left')
        label_enter.place(relx=0.02, rely=0.02)

        self.deformed_var = tk.StringVar()
        self.undeformed_var = tk.StringVar()

        deformed_check = ttk.Checkbutton(self, text="Deformed Structure", variable=self.deformed_var,
                                         style="Check.TCheckbutton")
        undeformed_check = ttk.Checkbutton(self, text="Undeformed Structure", variable=self.undeformed_var,
                                           style="Check.TCheckbutton")

        deformed_check.pack(side='left')
        undeformed_check.pack(side='left')
        undeformed_check.place(relx=0.1, rely=0.2)
        deformed_check.place(relx=0.1, rely=0.4)

        forward_button = ttk.Button(self, text='Create Plots', command=lambda: self.controller.frames[Plots_Maker].plot_activation(self.undeformed_var.get(), self.deformed_var.get()), style="button_main.TButton")
        forward_button.pack(side='right')
        forward_button.place(relx=0.8, rely=0.9)

        self.back_button = ttk.Button(self, text="Go To Results ", command=lambda: self.controller.show_frame(Result_Data), style="button_main.TButton")
        self.back_button.pack(side='left')
        self.back_button.place(relx=0.02, rely=0.9)