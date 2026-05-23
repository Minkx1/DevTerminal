from libs.simple_tk import Window, VBox, HBox, TextBox, Entry, Button, Label
import customtkinter as CTk
import os
import threading
import shlex

SCREEN_W, SCREEN_H = 900, 500
VERSION = "1.0"
NAME = "DevTerminal"
AUTHOR = "Minkx1"

class Terminal(Window):
    def __init__(self, title=NAME, size=(SCREEN_W, SCREEN_H), eval_cmd=None):
        self.current_path = os.getcwd()
        self.history = []
        self.history_idx = -1
        self._eval_callback = eval_cmd
        
        self.header = f"{title} [V{VERSION}] by {AUTHOR}\n\n{self.current_path}>"
        super().__init__(title, size)

    def cmd_eval(self, func):
        """ Decorator for registering a command evaluation function. The function should accept a list of command parts (command and arguments) and return a string result or None. """
        self._eval_callback = func
        return func

    def build(self):
        with VBox(fg_color="transparent", padx=10, pady=10):
            self.txt = TextBox(height=SCREEN_H - 100, fill="both", expand=True)
            self.txt.insert("0.0", self.header)
            self.txt.configure(state="disabled")

            with HBox(fg_color="transparent", expand=False, height=45, fill="both", pady=(10, 0)):
                # self.lbl_path = Label(text=self._get_prompt(), width=130, anchor="e")
                self.entry = Entry("Enter command...", height=30, fill="x", expand=True)
                self.btn_submit = Button("Run", command=self.execute, width=75)

        self._bind_events()

    def _bind_events(self):
        self.entry.bind("<Return>", lambda e: self.execute())
        self.entry.bind("<Up>", self._history_up)
        self.entry.bind("<Down>", self._history_down)

    def _history_up(self, event):
        if self.history:
            self.history_idx = min(self.history_idx + 1, len(self.history) - 1)
            self._update_entry_from_history()
        return "break"

    def _history_down(self, event):
        if self.history_idx > 0:
            self.history_idx -= 1
            self._update_entry_from_history()
        else:
            self.history_idx = -1
            self.entry.delete(0, "end")
        return "break"

    def _update_entry_from_history(self):
        self.entry.delete(0, "end")
        cmd = self.history[-(self.history_idx + 1)]
        self.entry.insert(0, cmd)

    def log(self, text):
        """Logging info into terminal."""
        def append():
            self.txt.configure(state="normal")
            self.txt.insert("end", text)
            self.txt.configure(state="disabled")
            self.txt.see("end")
        self.after(0, append)

    def execute(self):
        cmd = self.entry.get().strip()
        if not cmd:
            return

        if not self.history or self.history[-1] != cmd:
            self.history.append(cmd)
        self.history_idx = -1

        self.entry.delete(0, "end")
        self.log(f" {cmd}\n")

        threading.Thread(target=self._run_proc, args=(cmd,), daemon=True).start()

    def _eval_basic_cmd(self, cmd):
        match cmd[0].lower():
            case "cls" | "clear":
                self.after(0, self._clear_screen)
                return True
            case "quit" | "exit":
                self.after(0, self.destroy)
                return True

        return False

    def _run_proc(self, cmd: str):
        try:
            try:
                cmd_parts: list[str] = shlex.split(cmd)
            except ValueError:
                cmd_parts: list[str] = cmd.split()
                
            if not cmd_parts:
                return

            if not self._eval_basic_cmd(cmd_parts):
                # 2. Якщо розробник зареєстрував свій @cmd_eval, передаємо команду йому
                if self._eval_callback:
                    result = self._eval_callback(cmd_parts)
                    
                    # Якщо функція щось повернула (рядок) — друкуємо його
                    if result is not None:
                        self.log(str(result) + "\n")
                        self.log(f"\n{self.current_path}>")
                        return 
            else:
                return

        except Exception as e:
            self.log(f"Error: {e}\n")

        self.log(f"\n{self.current_path}>")

    def _clear_screen(self):
        self.txt.configure(state="normal")
        self.txt.delete("0.0", "end")
        self.txt.insert("0.0", f"{self.current_path}>")
        self.txt.configure(state="disabled")

# Example of usage
if __name__ == "__main__":
    app = Terminal("Terminal", (SCREEN_W, SCREEN_H))
    state_db = {}

    @app.cmd_eval
    def test(cmd: list[str]):
        match cmd[0].lower():
            case "echo":
                return " ".join(cmd[1:])
                
            case "set":
                if len(cmd) < 3:
                    return "Error: 'set' requires <id> and <value>"
                state_db[cmd[1]] = cmd[2]
                return f"Saved: {cmd[1]} = {cmd[2]}"
                
            case "get":
                if len(cmd) < 2:
                    return "Error: 'get' requires <id>"
                return f"{cmd[1]} -> {state_db.get(cmd[1], 'Not found')}"
                
            case _:
                return "Unknown command: " + cmd[0]

    app.run(__file__)