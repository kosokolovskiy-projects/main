import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from matplotlib.axes._axes import _log as matplotlib_axes_logger

from utils.Node import Node

from extra_files.example_data import *



matplotlib_axes_logger.setLevel('ERROR')


class Main_Screen(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)

        self["style"] = "Main_Screen.TFrame"

        self.controller = controller
        self.num_coord_lines = 2

        self.x_1_1 = tk.StringVar()
        self.x_1_2 = tk.StringVar()
        self.x_1_3 = tk.StringVar()
        self.x_2_1 = tk.StringVar()
        self.x_2_2 = tk.StringVar()
        self.x_2_3 = tk.StringVar()

        if self.controller.example:
            self.x_1_1.set(f'{float(nodes_general[0][0]):.3f}')
            self.x_1_2.set(f'{float(nodes_general[0][1]):.3f}')
            self.x_1_3.set(f'{float(nodes_general[0][2]):.3f}')
            self.x_2_1.set(f'{float(nodes_general[1][0]):.3f}')
            self.x_2_2.set(f'{float(nodes_general[1][1]):.3f}')
            self.x_2_3.set(f'{float(nodes_general[1][2]):.3f}')

        self.coord_dict = {}

        self.controller = controller

        label_main = ttk.Label(self, text="Enter Points:", style="Text_header.TLabel")
        label_main.grid(column=0, row=0, sticky="W", columnspan=6)

        # first column

        first_coordinate_label_1 = ttk.Label(self, text="x:", style="Text_add.TLabel", width=5)
        first_coordinate_label_1.grid(column=0, row=1)
        first_coordinate_entry_1 = ttk.Entry(self, width=10, textvariable=self.x_1_1)
        first_coordinate_entry_1.grid(column=1, row=1)

        first_coordinate_label_2 = ttk.Label(self, text="x:", style="Text_add.TLabel", width=5)
        first_coordinate_label_2.grid(column=0, row=2)
        first_coordinate_entry_2 = ttk.Entry(self, width=10, textvariable=self.x_2_1)
        first_coordinate_entry_2.grid(column=1, row=2)

        # second column

        second_coordinate_label_1 = ttk.Label(self, text="y:", style="Text_add.TLabel", width=5)
        second_coordinate_label_1.grid(column=2, row=1)
        second_coordinate_entry_1 = ttk.Entry(self, width=10, textvariable=self.x_1_2)
        second_coordinate_entry_1.grid(column=3, row=1)

        second_coordinate_label_2 = ttk.Label(self, text="y:", style="Text_add.TLabel", width=5)
        second_coordinate_label_2.grid(column=2, row=2)
        second_coordinate_entry_2 = ttk.Entry(self, width=10, textvariable=self.x_2_2)
        second_coordinate_entry_2.grid(column=3, row=2)

        # third column

        third_coordinate_label_1 = ttk.Label(self, text="z:", style="Text_add.TLabel", width=5)
        third_coordinate_label_1.grid(column=4, row=1)
        third_coordinate_entry_1 = ttk.Entry(self, width=10, textvariable=self.x_1_3)
        third_coordinate_entry_1.grid(column=5, row=1)

        third_coordinate_label_2 = ttk.Label(self, text="z:", style="Text_add.TLabel", width=5)
        third_coordinate_label_2.grid(column=4, row=2)
        third_coordinate_entry_2 = ttk.Entry(self, width=10, textvariable=self.x_2_3)
        third_coordinate_entry_2.grid(column=5, row=2)

        self.add_coord_button = ttk.Button(self, text="Add Coordinate", command=self.add_coord,
                                           style="button_main.TButton")
        self.add_coord_button.grid(column=0, row=self.num_coord_lines + 1, columnspan=6)

        self.next_button = ttk.Button(self, text="Set Constraints", command=self.plot_maker,
                                      style="button_main.TButton")
        self.next_button.grid(row=self.num_coord_lines + 2, column=0, columnspan=6)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=7)

    def add_coord(self):
        self.num_coord_lines += 1

        if self.num_coord_lines >= 5 and self.controller.example:
            messagebox.showinfo(title="Error", message="You are in example mode, more lines cannot be added")
            self.num_coord_lines -= 1
        try:
            temp_1 = f"x_{self.num_coord_lines}_1"
            temp_2 = f"x_{self.num_coord_lines}_2"
            temp_3 = f"x_{self.num_coord_lines}_3"
            if temp_1 not in self.__dict__.keys():
                setattr(self, temp_1, tk.StringVar())
                setattr(self, temp_2, tk.StringVar())
                setattr(self, temp_3, tk.StringVar())

            ####### EXAMPLE #########
            if self.controller.example:
                getattr(self, temp_1).set(f'{float(nodes_general[self.num_coord_lines - 1][0]):.3f}')
                getattr(self, temp_2).set(f'{float(nodes_general[self.num_coord_lines - 1][1]):.3f}')
                getattr(self, temp_3).set(f'{float(nodes_general[self.num_coord_lines - 1][2]):.3f}')
            ####### EXAMPLE #########

            temp_label_1 = ttk.Label(self, text="x:", style="Text_add.TLabel", width=5)
            temp_label_1.grid(column=0, row=self.num_coord_lines)
            temp_entry_1 = ttk.Entry(self, width=10, textvariable=getattr(self, temp_1))
            temp_entry_1.grid(column=1, row=self.num_coord_lines)

            temp_label_2 = ttk.Label(self, text="y:", style="Text_add.TLabel", width=5)
            temp_label_2.grid(column=2, row=self.num_coord_lines)
            temp_entry_2 = ttk.Entry(self, width=10, textvariable=getattr(self, temp_2))
            temp_entry_2.grid(column=3, row=self.num_coord_lines)

            temp_label_3 = ttk.Label(self, text="z:", style="Text_add.TLabel", width=5)
            temp_label_3.grid(column=4, row=self.num_coord_lines)
            temp_entry_3 = ttk.Entry(self, width=10, textvariable=getattr(self, temp_3))
            temp_entry_3.grid(column=5, row=self.num_coord_lines)

            self.add_coord_button.destroy()
            self.add_coord_button = ttk.Button(self, text="Add Coordinate", command=self.add_coord,
                                               style="button_main.TButton")
            self.add_coord_button.grid(column=0, row=self.num_coord_lines + 1, columnspan=6, padx=7, pady=7)

            self.next_button.destroy()
            self.next_button = ttk.Button(self, text="Set Constraints", command=self.plot_maker,
                                          style="button_main.TButton")
            self.next_button.grid(row=self.num_coord_lines + 2, column=0, columnspan=6)
        except:
            pass
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=7)

    def plot_maker(self):

        x = np.array([])
        y = np.array([])
        z = np.array([])
        for i in range(1, self.num_coord_lines + 1):
            x = np.append(x, float(getattr(self, f'x_{i}_1').get()))
            y = np.append(y, float(getattr(self, f'x_{i}_2').get()))
            z = np.append(z, float(getattr(self, f'x_{i}_3').get()))
            self.coord_dict[i - 1] = Node(x[i - 1], y[i - 1], z[i - 1])

        self.controller.nodes_dict = self.coord_dict

        # self.config( width=200 )

        from widgets_folder.constraint_screen import Constraint_Screen
        self.controller.frames[Constraint_Screen].create_second()
