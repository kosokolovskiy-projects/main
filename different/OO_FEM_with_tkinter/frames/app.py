import tkinter as tk
from tkinter import ttk

from widgets_folder.constraint_screen import Constraint_Screen
from widgets_folder.main_screen import Main_Screen
from widgets_folder.displacement_screen import Displacement_Screen
from widgets_folder.force_screen import Force_Screen
from widgets_folder.create_elements import Create_Elements
from widgets_folder.number_elements import Number_Elements
from widgets_folder.check_data import Check_Data
from widgets_folder.result_data import Result_Data
from widgets_folder.ask_plots import Ask_Plots
from widgets_folder.plots_maker import Plots_Maker

from utils.Structure import Structure

COLOUR_PRIMARY = "#2e3f4f"
COLOUR_SECONDARY = "#293846"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#8095a8"
BUTTON_BACKGROUND ="#f5f7fa"
BUTTON_ACTIVE_BACKGROUND = "#ebf2ff"


class PlotMaker(tk.Tk):
    def __init__(self, example, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.example = example

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "button_main.TButton",
            background=BUTTON_BACKGROUND,
            font="Arial 12",
            bd=1
        )

        style.configure("TNotebook", background="COLOUR_LIGHT_BACKGROUND")
        style.map("TNotebook", background= [("selected", "blue")])

        style.configure("Main_Screen.TFrame", background=COLOUR_LIGHT_BACKGROUND)
        style.configure("Background.TFrame", background=COLOUR_PRIMARY)

        style.configure(
            "Text_header.TLabel",
            background=COLOUR_LIGHT_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font="Courier 18",
        )

        style.map("button_main.TButton", background=[('active', BUTTON_ACTIVE_BACKGROUND)])

        style.configure(
            "Text_add.TLabel",
            background=COLOUR_LIGHT_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font="Courier 14"
        )

        style.configure(
            "PomodoroButton.TButton",
            background=COLOUR_SECONDARY,
            foreground=COLOUR_LIGHT_TEXT,
        )

        style.configure(
            "Treeview",
            rowheight=25
        )

        style.configure(
            "Check.TCheckbutton",
            background=COLOUR_LIGHT_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font="Courier 13",
        )

        style.map(
            "PomodoroButton.TButton",
            background=[("active", COLOUR_PRIMARY), ("disabled", COLOUR_LIGHT_TEXT)]
        )

        # Main app window is a tk widget, so background is set directly
        self["background"] = COLOUR_PRIMARY

        style = ttk.Style()
        style.theme_use("clam")

        self.frames = dict()
        self.nodes_dict = {}
        self.structure = ()
        self.elements_lst = []
        self.connection_str = ()
        self.structure = Structure

        self.plot_options = {'undeformed': 0, 'deformed': 0}
        self.canvas_undeformed = None
        self.canvas_deformed = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(sticky="")

        self.all_widgets = (
            Main_Screen, Constraint_Screen, Displacement_Screen, Force_Screen, Number_Elements, Create_Elements, Check_Data, Result_Data, Ask_Plots, Plots_Maker)
        for FrameClass in self.all_widgets:
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(Main_Screen)


    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


example = True 
app = PlotMaker(example)
app.mainloop()
