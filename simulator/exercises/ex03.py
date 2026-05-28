"""
Exercise 03 — Agent mode
Without proper context: agent can't navigate the codebase → FSM stuck in INIT.
"""
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "03_agents" / "workspace"


def _validate():
    instructions = _WS / ".github" / "copilot-instructions.md"
    if not instructions.exists():
        return False, (
            "Missing `exercises/03_agents/workspace/.github/copilot-instructions.md`\n"
            "Agents need instructions that describe the project structure."
        )
    content = instructions.read_text().lower()
    required = ["fsm", "state", "transition", "agent", "codebase"]
    missing = [kw for kw in required if kw not in content]
    if missing:
        return False, (
            f"Instructions don't mention: **{', '.join(missing)}**\n"
            "The agent needs to know about the FSM architecture to complete transitions."
        )
    return True, "Agent context configured! The FSM can now complete its state transitions."


# ── Board states ──────────────────────────────────────────────────────────────

BOARD_BROKEN = {
    "leds": [
        {"id": "GPIO_LED_STATUS", "color": "green",  "on": True,  "blink": "slow"},
        {"id": "GPIO_LED_ERROR",  "color": "red",    "on": False, "blink": None},
        {"id": "GPIO_LED_COMM",   "color": "blue",   "on": False, "blink": None},
        {"id": "GPIO_LED_WARN",   "color": "yellow", "on": True,  "blink": "slow"},
    ],
    "uart": {
        "messages": [
            "[INFO]  UART init OK",
            "[WARN]  FSM: no transition from INIT",
            "[WARN]  FSM: no transition from INIT",
            "[WARN]  FSM: no transition from INIT",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [
            24.0, 24.1, 24.2, 24.1, 24.0, 24.2, 24.3,
            24.2, 24.1, 24.0, 24.2, 24.1, 24.0, 24.2,
            24.1, 24.0, 24.1, 24.2, 24.0, 24.1,
        ],
        "adc_values": [
            1280, 1282, 1285, 1281, 1278, 1283, 1286,
            1282, 1279, 1277, 1281, 1280, 1278, 1282,
            1280, 1278, 1280, 1283, 1279, 1280,
        ],
        "label": "TMP36 / PA0",
    },
    "fsm": {
        "states":  ["BOOT", "INIT", "IDLE", "RUNNING", "ERROR", "RESET"],
        "current": "INIT",
        "transitions": [
            ("BOOT", "INIT"),
            # Missing: INIT -> IDLE, and rest of transitions
            ("RUNNING", "ERROR"), ("ERROR", "RESET"),
        ],
    },
    "status":     {"GPIO": "WARN", "UART": "WARN", "SENSOR": "PASS", "FSM": "FAIL"},
    "error_note": "Agent has no codebase context → generated incomplete FSM (missing transitions)",
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
            "[INFO]  FSM: BOOT -> INIT",
            "[INFO]  FSM: INIT -> IDLE",
            "[INFO]  FSM: IDLE -> RUNNING",
            "[DEBUG] FSM: cycle OK",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [
            24.0, 24.1, 24.2, 24.1, 24.0, 24.2, 24.3,
            24.2, 24.1, 24.0, 24.2, 24.1, 24.0, 24.2,
            24.1, 24.0, 24.1, 24.2, 24.0, 24.1,
        ],
        "adc_values": [
            1280, 1282, 1285, 1281, 1278, 1283, 1286,
            1282, 1279, 1277, 1281, 1280, 1278, 1282,
            1280, 1278, 1280, 1283, 1279, 1280,
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
    "title":   "Exercise 03 — Agent Mode",
    "concept": "Agent mode + codebase context",
    "mission": (
        "**🎯 Mission:** The FSM is **stuck in INIT** — it never transitions.\n\n"
        "A developer used Copilot Agent to generate the FSM, but the agent had "
        "no knowledge of the project structure. It generated an incomplete state "
        "machine missing all transitions after INIT.\n\n"
        "**Your task:** Update the `copilot-instructions.md` to give the agent "
        "context about the FSM architecture, so it can navigate the codebase "
        "and complete the missing transitions."
    ),
    "problem": "Agent has no codebase context → FSM incomplete, stuck in INIT forever!",
    "hints": [
        "In agent mode, `copilot-instructions.md` is the agent's map of your project",
        "Describe the FSM pattern: states, transitions, and the `FSM_Transition()` function",
        "Tell the agent where each module lives: `src/fsm.c`, `src/gpio.c`, etc.",
        "Mention that transitions must be registered via `FSM_AddTransition()`",
        "Add a `## Architecture` section describing module dependencies",
    ],
    "files_to_edit": [
        "exercises/03_agents/workspace/.github/copilot-instructions.md"
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## What changed?

Agents navigate your **entire codebase** autonomously. Without context they:
- Miss files that define patterns they should follow
- Generate isolated code that doesn't integrate with existing modules
- Skip registering callbacks or transitions because they don't know they exist

By describing the FSM architecture in `copilot-instructions.md`, the agent:
- Knows to look in `src/fsm.c` for the state machine implementation
- Understands that `FSM_AddTransition(src, dst, guard, action)` must be called
- Can trace the call graph to find where to add the missing `INIT → IDLE` transition
""",
}
