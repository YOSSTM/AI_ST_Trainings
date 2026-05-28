# VirtualBoard Simulator — TODO: Add Architecture Section

## Context

Python 3 Streamlit app — virtual embedded-board training simulator.
No C, no HAL, no embedded toolchain.

## Naming Conventions

- Functions/variables: `snake_case` (e.g. `render_led_panel`, `make_fsm_diagram`)
- Classes: `PascalCase` (e.g. `BoardState`)
- Constants: `UPPER_SNAKE_CASE` (e.g. `BOARD_BROKEN`, `BOARD_FIXED`)

## TODO — Add Architecture Section Below

# Add an "## Architecture" section that describes:
#   1. The project file structure (simulator/board/gpio.py, uart.py, sensor.py, fsm.py)
#   2. The FSM data pattern: fsm_data dict with 'states', 'current', 'transitions'
#   3. The expected state sequence: BOOT → INIT → IDLE → RUNNING ...
#   4. Agent instructions: where to look, how to add missing transitions to the list
#
# The agent needs this to understand how to complete the FSM transitions.
# Without it, it generates isolated code that doesn't integrate.
#
# See solution/ for a complete reference.
