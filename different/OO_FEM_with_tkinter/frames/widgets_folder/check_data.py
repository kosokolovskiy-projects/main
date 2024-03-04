import tkinter as tk
from tkinter import ttk

import pandas as pd
from extra_files.example_data import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger

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




class Check_Data(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.controller = controller

        self["style"] = "Main_Screen.TFrame"


        # Label Frames
        self.frame_label_displ = ttk.Frame(self, style="Main_Screen.TFrame", height=10)
        self.frame_label_constr = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_label_force = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_label_displ.grid(row=0, column=0, padx=7, pady=7)
        self.frame_label_constr.grid(row=2, column=0, padx=7, pady=7)
        self.frame_label_force.grid(row=4, column=0, padx=7, pady=7)

        # DATA FRAME displ
        self.frame_data_displ = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_data_constr = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_data_force = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_data_displ.grid(row=1, column=0, padx=7, pady=7)
        self.frame_data_constr.grid(row=3, column=0, padx=7, pady=7)
        self.frame_data_force.grid(row=5, column=0, padx=7, pady=7)


        self.viewer_displ = ttk.Treeview(self.frame_data_displ, style="Treeview", height=3)
        self.viewer_constr = ttk.Treeview(self.frame_data_constr, style="Treeview", height=3)
        self.viewer_force = ttk.Treeview(self.frame_data_force, style="Treeview", height=3)
        # self.viewer_1.place()

        # BUTTONS FRAME
        self.frame_buttons = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_buttons.grid(row=6, column=0, padx=7, pady=7)
        self.grid_columnconfigure(6, weight=1)

        self.back_button = ttk.Button(self.frame_buttons, text="Go Back",
                                      command=lambda: self.controller.show_frame(Create_Elements), style="button_main.TButton")

        self.back_button.grid(row=0, column=0, columnspan=2, padx=7, pady=7)

    def validate_button_func(self):
        self.controller.show_frame(Check_Data)

        self.forward_button = ttk.Button(self.frame_buttons, text="Solve",
                                         command=self.forward_button_func , style="button_main.TButton")
        self.forward_button.grid(row=0, column=1, columnspan=1, padx=7, pady=7)

        # Labels
        label_displ = ttk.Label(self.frame_label_displ, text="Displacements", style="Text_add.TLabel")
        label_constr = ttk.Label(self.frame_label_constr, text="Constraints", style="Text_add.TLabel")
        label_force = ttk.Label(self.frame_label_force, text="Forces", style="Text_add.TLabel")
        label_displ.grid(row=0, column=0, padx=7, pady=7)
        label_constr.grid(row=0, column=0, padx=7, pady=7)
        label_force.grid(row=0, column=0, padx=7, pady=7)

        df_force = pd.DataFrame(columns=["Node ", f'x{dict_elements[1]}', f'x{dict_elements[2]}', f'x{dict_elements[3]}'])
        df_displ = pd.DataFrame(columns=["Node ", f'x{dict_elements[1]}', f'x{dict_elements[2]}', f'x{dict_elements[3]}'])
        df_constr = pd.DataFrame(columns=["Node ", f'x{dict_elements[1]}', f'x{dict_elements[2]}', f'x{dict_elements[3]}'])
        for idx, key_value in enumerate(self.controller.nodes_dict.items()):
            df_displ.loc[idx] = [f'{idx + 1}'] + [key_value[1].displ.displacement[0],
                                                       key_value[1].displ.displacement[1],
                                                       key_value[1].displ.displacement[2]]
            df_constr.loc[idx] = [f'{idx + 1}'] + [key_value[1].constr[0], key_value[1].constr[1],
                                                        key_value[1].constr[2]]
            df_force.loc[idx] = [f'{idx + 1}'] + [key_value[1].force[0], key_value[1].force[1],
                                                       key_value[1].force[2]]
            df_force = df_force.rename(index={idx: f'Node {idx + 1}'})
            df_constr = df_constr.rename(index={idx: f'Node {idx + 1}'})
            df_displ = df_displ.rename(index={idx: f'Node {idx + 1}'})

        names = ("Displacement", "Constraints", "Forces")

        self.clear_tree(self.viewer_displ)
        self.clear_tree(self.viewer_constr)
        self.clear_tree(self.viewer_force)

        # Set up Treeview
        self.viewer_displ["columns"] = list(df_displ.columns)
        self.viewer_constr["columns"] = list(df_constr.columns)
        self.viewer_force["columns"] = list(df_force.columns)
        self.viewer_displ["show"] = "headings"
        self.viewer_constr["show"] = "headings"
        self.viewer_force["show"] = "headings"

        # Loop through column list for headers
        for column in self.viewer_displ["column"]:
            self.viewer_displ.heading(column, text=column)
        for column in self.viewer_constr["column"]:
            self.viewer_constr.heading(column, text=column)
        for column in self.viewer_force["column"]:
            self.viewer_force.heading(column, text=column)

        # Put data in Treeview
        df_rows_displ = df_displ.to_numpy().tolist()
        for row in df_rows_displ:
            self.viewer_displ.insert("", "end", values=row)
        df_rows_constr = df_constr.to_numpy().tolist()
        for row in df_rows_constr:
            self.viewer_constr.insert("", "end", values=row)
        df_rows_force = df_force.to_numpy().tolist()
        for row in df_rows_force:
            self.viewer_force.insert("", "end", values=row)

        for i in range(len(self.controller.nodes_dict.values()) + 1):
            self.viewer_displ.column(f'#{i}', width=100, anchor='center')
            self.viewer_constr.column(f'#{i}', width=100, anchor='center')
            self.viewer_force.column(f'#{i}', width=100, anchor='center')

        # Add Scroll
        scroll_displ = tk.Scrollbar(self.frame_data_displ)
        scroll_displ.grid(row=0, column=1, sticky='NS', padx=7, pady=7)

        self.viewer_displ.config(yscrollcommand=scroll_displ.set)
        scroll_displ.config(command=self.viewer_displ.yview)

        scroll_constr = tk.Scrollbar(self.frame_data_constr)
        scroll_constr.grid(row=0, column=1, sticky='NS', padx=7, pady=7)

        self.viewer_constr.config(yscrollcommand=scroll_constr.set)
        scroll_constr.config(command=self.viewer_constr.yview)

        scroll_force = tk.Scrollbar(self.frame_data_force)
        scroll_force.grid(row=0, column=1, sticky='NS', padx=7, pady=7)

        self.viewer_force.config(yscrollcommand=scroll_force.set)
        scroll_force.config(command=self.viewer_force.yview)

        self.viewer_displ.grid(row=0, column=0, padx=7, pady=7)
        self.viewer_constr.grid(row=0, column=0, padx=7, pady=7)
        self.viewer_force.grid(row=0, column=0, padx=7, pady=7)

    def forward_button_func(self):
        from widgets_folder.result_data import Result_Data

        #self.controller.frames[Result_Data].solver()
        for widget in self.winfo_children():
            widget.destroy()
        self.controller.frames[Result_Data].forward_button_func()
        self.configure(width=200, height=100)
        self.controller.show_frame(Result_Data)

    def clear_tree(self, viewer):
        viewer.delete(*viewer.get_children())
