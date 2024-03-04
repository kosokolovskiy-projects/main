import tkinter as tk
from tkinter import ttk

import numpy as np
from extra_files.example_data import *
from utils.Displacement import Displacement


class Displacement_Screen(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self["style"] = "Main_Screen.TFrame"
        self.controller = controller


        self.prev_button = ttk.Button(self, text="Go back", command=lambda: controller.show_frame(Constraint_Screen), style="button_main.TButton")
        self.prev_button.grid(column=0, row=0, columnspan=3)
        self.calculate_button = ttk.Button(self, text="Calculate", command=self.plot_maker, style="button_main.TButton")
        self.calculate_button.grid(column=3, row=0, columnspan=3)

    def create_displacement(self):
        from widgets_folder.constraint_screen import Constraint_Screen
        from widgets_folder.main_screen import Main_Screen

        lst = (1, 0)
        self.grid_columnconfigure(lst, weight=1)
        self.grid_rowconfigure(lst, weight=1)

        self.main = self.controller.frames[Main_Screen]
        displacement_label = ttk.Label(self, text="Displacement Settings", style="Text_header.TLabel")
        displacement_label.grid(row=0, column=0, columnspan=6, sticky='W')

        for i in range(1, self.main.num_coord_lines + 1):
            temp_1 = f"x_{i - 1}_1"
            temp_2 = f"x_{i - 1}_2"
            temp_3 = f"x_{i - 1}_3"
            setattr(self, temp_1, tk.StringVar())
            setattr(self, temp_2, tk.StringVar())
            setattr(self, temp_3, tk.StringVar())

            ####### EXAMPLE ########
            if self.controller.example:
                getattr(self, temp_1).set(float(displacements_general[i - 1][0]))
                getattr(self, temp_2).set(float(displacements_general[i - 1][1]))
                getattr(self, temp_3).set(float(displacements_general[i - 1][2]))

            ####### EXAMPLE ########

            label_x_1 = ttk.Label(self, text="Node " + str(i), style="Text_add.TLabel")
            entry_x_1 = ttk.Entry(self, width=10, textvariable=getattr(self, temp_1))
            entry_x_2 = ttk.Entry(self, width=10, textvariable=getattr(self, temp_2))
            entry_x_3 = ttk.Entry(self, width=10, textvariable=getattr(self, temp_3))

            label_x_1.grid(row=(2 * i), column=0, sticky="W")
            entry_x_1.grid(row=(2 * i), column=1, sticky="")
            entry_x_2.grid(row=(2 * i), column=2, sticky="")
            entry_x_3.grid(row=(2 * i), column=3, sticky="")

        self.lim = self.main.num_coord_lines
        self.prev_button.destroy()
        self.calculate_button.destroy()
        self.prev_button = ttk.Button(self, text="Go back",
                                      command=lambda: self.controller.show_frame(Constraint_Screen), style="button_main.TButton")
        self.calculate_button = ttk.Button(self, text="Set Forces", command=self.plot_maker, style="button_main.TButton")
        self.calculate_button.grid(column=2, row=self.main.num_coord_lines * 2 + 1, columnspan=2, sticky='E')
        self.prev_button.grid(column=0, row=self.main.num_coord_lines * 2 + 1, columnspan=2, sticky='W')

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=7)

    def plot_maker(self):
        from widgets_folder.force_screen import Force_Screen

        x = np.array([])
        y = np.array([])
        z = np.array([])
        for i in range(1, self.lim + 1):
            x = np.append(x, float(getattr(self, f'x_{i - 1}_1').get()))
            y = np.append(y, float(getattr(self, f'x_{i - 1}_2').get()))
            z = np.append(z, float(getattr(self, f'x_{i - 1}_3').get()))
            self.main.coord_dict[i - 1].displ = Displacement((x[i - 1], y[i - 1], z[i - 1]))

        self.controller.frames[Force_Screen].create_force()
        self.controller.show_frame(Force_Screen)