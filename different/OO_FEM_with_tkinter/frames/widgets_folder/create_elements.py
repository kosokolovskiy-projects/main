import tkinter as tk
from tkinter import ttk

import inflect
from extra_files.example_data import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from utils.Element import Element

matplotlib_axes_logger.setLevel('ERROR')

dict_elements = {
    1: u'\u2081',
    2: u'\u2082',
    3: u'\u2083',
    4: u'\u2084',
    5: u'\u2085',
    6: u'\u2086',
    7: u'\u2087',
    8: u'\u2088',
    9: u'\u2089',
}





class Create_Elements(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self["style"] = "Main_Screen.TFrame"
        self.controller = controller
        self.container = container


    def test_func(self):

        from widgets_folder.number_elements import Number_Elements

        lst = (1, 0)
        self.grid_columnconfigure(lst, weight=1)
        self.grid_rowconfigure(lst, weight=1)

        self.connection_str = self.controller.connection_str
        self.number_elements = len(self.connection_str)

        self.label_properties = ttk.Label(self, text="Enter Elements' Properties", style="Text_header.TLabel")
        self.label_properties.grid(row=0, column=0, columnspan=4, sticky="W", pady=10, padx=10, ipadx=7, ipady=7,)

        self.p = inflect.engine()

        for i in range(1, self.number_elements + 1):
            temp_E = f"E_element_{i}"
            temp_A = f"A_element_{i}"
            setattr(self, temp_E, tk.StringVar())
            setattr(self, temp_A, tk.StringVar())

            ####### EXAMPLE ########
            if self.controller.example:
                getattr(self, temp_E).set(f"{float(elements_properties_general[i - 1][0]):.1f}")
                getattr(self, temp_A).set(f"{float(elements_properties_general[i - 1][1]):.4f}")
            ####### EXAMPLE ########

            if i <= 9:
                label_x_1 = ttk.Label(self, text=f"E{dict_elements[i]}", width=3, style="Text_add.TLabel")
                label_x_2 = ttk.Label(self, text=f"A{dict_elements[i]}", width=3, style="Text_add.TLabel")
            else:
                label_x_1 = ttk.Label(self, text="E" + str(i), width=4, style="Text_add.TLabel")
                label_x_2 = ttk.Label(self, text="A" + str(i), width=4, style="Text_add.TLabel")
            entry_x_1 = ttk.Entry(self, width=15, textvariable=getattr(self, temp_E))
            entry_x_2 = ttk.Entry(self, width=15, textvariable=getattr(self, temp_A))

            label_x_1.grid(row=(i), column=0, sticky="W", padx=7, pady=7)
            label_x_2.grid(row=(i), column=2, sticky="W", padx=7, pady=7)
            entry_x_1.grid(row=(i), column=1, sticky="WE", padx=7, pady=7)
            entry_x_2.grid(row=(i), column=3, sticky="WE", padx=7, pady=7)

        self.back_button = ttk.Button(self, text="Go back", command=self.controller.frames[Number_Elements].show_again, style="button_main.TButton")
        self.back_button.grid(row=(2 * self.number_elements + 1), column=0, padx=7, pady=7, columnspan=2, sticky="W")
        self.calculate_button = ttk.Button(self, text="Check Data", command=self.plot_maker, style="button_main.TButton")
        self.calculate_button.grid(row=(2 * self.number_elements + 1), column=2, padx=7, pady=7, columnspan=2,
                                   sticky="E")

    def plot_maker(self):
        from widgets_folder.check_data import Check_Data

        x = []
        for i in range(self.number_elements):
            temp_E = f"E_element_{i + 1}"
            temp_A = f"A_element_{i + 1}"

            x.append(Element(self.controller.nodes_dict[int(self.connection_str[i][0][-1]) - 1],
                             self.controller.nodes_dict[int(self.connection_str[i][1][-1]) - 1],
                             float(getattr(self, temp_E).get()), float(getattr(self, temp_A).get())))
        self.controller.elements_lst = np.copy(x)

        self.controller.frames[Check_Data].validate_button_func()