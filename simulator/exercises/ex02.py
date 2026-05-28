"""
Exercise 02 — .prompt.md files
Without them: vague prompts produce malformed UART output.
"""
from pathlib import Path
import glob

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "02_prompts" / "workspace"


def _validate():
    prompt_dir = _WS / ".github" / "prompts"
    files = list(prompt_dir.glob("*.prompt.md")) if prompt_dir.exists() else []
    if not files:
        return False, (
            "No `.prompt.md` file found in "
            "`exercises/02_prompts/workspace/.github/prompts/`\n"
            "Create `uart_handler.prompt.md` with structured prompt content."
        )
    raw = files[0].read_text()
    if "# TODO" in raw or "TODO —" in raw:
        return False, (
            "Prompt file is still the TODO template — replace it with a real structured prompt.\n"
            "Describe the `uart_data` dict, message format, and reference `render_uart_console()`."
        )
    content = raw.lower()
    required = ["uart", "format", "message", "render_uart_console"]
    missing = [kw for kw in required if kw not in content]
    if missing:
        return False, (
            f"Prompt is still too vague — missing: **{', '.join(missing)}**\n"
            "Describe the expected message format, the `render_uart_console()` API, and the dict structure."
        )
    return True, "Great prompt! Copilot now generates proper UART log messages for the simulator."


# ── Board states ──────────────────────────────────────────────────────────────

BOARD_BROKEN = {
    "leds": [
        {"id": "GPIO_LED_STATUS", "color": "green",  "on": True,  "blink": None},
        {"id": "GPIO_LED_ERROR",  "color": "red",    "on": True,  "blink": "fast"},
        {"id": "GPIO_LED_COMM",   "color": "blue",   "on": True,  "blink": "fast"},
        {"id": "GPIO_LED_WARN",   "color": "yellow", "on": True,  "blink": "slow"},
    ],
    "uart": {
        "messages": [
            "a#!$% garbled...",
            "msg truncated at 0x",
            "??  [0xFF 0x00 0xAB]",
            "ERROR: buf overflow +12",
            "a#!$% garbled...",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [
            24.1, 24.3, 24.2, 24.5, 24.4, 24.3, 24.2,
            24.1, 24.3, 24.5, 24.4, 24.2, 24.1, 24.3,
            24.5, 24.4, 24.2, 24.1, 24.3, 24.2,
        ],
        "adc_values": [
            1280, 1290, 1285, 1295, 1290, 1285, 1280,
            1275, 1285, 1295, 1290, 1280, 1275, 1285,
            1295, 1290, 1280, 1275, 1285, 1280,
        ],
        "label": "TMP36 / PA0",
    },
    "fsm": {
        "states":  ["BOOT", "INIT", "IDLE", "RUNNING", "ERROR", "RESET"],
        "current": "ERROR",
        "transitions": [
            ("BOOT", "INIT"), ("INIT", "IDLE"),
            ("IDLE", "RUNNING"), ("RUNNING", "ERROR"),
            ("ERROR", "RESET"), ("RESET", "IDLE"),
        ],
    },
    "status":     {"GPIO": "WARN", "UART": "FAIL", "SENSOR": "PASS", "FSM": "WARN"},
    "error_note": "Vague prompt → Copilot generated a broken UART handler with buffer overflow",
}

BOARD_FIXED = {
    "leds": [
        {"id": "GPIO_LED_STATUS", "color": "green",  "on": True,  "blink": None},
        {"id": "GPIO_LED_ERROR",  "color": "red",    "on": False, "blink": None},
        {"id": "GPIO_LED_COMM",   "color": "blue",   "on": True,  "blink": "slow"},
        {"id": "GPIO_LED_WARN",   "color": "yellow", "on": False, "blink": None},
    ],
    "uart": {
        "messages": [
            "[INFO]  UART init OK (115200 8N1)",
            "[INFO]  MSG #001 | ID:0x01 | Temp:24.5C",
            "[DEBUG] MSG #002 | ID:0x02 | ADC:1285",
            "[INFO]  MSG #003 | ID:0x01 | Temp:24.3C",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [
            24.1, 24.3, 24.2, 24.5, 24.4, 24.3, 24.2,
            24.1, 24.3, 24.5, 24.4, 24.2, 24.1, 24.3,
            24.5, 24.4, 24.2, 24.1, 24.3, 24.2,
        ],
        "adc_values": [
            1280, 1290, 1285, 1295, 1290, 1285, 1280,
            1275, 1285, 1295, 1290, 1280, 1275, 1285,
            1295, 1290, 1280, 1275, 1285, 1280,
        ],
        "label": "TMP36 / PA0",
    },
    "fsm": {
        "states":  ["BOOT", "INIT", "IDLE", "RUNNING", "ERROR", "RESET"],
        "current": "RUNNING",
        "transitions": [
            ("BOOT", "INIT"), ("INIT", "IDLE"),
            ("IDLE", "RUNNING"), ("RUNNING", "IDLE"),
            ("RUNNING", "ERROR"), ("ERROR", "RESET"), ("RESET", "IDLE"),
        ],
    },
    "status":     {"GPIO": "PASS", "UART": "PASS", "SENSOR": "PASS", "FSM": "PASS"},
    "error_note": None,
}

# ── Exercise definition ───────────────────────────────────────────────────────

EXERCISE = {
    "title":   "Exercise 02 — Prompt Files",
    "concept": "`.github/prompts/*.prompt.md`",
    "mission": (
        "**🎯 Mission:** The UART console is spitting out garbage.\n\n"
        "A developer used Copilot to generate the UART message handler, "
        "but with a vague one-liner prompt: *'write a uart handler'*. "
        "The result: buffer overflow, garbled bytes, FSM stuck in ERROR.\n\n"
        "**Your task:** Write a proper `.prompt.md` file that gives Copilot "
        "enough context to generate a correct UART handler.\n\n"
        "💬 **Use Copilot Chat** to help you write it! Open the workspace file and ask Copilot to fill it in."
    ),
    "problem": "Prompt too vague → Copilot generated a UART handler with buffer overflow!",
    "hints": [
        "A `.prompt.md` lives in `.github/prompts/` — the **filename** is the slash-command name",
        "`mode:` is **optional** (default: `ask`). Add `mode: edit` for code-generation prompts",
        "There is **no `name:` field** in `.prompt.md` — use `description:` as the label",
        "Describe: `uart_data` dict structure, `messages: list[str]`, `baud: int`",
        "Include: message format `[LEVEL]  text` and `render_uart_console()` function reference",
        "💬 Try in Copilot Chat: `/uart_handler` once the file exists to invoke it directly",
    ],
    "files_to_edit": [
        "exercises/02_prompts/workspace/.github/prompts/uart_handler.prompt.md"
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## What changed?

A well-structured `.prompt.md` gives Copilot:

- **Scope**: what to generate and in which module (`simulator/board/uart.py`)
- **Data structure**: the `uart_data` dict — `messages: list[str]`, `baud: int`
- **Format spec**: `[LEVEL]  text` prefix, colorized by `render_uart_console()`
- **Integration**: how to append a message and call `st.rerun()` to refresh
- **Python patterns**: type hints, docstrings, no mutable defaults

Reusable prompts save your whole team from repeating context in every chat.
""",
}
