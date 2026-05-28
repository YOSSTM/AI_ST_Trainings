---
applyTo: "simulator/**/*.py"
---

# VirtualBoard Simulator — Scoped Python Instructions
# (applies ONLY to simulator/**/*.py)

## Context

Python 3 Streamlit app — virtual embedded-board training simulator.
No C, no HAL, no embedded toolchain.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|--------|
| Functions | `snake_case` | `render_led_panel`, `make_sensor_chart` |
| Classes | `PascalCase` | `BoardState`, `ExerciseConfig` |
| Constants | `UPPER_SNAKE_CASE` | `BOARD_BROKEN`, `BOARD_FIXED` |
| Private helpers | `_leading_underscore` | `_validate`, `_chip_class` |

## Board Module Interface

```python
# Returns HTML → st.components.v1.html()
def render_led_panel(leds: list) -> str: ...
def render_uart_console(uart_data: dict) -> str: ...

# Returns Plotly Figure → st.plotly_chart()
def make_sensor_chart(sensor_data: dict) -> go.Figure: ...
def make_fsm_diagram(fsm_data: dict) -> go.Figure: ...
```

## Error Handling

- Board functions never raise — return a safe fallback
- Validators always return `(bool, str)` — never raise
- Log issues in `uart_data["messages"]` with `[ERROR]` prefix
