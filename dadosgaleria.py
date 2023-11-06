import importlib.util
import os
import sys
from os.path import isfile, join
from pathlib import Path
import flet as ft
class ControlGroup:
    def __init__(self, name, label, icon, selected_icon):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon
        self.grid_items = []
class GalleryData:
    def __init__(self):
        pass#self.import_modules()
    destinations_list = [
        ControlGroup(
            name="Membros directivos",
            label="Membros directivos",
            icon=ft.icons.GRID_VIEW,
            selected_icon=ft.icons.GRID_VIEW_SHARP,
        ),
        ControlGroup(
            name="navigation",
            label="Navigation",
            icon=ft.icons.MENU_SHARP,
            selected_icon=ft.icons.MENU_SHARP,
        ),
        ControlGroup(
            name="displays",
            label="Displays",
            icon=ft.icons.INFO_OUTLINED,
            selected_icon=ft.icons.INFO_SHARP,
        ),
        ControlGroup(
            name="buttons",
            label="Buttons",
            icon=ft.icons.SMART_BUTTON_SHARP,
            selected_icon=ft.icons.SMART_BUTTON_SHARP,
        ),
        ControlGroup(
            name="input",
            label="Input",
            icon=ft.icons.INPUT_SHARP,
            selected_icon=ft.icons.INPUT_OUTLINED,
        ),
        ControlGroup(
            name="dialogs",
            label="Dialogs",
            icon=ft.icons.MESSAGE_OUTLINED,
            selected_icon=ft.icons.MESSAGE_SHARP,
        ),
        ControlGroup(
            name="charts",
            label="Charts",
            icon=ft.icons.INSERT_CHART_OUTLINED,
            selected_icon=ft.icons.INSERT_CHART_SHARP,
        ),
        ControlGroup(
            name="animations",
            label="Animations",
            icon=ft.icons.ANIMATION_SHARP,
            selected_icon=ft.icons.ANIMATION_SHARP,
        ),
        ControlGroup(
            name="utility",
            label="Utility",
            icon=ft.icons.PAN_TOOL_OUTLINED,
            selected_icon=ft.icons.PAN_TOOL_SHARP,
        ),
        ControlGroup(
            name="colors",
            label="Colors",
            icon=ft.icons.FORMAT_PAINT_OUTLINED,
            selected_icon=ft.icons.FORMAT_PAINT_SHARP,
        ),
        ControlGroup(
            name="contrib",
            label="Contrib",
            icon=ft.icons.MY_LIBRARY_ADD_OUTLINED,
            selected_icon=ft.icons.LIBRARY_ADD_SHARP,
        ),
    ]
