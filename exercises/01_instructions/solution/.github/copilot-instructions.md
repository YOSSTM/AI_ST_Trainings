# VirtualBoard Simulator — Copilot Instructions

## Context

This is a **Python 3 web application** — a virtual embedded-board training simulator.

- **UI framework:** Streamlit (`streamlit>=1.32`)
- **Charts:** Plotly (`plotly.graph_objects`)
- **Custom components:** `streamlit.components.v1.html()`
- **No C, no HAL, no embedded toolchain** — pure Python

---

## Project Structure

```
simulator/
├── app.py                  — Streamlit entry point, layout, mode selector
├── board/
│   ├── gpio.py             — render_led_panel(leds: list) -> str (HTML)
│   ├── uart.py             — render_uart_console(uart_data: dict) -> str (HTML)
│   ├── sensor.py           — make_sensor_chart(sensor_data: dict) -> go.Figure
│   └── fsm.py              — make_fsm_diagram(fsm_data: dict) -> go.Figure
exercises/
└── exNN.py                 — EXERCISE dict + _validate() function
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|--------|
| Functions | `snake_case` | `render_led_panel`, `make_sensor_chart` |
| Classes | `PascalCase` | `BoardState`, `ExerciseConfig` |
| Constants | `UPPER_SNAKE_CASE` | `BOARD_BROKEN`, `BOARD_FIXED` |
| Modules | `lowercase` | `gpio`, `uart`, `sensor`, `fsm` |
| Private helpers | `_leading_underscore` | `_validate`, `_chip_class` |

---

## Board Module Interface

Every board module follows one of two patterns:

```python
# Pattern A — returns HTML string (rendered with st.components.v1.html)
def render_led_panel(leds: list) -> str:
    """leds: list of dicts with keys: id, color, on, blink"""
    ...

# Pattern B — returns Plotly figure (rendered with st.plotly_chart)
def make_sensor_chart(sensor_data: dict) -> go.Figure:
    """sensor_data keys: temp_values, adc_values, label"""
    ...
```

---

## Exercise Module Pattern

Each `exNN.py` must export an `EXERCISE` dict with:
```python
EXERCISE = {
    "title":        str,
    "concept":      str,
    "mission":      str,           # markdown shown in the left panel
    "problem":      str,           # one-line error description
    "hints":        list[str],
    "files_to_edit": list[str],
    "validate":     callable,      # returns (bool, str)
    "board_broken": dict,          # board state when broken
    "board_fixed":  dict,          # board state after fix
    "explanation":  str,           # markdown shown in correction view
}
```

---

## Sensor Calibration (TMP36, 12-bit ADC, Vref=3.3V)

```python
def convert_adc_to_temperature(adc_raw: int, vref: float = 3.3, bits: int = 12) -> float:
    voltage = (adc_raw / (2**bits - 1)) * vref
    temp_c  = (voltage - 0.5) / 0.01
    return round(temp_c, 1) if -40 <= temp_c <= 125 else float('nan')
```

---

## Streamlit Patterns

- Use `st.markdown(..., unsafe_allow_html=True)` for custom HTML panels
- Use `st.columns([1, 2])` for mission/simulator split layout
- Use `st.session_state` for persistent validation state across reruns
- Always call `st.rerun()` after mutating `st.session_state`
- Use `st.plotly_chart(..., use_container_width=True, config={"displayModeBar": False})`

---

## FSM Architecture (Python)

State machine data is a dict — no classes needed:
```python
fsm_data = {
    "states":      ["BOOT", "INIT", "IDLE", "RUNNING", "ERROR", "RESET"],
    "current":     "RUNNING",
    "transitions": [("BOOT", "INIT"), ("INIT", "IDLE"), ...],
}
```
Passed to `make_fsm_diagram(fsm_data)` in `simulator/board/fsm.py`.

---

## Error Handling

- Board module functions never raise — return safe fallback (empty HTML / empty Figure)
- Validation functions always return `(bool, str)` — never raise
- Log anomalies in `uart_data["messages"]` with `[ERROR]` prefix
