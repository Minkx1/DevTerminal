# DevTerminal

A lightweight desktop terminal application built with a `customtkinter`.

## Features

- Interactive command entry with command history navigation using `Up` and `Down` arrows
- Custom command evaluation via decorator-based callback registration
- Basic built-in commands: `cls` / `clear`, `quit` / `exit`
- Scrollable log output with a live prompt

## Usage

1. Install required dependencies from `requirements.txt`.
2. Run the app:

   ```bash
   python main.py
   ```

3. Enter commands in the input field and press `Run` or `Enter`.

## Example of usage

```python
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

app.run(__file__) # __file__ for debug-mode
```

## Notes

- The terminal keeps a command history and prevents duplicate consecutive history entries.
- The UI prompt updates to show the current working directory.
