import flet as ft

class MyCheckbox(ft.Checkbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked = False

    def is_checked(self):
        return self.checked

    def set_checked(self, checked):
        self.checked = checked