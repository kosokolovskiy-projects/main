import tkinter as tk
from tkinter import ttk, messagebox

from extra_files.example_data import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from widgets_folder.create_elements import Create_Elements

matplotlib_axes_logger.setLevel('ERROR')




class Number_Elements(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self["style"] = "Main_Screen.TFrame"
        self.connection_str = []
        self.controller = controller
        self.number_elements = tk.StringVar()
        self.help_label = ttk.Label(self, text="Temp")




    def check_input(self):
        if self.number_elements.get() == '':
            messagebox.showinfo(title="Error", message="Please, enter the number of elements")
        elif self.controller.example and int(self.number_elements.get()) != 6:
            messagebox.showerror(title='Error', message="You've entered the wrong number of elements for example mode")
        else:
            self.create_input_for_elements()
            self.help_label.destroy()

    def define_number_elements(self):
        from widgets_folder.force_screen import Force_Screen

        lst = (0, 1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(lst, weight=1)

        self.controller.show_frame(Number_Elements)

        for widgets in self.winfo_children():
            widgets.destroy()

        self.text_announce = ttk.Label(self, text="Enter the number of Elements: ", style="Text_header.TLabel")
        self.text_announce.grid(column=0, row=0, padx=7, pady=7, sticky="W", columnspan=2)

        self.entry_number_elements = ttk.Entry(self, width=10, textvariable=self.number_elements)
        self.entry_number_elements.grid(row=0, column=3, columnspan=1, padx=7, pady=7, sticky="E")
        self.entry_number_elements.focus()

        # EXAMPLE
        if self.controller.example:
            self.number_elements.set(str(6))
        # EXAMPLE

        self.prev_button = ttk.Button(self, text="Go back", command=lambda: self.controller.show_frame(Force_Screen), style="button_main.TButton")
        self.prev_button.grid(column=0, row=1, columnspan=1, sticky="W", padx=7, pady=7)

        self.calculate_button = ttk.Button(self, text="Create Elements", command=self.check_input, style="button_main.TButton")
        self.calculate_button.grid(column=3, row=1, columnspan=2, padx=7, pady=7, sticky="E")

        if self.controller.example:
            self.help_label = ttk.Label(self, text="*Since you are in the example mode, please enter 6",
                                        style="Text_add.TLabel")
            self.help_label.grid(column=0, row=4, columnspan=4, sticky='W')


    def create_input_for_elements(self):
        from widgets_folder.force_screen import Force_Screen

        self.text_announce.destroy()
        self.text_announce = ttk.Label(self, text=f"Connections betweeen elements: {self.number_elements.get()}",
                                       style="Text_header.TLabel")
        self.text_announce.grid(column=0, row=0, padx=7, pady=7, ipadx=7, ipady=7,  columnspan=6, sticky="W")
        self.entry_number_elements.destroy()

        for i in range(int(self.number_elements.get())):
            temp_1 = f"element_temp_{i + 1}_1"
            temp_2 = f"element_temp_{i + 1}_2"
            setattr(self, temp_1, tk.StringVar())
            setattr(self, temp_2, tk.StringVar())

            ####### EXAMPLE ########
            if self.controller.example:
                getattr(self, temp_1).set(int(connections_general[i][0]))
                getattr(self, temp_2).set(int(connections_general[i][1]))
            ####### EXAMPLE ########

            element_name = ttk.Label(self, text=("Element " + str(i + 1)), style="Text_add.TLabel")
            element_name.grid(row=(i + 1), column=0, padx=7, pady=7)
            self.entry_number_elements = ttk.Entry(self, width=12, textvariable=getattr(self, temp_1))
            self.entry_number_elements.grid(row=(i + 1), column=1, padx=7, pady=7)
            self.entry_number_elements = ttk.Entry(self, width=12, textvariable=getattr(self, temp_2))
            self.entry_number_elements.grid(row=(i + 1), column=2, padx=7, pady=7)

        self.prev_button.destroy()
        self.calculate_button.destroy()
        self.prev_button = ttk.Button(self, text="Go back", command=lambda: self.controller.show_frame(Force_Screen), style="button_main.TButton")
        self.prev_button.grid(column=0, row=(2 * int(self.number_elements.get()) + 2), sticky="W", padx=7, pady=7,
                              columnspan=1)
        self.calculate_button = ttk.Button(self, text="Set Elements Properties", command=self.plot_maker, style="button_main.TButton")
        self.calculate_button.grid(column=1, row=(2 * int(self.number_elements.get()) + 2), padx=28, pady=7,
                                   columnspan=2, sticky='E')

    def show_again(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.define_number_elements()

    def plot_maker(self):

        x = np.array([])
        y = np.array([])
        self.connection_str = []
        for i in range(int(self.number_elements.get())):
            x = np.append(x, float(getattr(self, f"element_temp_{i + 1}_1").get()))
            y = np.append(y, float(getattr(self, f"element_temp_{i + 1}_2").get()))
            self.connection_str.append((f"node_{int(x[i])}", f"node_{int(y[i])}"))
        self.controller.connection_str = self.connection_str
        self.controller.show_frame(Create_Elements)
        self.controller.frames[Create_Elements].test_func()