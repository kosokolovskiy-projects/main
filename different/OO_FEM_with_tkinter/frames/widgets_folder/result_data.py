import tkinter as tk
from tkinter import ttk

import pandas as pd
from extra_files.example_data import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from utils.Structure import Structure

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




class Result_Data(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.controller = controller

        self["style"] = "Main_Screen.TFrame"
        #self.grid_columnconfigure(2, weight=1)

    def solver(self):
        # Label Frames
        self.frame_label_displ = ttk.Frame(self, style="Main_Screen.TFrame", height=10)
        self.frame_label_displ.grid(row=0, column=0, padx=7, pady=7)

        # DATA FRAME displacement
        self.frame_data_displ = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_data_displ.grid(row=1, column=0, padx=7, pady=7)

        self.viewer_displ = ttk.Treeview(self.frame_data_displ, style="Treeview",  height=3)


        # LABEL Frame force elements
        self.frame_label_force = ttk.Frame(self, style="Main_Screen.TFrame", height=10)
        self.frame_label_force.grid(row=2, column=0, padx=7, pady=7)


        # DATA FRAME forces in elements
        self.frame_data_force_element = ttk.Frame(self, style="Main_Screen.TFrame", height=10)
        self.frame_data_force_element.grid(row=3, column=0, padx=7, pady=7)

        self.viewer_force = ttk.Treeview(self.frame_data_force_element, style="Treeview",  height=3)

        # BUTTONS FRAME
        self.frame_buttons = ttk.Frame(self, style="Main_Screen.TFrame")
        self.frame_buttons.grid(row=4, column=0, padx=7, pady=7)

        self.forward_button = ttk.Button(self.frame_buttons, text="Solve", command=self.forward_button_func, style="button_main.TButton")
        self.exit_button = ttk.Button(self.frame_buttons, text="Exit", command=self.controller.destroy, style="button_main.TButton")

        self.forward_button.grid(row=0, column=0, columnspan=1, padx=7, pady=7)
        self.exit_button.grid(row=1, column=0, columnspan=2, padx=7, pady=7)


    def forward_button_func(self):
        from widgets_folder.ask_plots import Ask_Plots
        from widgets_folder.result_data import Result_Data

        self.controller.show_frame(Result_Data)
        self.solution()
        self.solver()

        self.forward_button.configure(text="Go To Plots")
        self.forward_button.configure(command=lambda: self.controller.show_frame(Ask_Plots))

        # LABELS
        label_displ = ttk.Label(self.frame_label_displ, text="Displacements", style="Text_add.TLabel")
        label_displ.grid(row=0, column=0, padx=7, pady=7)

        label_force = ttk.Label(self.frame_label_force, text="Element Forces", style="Text_add.TLabel")
        label_force.grid(row=0, column=0, padx=7, pady=7)

        self.displ_treeview()
        self.force_elements_treeview()

    def force_elements_treeview(self):
        self.clear_tree(self.viewer_force)

        df_force = pd.DataFrame.from_dict(self.controller.structure.force_elements, orient="index")

        # Set up Treeview
        headings_temp = [int(x + 1) for x in range(len(self.controller.structure.force_elements.values()))]
        df_force.insert(0, "Element", headings_temp)

        self.viewer_force["columns"] = list(df_force.columns)
        self.viewer_force["show"] = "headings"


        # Loop through column list for headers
        for column in self.viewer_force["column"]:
            self.viewer_force.heading(column, text=column)

        # Put data in Treeview
        df_rows_force = df_force.to_numpy().tolist()
        for i in range(len(df_rows_force)):
            df_rows_force[i][0] = int(df_rows_force[i][0])
            df_rows_force[i][1] = float(f'{df_rows_force[i][1]:.2f}')


        for row in df_rows_force:
            self.viewer_force.insert("", "end", values=row)

        self.viewer_force.column(f'Element', width=110, anchor='center')
        self.viewer_force.column(f'0', width=320, anchor='center')
        self.viewer_force.heading('0', text='Force')


        # Add Scroll
        scroll_force = tk.Scrollbar(self.frame_data_force_element)
        scroll_force.grid(row=0, column=1, sticky='NS', padx=7, pady=7)

        self.viewer_force.config(yscrollcommand=scroll_force.set)
        scroll_force.config(command=self.viewer_force.yview)

        self.viewer_force.grid(row=0, column=0, padx=7, pady=7)


    def displ_treeview(self):
        df_displ = pd.DataFrame(columns=["Node ", f'x{dict_elements[1]}', f'x{dict_elements[2]}', f'x{dict_elements[3]}'])
        for idx, key_value in enumerate(self.controller.nodes_dict.items()):
            df_displ.loc[idx] = [f'{idx + 1}'] + [f'{key_value[1].displ.displacement[0]:.6f}',
                                                       f'{key_value[1].displ.displacement[1]:.6f}',
                                                       f'{key_value[1].displ.displacement[2]:.6f}']
            df_displ = df_displ.rename(index={idx: f'Node{dict_elements[idx + 1]}'})

        self.clear_tree(self.viewer_displ)

        # Set up Treeview
        self.viewer_displ["columns"] = list(df_displ.columns)
        self.viewer_displ["show"] = "headings"

        # Loop through column list for headers
        for column in self.viewer_displ["column"]:
            self.viewer_displ.heading(column, text=column)

        # Put data in Treeview
        df_rows_displ = df_displ.to_numpy().tolist()
        for row in df_rows_displ:
            self.viewer_displ.insert("", "end", values=row)

        for i in range(len(self.controller.nodes_dict.values()) + 1):
            self.viewer_displ.column(f'#{i}', width=110, anchor='center')


        # Add Scroll
        scroll_displ = tk.Scrollbar(self.frame_data_displ)
        scroll_displ.grid(row=0, column=1, sticky='NS', padx=7, pady=7)

        self.viewer_displ.config(yscrollcommand=scroll_displ.set)
        scroll_displ.config(command=self.viewer_displ.yview)

        self.viewer_displ.grid(row=0, column=0, padx=7, pady=7)

    # TRY THE SOLUTION
    def solution(self):
        self.controller.structure = Structure(self.controller.connection_str, *self.controller.elements_lst)

        for one_connect in self.controller.connection_str:
            self.controller.structure.add_element(one_connect)

        self.controller.structure.create_connections_nodes()


        self.controller.structure.create_r0()

        for i in range(1):
            if i == 0:
                self.controller.structure.create_global_matrix()
                self.controller.structure.solution()
                self.controller.structure.print_results()

    def clear_tree(self, viewer):
        viewer.delete(*viewer.get_children())


