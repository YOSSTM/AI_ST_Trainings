"""
Exercise 03 — Custom Agents (.agent.md)
Without a scoped agent: Copilot edits everything → FSM transitions broken.
With a custom agent: tools restricted to read+search+edit, description triggers it automatically.
"""
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_WS = WORKSPACE_ROOT / "exercises" / "03_agents" / "workspace"


def _validate():
    issues = []

    # ── Check 1: .github/agents/ folder exists with at least one .agent.md ───
    agents_dir = _WS / ".github" / "agents"
    agent_files = list(agents_dir.glob("*.agent.md")) if agents_dir.exists() else []
    if not agent_files:
        return False, (
            "❌ No `.agent.md` file found.\n"
            "Create `.github/agents/fsm-agent.agent.md` in the workspace.\n\n"
            "**Location:** `.github/agents/*.agent.md`"
        )

    agent_file = agent_files[0]
    raw = agent_file.read_text()

    # ── Check 2: YAML front-matter ────────────────────────────────────────────
    fm_lines = raw.splitlines()
    if not fm_lines or fm_lines[0].strip() != "---":
        return False, "❌ `.agent.md` has no YAML front-matter. Add `---` markers."
    end = next((i for i, l in enumerate(fm_lines[1:], 1) if l.strip() == "---"), -1)
    if end < 0:
        return False, "❌ YAML front-matter not closed — add a closing `---`."
    fm_content = "\n".join(fm_lines[1:end])

    # ── Check 3: description is present and meaningful ────────────────────────
    desc_line = next((l for l in fm_content.splitlines() if l.strip().startswith("description:")), None)
    if desc_line is None:
        issues.append(
            "⚠ `description:` missing — it is **required** in `.agent.md`.\n"
            "   Copilot uses it to decide when to invoke this agent automatically."
        )
    else:
        desc_value = desc_line.split(":", 1)[-1].strip().strip('"').strip("'")
        if len(desc_value) < 20:
            issues.append(
                f"⚠ `description:` too vague ({len(desc_value)} chars).\n"
                "   Include trigger phrases, e.g. 'Use when modifying FSM transitions in simulator/board/fsm.py'"
            )

    # ── Check 4: tools are restricted (not unrestricted) ─────────────────────
    tools_line = next((l for l in fm_content.splitlines() if l.strip().startswith("tools:")), None)
    if tools_line is None:
        issues.append(
            "⚠ `tools:` field missing.\n"
            "   Without it, the agent has unrestricted access. "
            "   Restrict to: `tools: [read, search, edit]`"
        )
    else:
        tools_value = tools_line.split(":", 1)[-1].strip().lower()
        if "execute" in tools_value or "web" in tools_value:
            issues.append(
                "⚠ Agent has `execute` or `web` access — unnecessary for FSM editing.\n"
                "   Restrict to: `tools: [read, search, edit]`"
            )

    # ── Check 5: body contains FSM context ────────────────────────────────────
    body = "\n".join(fm_lines[end + 1:]).lower()
    required = ["fsm", "transition", "simulator"]
    missing = [kw for kw in required if kw not in body]
    if missing:
        issues.append(
            f"⚠ Agent body missing context: **{', '.join(missing)}**\n"
            "   Tell the agent what it works on: FSM data dict, transition list, simulator/board/fsm.py"
        )

    if issues:
        return False, "\n\n".join(issues)

    return True, (
        "✅ Custom agent validated!\n"
        "`description:` present · tools scoped · FSM context in body — agent is ready."
    )


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
    "title":   "Exercise 03 — Custom Agents",
    "concept": "`.github/agents/*.agent.md` — scoped agent with tool restrictions",
    "mission": (
        "**🎯 Mission:** The FSM is **stuck in INIT** — transitions were accidentally "
        "overwritten because the agent had no boundaries.\n\n"
        "A generic Copilot agent was asked to complete the FSM. Without a custom agent "
        "definition, it had unrestricted access (execute, web, edit everything) and "
        "modified files it shouldn't have touched.\n\n"
        "**Your task:** Create a custom agent `.github/agents/fsm-agent.agent.md` that:\n"
        "- Has a **`description:`** that tells Copilot when to invoke it\n"
        "- Restricts **`tools:`** to `[read, search, edit]` — no terminal, no web\n"
        "- Has a body explaining what it does: FSM transitions in `simulator/board/fsm.py`\n\n"
        "💬 Once created, invoke it in Copilot Chat: type `@fsm-agent` and ask it to "
        "complete the missing FSM transitions."
    ),
    "problem": "No custom agent → unrestricted agent overwrote FSM transitions!",
    "hints": [
        "Custom agents live in `.github/agents/*.agent.md`",
        "`description:` is **required** — Copilot reads it to auto-invoke the agent",
        "Include trigger phrases: 'Use when modifying FSM transitions in simulator/board/fsm.py'",
        "`tools:` restricts what the agent can do — `[read, search, edit]` is enough for FSM work",
        "Without `tools:`, agent has unrestricted access (including `execute` and `web`)",
        "Body: describe the FSM data dict — `states`, `current`, `transitions: list[tuple]`",
        "💬 After creating the file, type `@fsm-agent` in Copilot Chat to invoke it",
        "💬 Ask it: \"Add the missing INIT → IDLE and IDLE → RUNNING transitions\"",
    ],
    "files_to_edit": [
        "exercises/03_agents/workspace/.github/agents/fsm-agent.agent.md",
    ],
    "validate": _validate,
    "board_broken": BOARD_BROKEN,
    "board_fixed":  BOARD_FIXED,
    "explanation": """## What changed?

### Why custom agents?

A **generic Copilot agent** has unrestricted tools by default:

| Tool | Risk without scoping |
|------|---------------------|
| `execute` | Runs arbitrary shell commands |
| `web` | Fetches external URLs |
| `edit` | Edits ANY file in the repo |

A **custom agent** (`fsm-agent.agent.md`) scopes all of this:

```yaml
---
description: "FSM specialist for simulator/board/fsm.py. Use when adding or reviewing
  state transitions in the VirtualBoard FSM data dict."
tools: [read, search, edit]
---
```

### The `.agent.md` format

```
.github/agents/
└── fsm-agent.agent.md   ← filename = @fsm-agent in chat
```

| Front-matter field | Required? | Purpose |
|--------------------|-----------|---------|
| `description:` | ✅ yes | Copilot reads this to auto-invoke the agent |
| `tools:` | recommended | Restrict to minimum needed (`read`, `search`, `edit`) |
| `name:` | optional | Display name (defaults to filename) |
| `model:` | optional | Lock to a specific model |

### Invoking in Copilot Chat

```
@fsm-agent Add the missing INIT → IDLE transition
```

The agent reads `simulator/board/fsm.py`, finds the `fsm_data` dict,
and adds only what's needed — it cannot accidentally run tests or push code.
""",
}
