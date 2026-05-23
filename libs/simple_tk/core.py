# Made by Minkx1
# Main file of SimpleTk, contains important classes. 

import customtkinter as ctk
import os, sys

#  PARENT MANAGEMENT 
class ParentManager():
    """ Class for managing widgets' parents for automatic register of widgets' masters."""
    parent_stack = []

    @staticmethod
    def get_current_parent():
        """Returns current last parrent."""
        if ParentManager.parent_stack:
            return ParentManager.parent_stack[-1]
        raise RuntimeError("No active container! Widgets must be created inside a Window setup.")

    @staticmethod
    def push_parent(widget):
        ParentManager.parent_stack.append(widget)
    @staticmethod
    def pop_parent():
        ParentManager.parent_stack.pop()
    
    @staticmethod
    def get_master_parent():
        if ParentManager.parent_stack:
            return ParentManager.parent_stack[0]
        raise RuntimeError("No active container! Widgets must be created inside a Window setup.")


#  BASE WINDOW 
class Window(ctk.CTk):
    def __init__(self, title:str = "SimpleTk App", size:str|tuple[int, int] = "500x500", theme:str = "dark", color_theme:str = "blue"):
        super().__init__()
        
        # setting tk&Ctk
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(color_theme)
    
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}") if isinstance(size, tuple) else self.geometry(size)
        
        self._build_ui()

    def _build_ui(self):
        ParentManager.push_parent(self) 
        self.build()

    def build(self):
        """This method is redfined by the user."""
        pass

    def run(self, debug_file=None):
        """
        debug_file: use __file__ for auto-reload when code has been changed.
        """
        if debug_file:
            self._debug_file = debug_file
            # Запам'ятовуємо час останньої зміни файлу
            try:
                self._last_mtime = os.stat(debug_file).st_mtime
            except FileNotFoundError:
                print(f"[Error]: Debug file '{debug_file}' not found.")
                return

            print(f"[DEBUG]: Watching {os.path.basename(debug_file)} for changes...")
            self._check_reload()

        self.mainloop()

    def _check_reload(self):
        """Перевіряє, чи змінився файл, і перезапускає скрипт."""
        try:
            current_mtime = os.stat(self._debug_file).st_mtime
            
            if current_mtime > self._last_mtime:
                print("\n[DEBUG] Change detected! Reloading application...\n")
                
                self.destroy() 
                
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                self.after(500, self._check_reload)
                
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[DEBUG] Error during reload check: {e}")


#  LAYOUT CONTAINERS 
class Container(ctk.CTkFrame):
    def __init__(self, **kwargs):
        parent = ParentManager.get_current_parent()
        
        fill = kwargs.pop('fill', 'both')
        expand = kwargs.pop('expand', True)
        padx = kwargs.pop('padx', 5)
        pady = kwargs.pop('pady', 5)

        super().__init__(master=parent, **kwargs)
        
        side = "left" if isinstance(parent, HBox) else "top"
        
        if "width" in kwargs or "height" in kwargs:
            self.pack_propagate(False)

        self.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)

    def __enter__(self):
        ParentManager.push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ParentManager.pop_parent()

class VBox(Container):
    """Vertical container"""
    pass

class HBox(Container):
    """Horizontal container"""
    pass

class ScrollBox(ctk.CTkScrollableFrame):
    def __init__(self, **kwargs):
        parent = ParentManager.get_current_parent()
        
        fill = kwargs.pop('fill', 'both')
        expand = kwargs.pop('expand', True)
        padx = kwargs.pop('padx', 5)
        pady = kwargs.pop('pady', 5)
        
        super().__init__(master=parent, **kwargs)
        
        side = "left" if isinstance(parent, HBox) else "top"

        if "width" in kwargs or "height" in kwargs:
            self.pack_propagate(False)
        
        self.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)

    def __enter__(self):
        ParentManager.push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ParentManager.pop_parent()

#  Widget Mixin
class WidgetMixin:
    def __init__(self, **kwargs):
        if 'master' not in kwargs:
            kwargs['master'] = ParentManager.get_current_parent()
        
        align = kwargs.pop('anchor', None) # 'start', 'center', 'end'
        padx = kwargs.pop('padx', 5)
        pady = kwargs.pop('pady', 5)
        fill = kwargs.pop('fill', None)
        expand = kwargs.pop('expand', False)

        anchor_map = {"start": "w", "center": "center", "end": "e"}
        anchor = anchor_map.get(align, None)

        super().__init__(**kwargs)
        
        parent = kwargs['master']
        side = "left" if isinstance(parent, HBox) else "top"

        self.pack(side=side, padx=padx, pady=pady, anchor=anchor, fill=fill, expand=expand) # type: ignore

#  Variable for binding
class BindVar:
    def __init__(self, value=""):
        self._tk_var = ctk.StringVar(value=str(value))
        
    @property
    def v(self): 
        return self._tk_var.get()

    @v.setter
    def v(self, new_val):
        self._tk_var.set(str(new_val))

    def set(self, value:str):
        self.v = value

    def get(self):
        return self.v

    def __str__(self):
        return str(self.v)

class IntBindVar(BindVar):
    def __init__(self, value=0):
        self._tk_var = ctk.IntVar(value=int(value))

class RadioGroup:
    """Object for grouping RadioButtons"""
    def __init__(self, value=""):
        self.var = ctk.StringVar(value=str(value))
    
    def get(self):
        return self.var.get()
    
    def set(self, val):
        self.var.set(val)
