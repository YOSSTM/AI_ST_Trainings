# VirtualBoard Simulator — Copilot Instructions

## Context

Python 3 Streamlit web application — virtual embedded-board training simulator.
No C, no HAL, no embedded toolchain.

## Naming Conventions

- Functions/variables: `snake_case` (e.g. `render_led_panel`, `make_fsm_diagram`)
- Classes: `PascalCase` (e.g. `BoardState`)
- Constants/board state dicts: `UPPER_SNAKE_CASE` (e.g. `BOARD_BROKEN`, `BOARD_FIXED`)
- Private helpers: `_leading_underscore` (e.g. `_validate`)

## Architecture

The project follows a **modular board + exercise architecture**:

```
simulator/
├── app.py              — Streamlit entry point, layout, mode selector
├── board/
│   ├── gpio.py         — render_led_panel(leds: list) -> str
│   ├── uart.py         — render_uart_console(uart_data: dict) -> str
│   ├── sensor.py       — make_sensor_chart(sensor_data: dict) -> go.Figure
│   └── fsm.py          — make_fsm_diagram(fsm_data: dict) -> go.Figure
exercises/
└── exNN.py             — EXERCISE dict + _validate() callable
```

### FSM Module (`simulator/board/fsm.py`)

The FSM is **data-driven** — no class, just a dict:

```python
fsm_data = {
    "states":      list[str],        # all state names
    "current":     str,              # currently active state
    "transitions": list[tuple],      # (src: str, dst: str) pairs
}
```

Passed to `make_fsm_diagram(fsm_data)` which returns a `go.Figure`.

**Expected state sequence:**
```
BOOT → INIT → IDLE → RUNNING ⇄ IDLE
                    ↓
                  ERROR → RESET → IDLE
```

All transitions must appear in `fsm_data["transitions"]`.

### Agent Instructions

When working in agent mode on this codebase:
- Always read `simulator/board/fsm.py` first to understand the diagram renderer
- FSM state is a dict — add missing transitions directly to the `transitions` list
- The `make_fsm_diagram()` function is the **only consumer** of `fsm_data`
- Add new states to `fsm_data["states"]` list — never hardcode them in `fsm.py`
- Log state changes via the `uart_data["messages"]` list with `[INFO]  FSM: X -> Y`

## Board Modules

```python
# gpio.py
render_led_panel(leds: list) -> str          # HTML for st.components.v1.html()

# uart.py
render_uart_console(uart_data: dict) -> str  # HTML for st.components.v1.html()

# sensor.py
make_sensor_chart(sensor_data: dict) -> go.Figure

# fsm.py
make_fsm_diagram(fsm_data: dict) -> go.Figure
```

## Sensor Calibration

```python
# TMP36, 12-bit ADC, Vref=3.3V
voltage = (adc_raw / 4095.0) * 3.3
temp_c  = (voltage - 0.5) / 0.01
```
