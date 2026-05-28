"""
Exercise 05 — Capstone
Everything is broken. Fix all Copilot configs to bring the board back to life.
"""
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "05_capstone" / "workspace"


def _validate():
    results = []

    # Check 1: instructions
    instr = _WS / ".github" / "copilot-instructions.md"
    if not instr.exists():
        results.append("❌ Missing `.github/copilot-instructions.md`")
    else:
        raw = instr.read_text()
        if "# TODO" in raw:
            results.append("⚠ `copilot-instructions.md` is still the TODO template — fill it in")
        else:
            c = raw.lower()
            if not all(kw in c for kw in ["embedded", "gpio", "uart", "naming"]):
                results.append("⚠ `copilot-instructions.md` needs more embedded context")

    # Check 2: at least one prompt file
    prompts_dir = _WS / ".github" / "prompts"
    prompt_files = list(prompts_dir.glob("*.prompt.md")) if prompts_dir.exists() else []
    if not prompt_files:
        results.append("❌ Missing `.github/prompts/*.prompt.md`")
    else:
        combined = " ".join(f.read_text().lower() for f in prompt_files)
        if "uart" not in combined and "sensor" not in combined:
            results.append("⚠ Prompt files need UART or sensor context")

    if results:
        return False, "\n".join(results) + "\n\nFix all issues to complete the capstone."

    return True, (
        "🎉 All configs in place! "
        "The board is fully operational — mission complete!"
    )


# ── Board states ──────────────────────────────────────────────────────────────

BOARD_BROKEN = {
    "leds": [
        {"id": "led1", "color": "red", "on": True,  "blink": "fast"},
        {"id": "led2", "color": "red", "on": True,  "blink": "fast"},
        {"id": "led3", "color": "red", "on": True,  "blink": "fast"},
        {"id": "led4", "color": "red", "on": True,  "blink": "fast"},
    ],
    "uart": {
        "messages": [
            "print('hello world')",
            "ERROR: buf overflow +12",
            "0xDEAD 0xBEEF ??",
            "[ERROR] Temp: 998.7 C",
        ],
        "baud": 9600,
    },
    "sensor": {
        "temp_values": [-273.15] * 10 + [998.7] * 10,
        "adc_values":  [4095]    * 20,
        "label": "MULTIPLE FAILURES",
    },
    "fsm": {
        "states":      ["state1", "state2", "state3", "state4"],
        "current":     "state1",
        "transitions": [
            ("state1", "state2"), ("state2", "state3"),
            ("state3", "state4"), ("state4", "state1"),
        ],
    },
    "status":     {"GPIO": "FAIL", "UART": "FAIL", "SENSOR": "FAIL", "FSM": "FAIL"},
    "error_note": "All Copilot configs missing — the board is completely dead",
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
            "[INFO]  System init OK",
            "[INFO]  UART OK (115200 8N1)",
            "[DEBUG] Temp: 24.2 C  ADC: 1282",
            "[INFO]  FSM -> RUNNING  All OK",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [
            23.8, 24.0, 24.2, 24.5, 24.3, 24.1, 24.0,
            24.2, 24.4, 24.3, 24.1, 24.0, 24.2, 24.4,
            24.3, 24.1, 24.0, 24.2, 24.5, 24.3,
        ],
        "adc_values": [
            1272, 1278, 1283, 1291, 1286, 1281, 1278,
            1283, 1289, 1286, 1281, 1278, 1283, 1289,
            1286, 1281, 1278, 1283, 1291, 1286,
        ],
        "label": "TMP36 / PA0 — calibrated",
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
    "title":   "Exercise 05 — Capstone",
    "concept": "All concepts combined",
    "mission": (
        "**🎯 Final Mission:** The board is completely dead.\n\n"
        "A new developer joined the team, deleted all the Copilot config files "
        "\"to start fresh\", and let Copilot regenerate everything from scratch. "
        "The result: total failure across all modules.\n\n"
        "**Your task:** Apply everything you learned in exercises 01–04 to bring "
        "the board back to life:\n"
        "- ✅ `copilot-instructions.md` with embedded context\n"
        "- ✅ `.prompt.md` for UART handler\n"
        "- ✅ Skill (`.prompt.md` **or** `SKILL.md`) for sensor calibration\n"
        "- ✅ Agent instructions for FSM navigation\n\n"
        "💬 **Use Copilot Chat freely** — this is the capstone, no restrictions!"
    ),
    "problem": "All Copilot configs deleted — board completely dead!",
    "hints": [
        "Re-use your fixes from exercises 01–04",
        "Instructions + prompts + skills all go in `.github/`",
        "Remember: `.prompt.md` filename = skill name; `SKILL.md` requires `name:` matching the folder",
        "`mode:` is always optional in `.prompt.md` (defaults to `ask`)",
        "Check Correction mode on each previous exercise for reference",
        "💬 Open Copilot Chat, switch to **Agent mode**, and ask it to reconstruct the configs",
    ],
    "files_to_edit": [
        "exercises/05_capstone/workspace/.github/copilot-instructions.md",
        "exercises/05_capstone/workspace/.github/prompts/uart_handler.prompt.md",
        "exercises/05_capstone/workspace/.github/skills/sensor-calibration/SKILL.md",
        "exercises/05_capstone/workspace/.github/agents/fsm-agent.agent.md",
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## The Full Picture

You've now seen how **four complementary tools** work together:

| Tool | Where it lives | What it teaches Copilot |
|------|---------------|------------------------|
| `copilot-instructions.md` | `.github/` | Tech stack, conventions, architecture |
| `*.instructions.md` with `applyTo` | `.github/instructions/` | Scoped rules for specific file patterns |
| `*.prompt.md` | `.github/prompts/` | Reusable prompts — **filename** is the slash-command name, `mode:` is optional |
| `SKILL.md` | `.github/skills/<name>/` | Packaged skill — **`name:`** required, must match folder |
| `*.agent.md` | `.github/agents/` | Custom agent — **`description:`** required, restrict `tools:` |

Together they turn Copilot from a generic autocomplete into a **senior embedded SW engineer** that knows your exact project.
""",
}
