"""
Exercise 04 — Skills (.prompt.md as a reusable skill)
Without domain skill: Copilot calibrates the ADC wrong → sensor reads 998 °C.
"""
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "04_skills" / "workspace"


def _validate():
    prompt_dir = _WS / ".github" / "prompts"
    files = list(prompt_dir.glob("*.prompt.md")) if prompt_dir.exists() else []
    if not files:
        return False, (
            "No skill file found in "
            "`exercises/04_skills/workspace/.github/prompts/`\n"
            "Create `sensor_calibration.prompt.md` as a reusable skill."
        )
    raw = files[0].read_text()
    if "# TODO" in raw or "TODO —" in raw:
        return False, (
            "Skill file is still the TODO template — replace it with a real skill.\n"
            "Include the TMP36 formula, `convert_adc_to_temperature()` signature, Vref, and resolution."
        )
    content = raw.lower()
    required = ["adc", "calibr", "vref", "temperature", "formula"]
    missing = [kw for kw in required if kw not in content]
    if missing:
        return False, (
            f"Skill is incomplete — missing: **{', '.join(missing)}**\n"
            "The skill must explain the Python ADC-to-temperature conversion: Vref, resolution, formula."
        )
    return True, "Skill file valid! Copilot now understands TMP36 calibration in Python."


# ── Board states ──────────────────────────────────────────────────────────────

BOARD_BROKEN = {
    "leds": [
        {"id": "GPIO_LED_STATUS", "color": "green",  "on": True,  "blink": None},
        {"id": "GPIO_LED_ERROR",  "color": "red",    "on": True,  "blink": "slow"},
        {"id": "GPIO_LED_COMM",   "color": "blue",   "on": True,  "blink": "slow"},
        {"id": "GPIO_LED_WARN",   "color": "yellow", "on": True,  "blink": "fast"},
    ],
    "uart": {
        "messages": [
            "[ERROR] Temp out of range: 998.7 C",
            "[ERROR] Temp out of range: 1001.2 C",
            "[WARN]  ADC raw: 4012 (unscaled!)",
            "[ERROR] Overheat protection triggered",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [998.7, 1001.2, 995.4, 1003.8, 999.1,
                        1002.5, 997.3, 1004.6, 998.0, 1000.5,
                        996.8, 1002.1, 999.4, 1001.7, 997.5,
                        1003.2, 998.9, 1000.1, 996.3, 1002.8],
        "adc_values":  [4012, 4015, 4008, 4019, 4013,
                        4016, 4010, 4020, 4012, 4014,
                        4009, 4015, 4013, 4016, 4010,
                        4018, 4012, 4014, 4008, 4016],
        "label": "TMP36 / PA0 — WRONG CALIBRATION",
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
    "status":     {"GPIO": "WARN", "UART": "FAIL", "SENSOR": "FAIL", "FSM": "WARN"},
    "error_note": "No ADC skill → Copilot used raw ADC count as temperature (998 °C!)",
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
            "[INFO]  ADC calibration OK (Vref=3.3V, 12-bit)",
            "[DEBUG] Raw ADC: 1287  Voltage: 1.037V",
            "[INFO]  Temp: 23.7 C  (TMP36 formula OK)",
            "[DEBUG] Temp: 24.1 C",
        ],
        "baud": 115200,
    },
    "sensor": {
        "temp_values": [23.7, 24.1, 24.3, 24.0, 23.8,
                        24.2, 24.5, 24.3, 24.0, 23.9,
                        24.1, 24.4, 24.2, 24.0, 23.8,
                        24.1, 24.3, 24.5, 24.2, 24.0],
        "adc_values":  [1275, 1282, 1286, 1279, 1272,
                        1283, 1291, 1286, 1279, 1274,
                        1281, 1288, 1283, 1279, 1272,
                        1281, 1285, 1291, 1282, 1279],
        "label": "TMP36 / PA0 (calibrated, Vref=3.3V)",
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
    "title":   "Exercise 04 — Skills",
    "concept": "`.prompt.md` skill · `SKILL.md` folder-based skill",
    "mission": (
        "**🎯 Mission:** The sensor is reading **998 °C** — the board triggered "
        "overheat protection and the FSM crashed to ERROR.\n\n"
        "Copilot was asked to implement ADC-to-temperature conversion but had "
        "no domain knowledge about the TMP36 sensor or ADC calibration. "
        "It used the raw 12-bit ADC count directly as degrees Celsius.\n\n"
        "**Option A — Quick skill:** Create a `sensor_calibration.prompt.md` in `.github/prompts/` "
        "with a rich `description:` and the TMP36 formula.\n\n"
        "**Option B — Packaged skill:** Create a `SKILL.md` inside `.github/skills/sensor-calibration/` "
        "for a more structured, multi-asset skill with a `name:` field matching the folder.\n\n"
        "💬 **Use Copilot Chat** to help you write the skill content!"
    ),
    "problem": "No domain skill → Copilot used raw ADC value as temperature (998 °C!)",
    "hints": [
        # prompt.md approach
        "**`.prompt.md`** — quick skill: `sensor_calibration.prompt.md` in `.github/prompts/`",
        "The **filename** (without extension) is the slash-command name — there is no `name:` field",
        "`mode:` is optional (defaults to `ask`). Use `edit` for code generation skills",
        # SKILL.md approach
        "**`SKILL.md`** — packaged skill: `.github/skills/sensor-calibration/SKILL.md`",
        "In `SKILL.md`, `name:` IS required and must match the folder name (e.g. `sensor-calibration`)",
        "SKILL.md supports bundled assets: `scripts/`, `references/`, `assets/` sub-folders",
        # formula
        "TMP36 formula: `Temp (°C) = (Voltage - 0.5) / 0.01`",
        "ADC voltage: `V = (adc_raw / (2**bits - 1)) * vref` where Vref = 3.3V, bits = 12",
        "💬 Ask Copilot Chat: \"Write a TMP36 calibration skill for `.github/prompts/`\"",
    ],
    "files_to_edit": [
        "exercises/04_skills/workspace/.github/prompts/sensor_calibration.prompt.md",
        "(or) .github/skills/sensor-calibration/SKILL.md  (the SKILL.md approach)",
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## What changed?

### Two ways to package a skill

#### A — `.prompt.md` (quick skill)

File: `.github/prompts/sensor_calibration.prompt.md`

```yaml
---
description: TMP36 ADC calibration in Python (12-bit ADC, Vref=3.3V)
mode: edit   # optional
---
```

- The **filename** (`sensor_calibration`) is the slash-command name — no `name:` field exists here
- Invoked via `/sensor_calibration` in Copilot Chat
- Best for: single focused tasks with a prompt body

---

#### B — `SKILL.md` (packaged skill)

Folder: `.github/skills/sensor-calibration/SKILL.md`

```yaml
---
name: sensor-calibration    # required — must match folder name
description: 'TMP36 ADC calibration in Python. Use for sensor readings in simulator/board/sensor.py.'
---
```

- `name:` IS required and must match the folder name (lowercase, hyphens)
- Supports bundled `scripts/`, `references/`, `assets/` folders
- Best for: multi-step workflows with templates or helper scripts

---

### The TMP36 calibration formula

```python
def convert_adc_to_temperature(adc_raw: int, vref: float = 3.3, bits: int = 12) -> float:
    voltage = (adc_raw / (2**bits - 1)) * vref
    temp_c  = (voltage - 0.5) / 0.01
    if temp_c < -40.0 or temp_c > 125.0:
        return float('nan')
    return round(temp_c, 1)
```

Without a skill, Copilot has no way to know the TMP36 transfer function or that Vref = 3.3V.
""",
}
