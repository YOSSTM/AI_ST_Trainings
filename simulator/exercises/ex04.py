"""
Exercise 04 — Skills (SKILL.md)
The SKILL.md format: name (required, matches folder), description (required), body.
Without domain skill: Copilot calibrates the ADC wrong → sensor reads 998 °C.
"""
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "04_skills" / "workspace"


def _validate():
    issues = []

    # ── Check 1: .github/skills/ folder exists with at least one skill folder ──
    skills_root = _WS / ".github" / "skills"
    skill_dirs = [d for d in skills_root.iterdir() if d.is_dir()] if skills_root.exists() else []
    if not skill_dirs:
        return False, (
            "❌ No skill folder found.\n"
            "Create `.github/skills/sensor-calibration/SKILL.md` in the workspace.\n\n"
            "**SKILL.md structure:**\n"
            "```\n"
            ".github/skills/<skill-name>/\n"
            "└── SKILL.md   ← required (name must match folder)\n"
            "```"
        )

    skill_dir = skill_dirs[0]
    skill_file = skill_dir / "SKILL.md"

    # ── Check 2: SKILL.md file exists inside the folder ──────────────────────
    if not skill_file.exists():
        return False, (
            f"❌ `SKILL.md` not found inside `{skill_dir.name}/`.\n"
            "The file must be named exactly `SKILL.md` (uppercase)."
        )

    raw = skill_file.read_text()

    # ── Check 3: Parse YAML front-matter ─────────────────────────────────────
    fm_lines = raw.splitlines()
    if not fm_lines or fm_lines[0].strip() != "---":
        return False, (
            "❌ `SKILL.md` has no YAML front-matter.\n"
            "Add `---` markers at the top with `name:` and `description:` fields."
        )
    end = next((i for i, l in enumerate(fm_lines[1:], 1) if l.strip() == "---"), -1)
    if end < 0:
        return False, "❌ YAML front-matter not closed — add a closing `---`."
    fm_content = "\n".join(fm_lines[1:end])

    # ── Check 4: name: is present and matches folder name ─────────────────────
    name_line = next((l for l in fm_content.splitlines() if l.strip().startswith("name:")), None)
    if name_line is None:
        issues.append(
            "⚠ `name:` field missing from front-matter — it is **required** in `SKILL.md`.\n"
            f"   Expected: `name: {skill_dir.name}`"
        )
    else:
        name_value = name_line.split(":", 1)[-1].strip().strip('"').strip("'")
        if name_value != skill_dir.name:
            issues.append(
                f"⚠ `name: {name_value}` does not match folder name `{skill_dir.name}`.\n"
                "   The `name:` value must match the folder exactly."
            )

    # ── Check 5: description: is present and meaningful ───────────────────────
    desc_line = next((l for l in fm_content.splitlines() if l.strip().startswith("description:")), None)
    if desc_line is None:
        issues.append(
            "⚠ `description:` field missing — it is **required** in `SKILL.md`.\n"
            "   Copilot uses it to decide when to load the skill automatically."
        )
    else:
        desc_value = desc_line.split(":", 1)[-1].strip().strip('"').strip("'")
        if desc_value.upper().startswith("TODO") or len(desc_value) < 25:
            issues.append(
                f"⚠ `description:` too vague ({len(desc_value)} chars).\n"
                "   Be specific: name the domain, sensor, and function."
            )

    # ── Check 6: body contains domain knowledge ───────────────────────────────
    body = "\n".join(fm_lines[end + 1:]).lower()
    required = ["adc", "calibr", "vref", "temperature", "formula"]
    missing = [kw for kw in required if kw not in body]
    if missing:
        issues.append(
            f"⚠ Skill body is missing domain content: **{', '.join(missing)}**\n"
            "   Document the TMP36 formula, Vref=3.3V, and the conversion function."
        )

    if issues:
        return False, "\n\n".join(issues)

    return True, (
        "✅ Skill validated!\n"
        f"`name: {skill_dir.name}` matches folder · `description:` present · body has TMP36 domain knowledge."
    )


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
    "title":   "Exercise 04 — SKILL.md",
    "concept": "`SKILL.md` — packaged Copilot skill",
    "mission": (
        "**🎯 Mission:** The sensor is reading **998 °C** — the board triggered "
        "overheat protection and the FSM crashed to ERROR.\n\n"
        "Copilot had no domain knowledge about TMP36 ADC calibration and used "
        "the raw 12-bit ADC count directly as degrees Celsius.\n\n"
        "**Your task:** Create a proper `SKILL.md` to package the calibration "
        "knowledge so Copilot can apply it automatically.\n\n"
        "**3-step process:**\n"
        "1. Create folder `.github/skills/sensor-calibration/`\n"
        "2. Create `SKILL.md` inside it with required `name:` and `description:` front-matter\n"
        "3. Write the skill body: when to use, TMP36 formula, function signature\n\n"
        "💬 **Use Copilot Chat** to generate the skill content!"
    ),
    "problem": "No SKILL.md → Copilot used raw ADC value as temperature (998 °C!)",
    "hints": [
        # Structure
        "Folder: `.github/skills/sensor-calibration/` — then create `SKILL.md` inside",
        "`name:` is **required** and must match the folder name exactly: `sensor-calibration`",
        "`description:` is **required** — Copilot reads it to decide when to auto-load the skill",
        # Process
        "Step 1 — front-matter: `name:` + `description:` between `---` markers",
        "Step 2 — ## When to Use: describe the trigger (e.g. 'when converting TMP36 ADC readings')",
        "Step 3 — ## Procedure: formula, function signature, constraints",
        # Domain
        "TMP36 formula: `voltage = (adc_raw / 4095) * 3.3` → `temp = (voltage - 0.5) / 0.01`",
        "💬 Ask Copilot Chat: \"Write a SKILL.md for TMP36 ADC calibration — name: sensor-calibration\"",
    ],
    "files_to_edit": [
        "exercises/04_skills/workspace/.github/skills/sensor-calibration/SKILL.md",
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## What changed?

### SKILL.md — the packaged skill format

```
.github/skills/sensor-calibration/   ← folder name = skill name
└── SKILL.md                          ← required, uppercase
```

### Required front-matter

```yaml
---
name: sensor-calibration              # REQUIRED — must match folder name exactly
description: "TMP36 ADC-to-temperature calibration (Vref=3.3V, 12-bit). Use when
  generating sensor code in simulator/board/sensor.py."
---
```

| Field | Required? | Rule |
|-------|-----------|------|
| `name:` | ✅ yes | Must match folder name (lowercase, hyphens) |
| `description:` | ✅ yes | Specific — Copilot auto-loads based on this |

### The 3-step skill body

```markdown
## When to Use
Use when implementing or reviewing ADC sensor readings in the simulator.

## Formula
voltage = (adc_raw / (2**bits - 1)) × vref
temp_c  = (voltage − 0.5) / 0.01

## Function Signature
def convert_adc_to_temperature(adc_raw, vref=3.3, bits=12) -> float: ...
```

### Optional bundled assets

```
.github/skills/sensor-calibration/
├── SKILL.md
├── scripts/       ← executable helpers
├── references/    ← docs loaded on-demand
└── assets/        ← templates, boilerplate
```
""",
}
