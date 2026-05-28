"""
Exercise 01 — copilot-instructions.md + applyTo + description
Three complementary fields that govern how Copilot reads context.
"""
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "01_instructions" / "workspace"


def _validate():
    issues = []

    # ── Check 1: copilot-instructions.md with project context ─────────────────
    target = _WS / ".github" / "copilot-instructions.md"
    if not target.exists():
        issues.append(
            "❌ File not found: "
            "`exercises/01_instructions/workspace/.github/copilot-instructions.md`\n"
            "Create it in VS Code and add Python simulator context."
        )
    else:
        raw = target.read_text()
        if "# TODO" in raw:
            issues.append(
                "⚠ `copilot-instructions.md` is still the TODO template — replace it with real instructions."
            )
        else:
            content = raw.lower()
            required = ["python", "streamlit", "board", "naming", "simulator"]
            missing = [kw for kw in required if kw not in content]
            if missing:
                issues.append(
                    f"⚠ `copilot-instructions.md` is missing: **{', '.join(missing)}**\n"
                    "Mention: Python 3, Streamlit, board module structure, naming conventions."
                )

    # ── Check 2: a scoped .instructions.md with applyTo ───────────────────────
    instr_dir = _WS / ".github" / "instructions"
    instr_files = list(instr_dir.glob("*.instructions.md")) if instr_dir.exists() else []
    if not instr_files:
        issues.append(
            "❌ No `.instructions.md` file found in "
            "`exercises/01_instructions/workspace/.github/instructions/`\n"
            "Create `simulator.instructions.md` with an `applyTo` front-matter field."
        )
    else:
        instr_content = instr_files[0].read_text()
        if "applyTo" not in instr_content:
            issues.append(
                "⚠ Your `.instructions.md` has no `applyTo` front-matter.\n"
                "   Without it, instructions apply to ALL files — "
                "tests, configs, notebooks, everything."
            )
        elif "**/*.py" not in instr_content and "simulator/" not in instr_content:
            issues.append(
                "⚠ `applyTo` is too broad — scope it to Python source files:\n"
                "   `applyTo: 'simulator/**/*.py'`"
            )

    # ── Check 3: a .prompt.md skill with a rich description ───────────────────
    prompts_dir = _WS / ".github" / "prompts"
    prompt_files = list(prompts_dir.glob("*.prompt.md")) if prompts_dir.exists() else []
    if not prompt_files:
        issues.append(
            "❌ No `.prompt.md` skill found in "
            "`exercises/01_instructions/workspace/.github/prompts/`\n"
            "Create `sensor_calibration.prompt.md` with a descriptive `description:` field."
        )
    else:
        text = prompt_files[0].read_text()
        desc_line = next(
            (l for l in text.splitlines() if l.strip().startswith("description:")), None
        )
        if desc_line is None:
            issues.append(
                "⚠ Your prompt file has no `description:` field in the front-matter.\n"
                "   Without it, the skill is invisible in Copilot's `/` prompt picker."
            )
        else:
            desc_value = desc_line.split(":", 1)[-1].strip().strip('"').strip("'")
            if desc_value.upper().startswith("TODO"):
                issues.append(
                    "⚠ `description:` is still the TODO placeholder — replace it with a real description.\n"
                    "   Example: `TMP36 ADC calibration in Python (12-bit ADC, Vref=3.3V)`"
                )
            elif len(desc_value) < 25:
                issues.append(
                    f"⚠ Description too vague ({len(desc_value)} chars): `{desc_value}`\n"
                    "   Make it specific: name the domain, action, and module."
                )

    if issues:
        return False, "\n\n".join(issues)

    return True, (
        "All three configs in place!\n"
        "`copilot-instructions.md` → global context\n"
        "`.instructions.md` with `applyTo` → scoped to simulator Python files\n"
        "`description:` in skill → discoverable in Copilot prompt picker"
    )


# ── Board states ──────────────────────────────────────────────────────────────

BOARD_BROKEN = {
    "leds": [
        {"id": "led1",  "color": "red", "on": True,  "blink": "fast"},
        {"id": "led2",  "color": "red", "on": True,  "blink": "fast"},
        {"id": "led3",  "color": "red", "on": True,  "blink": "fast"},
        {"id": "led4",  "color": "red", "on": True,  "blink": "fast"},
    ],
    "uart": {
        "messages": [
            "print('hello world')",
            "TypeError: unsupported operand",
            "[WARN]  instructions bleed into test_board.py",
            "[ERROR] skill not found in prompt picker",
        ],
        "baud": 9600,
    },
    "sensor": {
        "temp_values": [-273.15] * 20,
        "adc_values":  [4095]   * 20,
        "label": "UNKNOWN — not initialized",
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
    "error_note": "No instructions → no context, no applyTo scope, skill invisible",
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
            "[INFO]  simulator init OK",
            "[INFO]  instructions scoped to simulator/**/*.py",
            "[INFO]  skill 'TMP36 calibration' found in prompt picker",
            "[INFO]  FSM -> RUNNING",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [
            23.1, 23.5, 24.0, 24.2, 24.5, 24.3, 24.1,
            23.9, 24.0, 24.2, 24.4, 24.6, 24.5, 24.3,
            24.1, 24.0, 24.2, 24.4, 24.5, 24.3,
        ],
        "adc_values": [
            1245, 1260, 1280, 1290, 1300, 1285, 1270,
            1265, 1270, 1280, 1295, 1310, 1305, 1290,
            1280, 1270, 1280, 1295, 1305, 1295,
        ],
        "label": "TMP36 / PA0 (12-bit ADC)",
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
    "title":   "Exercise 01 — Instructions, applyTo & description",
    "concept": "`copilot-instructions.md` · `applyTo` · `description`",
    "mission": (
        "**🎯 Mission:** Three Copilot config fields are missing — the board is dead.\n\n"
        "**Part A — Global instructions:**\n"
        "Create `.github/copilot-instructions.md` to teach Copilot that this is "
        "a Python/Streamlit simulator project.\n\n"
        "**Part B — Scoped instructions:**\n"
        "Create `.github/instructions/simulator.instructions.md` "
        "with `applyTo: 'simulator/**/*.py'` — without it, instructions bleed "
        "into test files, notebooks, and configs.\n\n"
        "**Part C — Discoverable skill:**\n"
        "Create `.github/prompts/sensor_calibration.prompt.md` with a rich "
        "`description:` field so the skill appears in Copilot's `/` prompt picker.\n\n"
        "💬 **Use Copilot Chat** to help you write these files! "
        "Open each workspace file and ask Copilot in Chat to generate the content."
    ),
    "problem": "No copilot-instructions.md, no applyTo scope, no skill description — all broken!",
    "hints": [
        # Part A
        "`.github/copilot-instructions.md` applies globally to ALL Copilot interactions",
        "Include: Python 3, Streamlit, Plotly, board module structure, naming conventions",
        # Part B
        "`.github/instructions/*.instructions.md` files use YAML front-matter with `applyTo`",
        "Scope with a glob: `applyTo: 'simulator/**/*.py'` — only board simulator files",
        "Without `applyTo`, simulator conventions bleed into test files, notebooks, CI configs",
        # Part C
        "The **filename** is the skill name shown in the `/` picker — there is no `name:` field",
        "The `description:` field in `.prompt.md` is what shows as the label in Copilot's `/` picker",
        "`mode:` is **optional** (default: `ask`). Use `edit` for code-generation skills, `agent` for multi-file tasks",
        "Make description specific: `TMP36 ADC calibration in Python (Vref=3.3V, 12-bit)`",
        # Copilot Chat
        "💬 Open a workspace file → ask Copilot Chat to generate the content — that's the exercise!",
    ],
    "files_to_edit": [
        "exercises/01_instructions/workspace/.github/copilot-instructions.md",
        "exercises/01_instructions/workspace/.github/instructions/simulator.instructions.md",
        "exercises/01_instructions/workspace/.github/prompts/sensor_calibration.prompt.md",
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## What changed?

### Part A — `copilot-instructions.md` (global)

Applies to **every** Copilot interaction in the repo — chats, completions, edits.
Tells Copilot the tech stack, project structure, and naming conventions once,
so you never have to repeat them in prompts.

```
.github/copilot-instructions.md
```

---

### Part B — `applyTo` (scoped instructions)

```yaml
---
applyTo: "simulator/**/*.py"
---
# Instructions only active when Copilot touches simulator Python files
```

Without `applyTo`, instructions apply to **every file** Copilot touches:
test scripts, `.env`, notebooks, `requirements.txt`, CI configs...

`applyTo` uses glob patterns to confine instructions to the right context.

---

### Part C — `description:` (skill discoverability)

```yaml
---
description: TMP36 ADC calibration in Python (12-bit ADC, Vref=3.3V)
mode: edit      # optional — ask (default) | edit | agent
---
```

**Key facts about `.prompt.md` front-matter:**

| Field | Required? | Purpose |
|-------|-----------|---------|
| `description` | ✅ **yes** (for discoverability) | Label shown in `/` picker; Copilot uses it to auto-suggest |
| `mode` | ❌ optional (default: `ask`) | `ask` = chat, `edit` = code edit, `agent` = multi-step |
| `name` | ❌ **does not exist** | The **filename** (`sensor_calibration`) IS the skill name |

A vague description → the skill is **invisible**.  
No `mode` → defaults to `ask` mode.
""",
}
