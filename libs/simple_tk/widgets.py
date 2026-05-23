# Made by Minkx1
# This file contains widgets for STk

from .core import ctk, WidgetMixin, BindVar, ParentManager
from tkinter import messagebox

class Spacer(WidgetMixin, ctk.CTkFrame):
    """Invsible block for creating space"""
    def __init__(self, width=0, height=0, **kwargs):
        super().__init__(width=width, height=height, fg_color="transparent", **kwargs)

class Button(WidgetMixin, ctk.CTkButton):
    def __init__(self, text, command=None, **kwargs):
        super().__init__(text=text, command=command, **kwargs)

class Label(WidgetMixin, ctk.CTkLabel):
    def __init__(self, text="", bind=None, **kwargs):
        if bind and isinstance(bind, BindVar):
            super().__init__(textvariable=bind._tk_var, **kwargs)
        else:
            super().__init__(text=text, **kwargs)

class Entry(WidgetMixin, ctk.CTkEntry):
    def __init__(self, placeholder="", **kwargs):
        super().__init__(placeholder_text=placeholder, **kwargs)

class TextBox(WidgetMixin, ctk.CTkTextbox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CheckBox(WidgetMixin, ctk.CTkCheckBox):
    def __init__(self, text="Check", bind=None, **kwargs):
        if bind and isinstance(bind, BindVar):
            super().__init__(text=text, variable=bind._tk_var, onvalue="True", offvalue="False", **kwargs)
        else:
            super().__init__(text=text, **kwargs)
    
class Switch(WidgetMixin, ctk.CTkSwitch):
    def __init__(self, text="Switch", bind=None, **kwargs):
        if bind and isinstance(bind, BindVar):
            super().__init__(text=text, variable=bind._tk_var, onvalue="True", offvalue="False", **kwargs)
        else:
            super().__init__(text=text, **kwargs)

class Slider(WidgetMixin, ctk.CTkSlider):
    def __init__(self, from_=0, to=100, bind=None, **kwargs):
        if bind and isinstance(bind, BindVar):
            super().__init__(from_=from_, to=to, variable=bind._tk_var, **kwargs)
        else:
            super().__init__(from_=from_, to=to, **kwargs)

class ProgressBar(WidgetMixin, ctk.CTkProgressBar):
    def __init__(self, bind=None, **kwargs):
        if bind and isinstance(bind, BindVar):
            super().__init__(variable=bind._tk_var, **kwargs)
        else:
            super().__init__(**kwargs)

class RadioButton(WidgetMixin, ctk.CTkRadioButton):
    def __init__(self, text, value, group, **kwargs):
        """ group must be RadioGroup object """
        super().__init__(text=text, value=value, variable=group.var, **kwargs)

class ComboBox(WidgetMixin, ctk.CTkComboBox):
    def __init__(self, options: list, command=None, **kwargs):
        super().__init__(values=options, command=command, **kwargs)

class OptionBox(WidgetMixin, ctk.CTkOptionMenu):
    def __init__(self, options: list, command=None, **kwargs):
        super().__init__(values=options, command=command, **kwargs)


class Tabview(WidgetMixin, ctk.CTkTabview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_tab(self, name):
        tab_object = self.add(name)
        return _TabContext(tab_object)

class _TabContext:
    """ Helping class """
    def __init__(self, tab_obj):
        self.tab_obj = tab_obj
        
    def __enter__(self):
        ParentManager.push_parent(self.tab_obj)
        return self.tab_obj
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        ParentManager.pop_parent()

class Image(WidgetMixin, ctk.CTkLabel):
    def __init__(self, path: str, size: tuple[int, int] = (100, 100), **kwargs):
        from PIL import Image as PILImage
        img_data = PILImage.open(path)
        self.ctk_image = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=size)
        
        super().__init__(text="", image=self.ctk_image, **kwargs)
    
    def update_image(self, new_path: str):
        from PIL import Image as PILImage
        img_data = PILImage.open(new_path)
        self.ctk_image.configure(light_image=img_data, dark_image=img_data)

class SegmentedButton(WidgetMixin, ctk.CTkSegmentedButton):
    def __init__(self, options: list, command=None, **kwargs):
        super().__init__(values=options, command=command, **kwargs)

class Notify:
    @staticmethod
    def info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def ask(title, message) -> bool:
        return messagebox.askyesno(title, message)