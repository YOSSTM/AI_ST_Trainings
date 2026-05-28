---
mode: edit
description: Add a structured UART log message to the VirtualBoard Streamlit simulator
---

Add a new log message to the `uart_data` dict consumed by `render_uart_console()` in `simulator/board/uart.py`.

### `uart_data` dict structure

```python
uart_data = {
    "messages": list[str],   # log lines displayed in the UART console panel
    "baud":     int,          # baud rate shown in the console header (e.g. 115200)
}
```

### Message format

All messages follow this format:
```
[LEVEL]  text
```

| Level prefix | Color in UI | When to use |
|-------------|------------|-------------|
| `[INFO]  ` | green | Normal operation |
| `[DEBUG] ` | blue | Diagnostic detail |
| `[WARN]  ` | orange | Recoverable issue |
| `[ERROR] ` | red | Failure requiring attention |

### Function to generate

```python
def build_uart_message(level: str, text: str) -> str:
    """
    Build a formatted UART log message string.

    Args:
        level: one of 'INFO', 'DEBUG', 'WARN', 'ERROR'
        text:  message content (no newline needed)

    Returns:
        Formatted string: '[LEVEL]  text'

    Raises:
        ValueError: if level is not a valid log level
    """
    ...
```

Place in `simulator/board/uart.py`.
The `render_uart_console()` function automatically colorizes based on the prefix.
