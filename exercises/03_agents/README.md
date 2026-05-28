# Exercise 03 — Custom Agents (`.agent.md`)

> **Concept:** Create a custom Copilot agent with a scoped `description:` and restricted `tools:` to illustrate why agent boundaries matter.

---

## 🔴 The Problem

The FSM is **stuck in INIT** — transitions were accidentally overwritten.

A developer ran a generic Copilot agent (no `.agent.md`, no tool restrictions) and asked it to complete the FSM. With unrestricted access the agent:
- Had `execute`, `web`, and edit-everything by default
- Modified files it shouldn't have touched
- Overwrote the transition list instead of appending to it

Result: only `BOOT → INIT` survived, all other transitions are gone.

---

## 🎯 Your Task

Create the file:
```
exercises/03_agents/workspace/.github/agents/fsm-agent.agent.md
```

Your agent must have:

| Field | Required? | What to write |
|-------|-----------|---------------|
| `description:` | ✅ yes | Trigger phrases — when and where this agent applies |
| `tools:` | recommended | `[read, search, edit]` — no `execute`, no `web` |
| Body | yes | What the agent does, FSM data structure, constraints |

---

## 📂 Folder Structure

```
03_agents/
├── broken/         ← Agent with vague description and unrestricted tools
│   └── .github/agents/fsm-agent.agent.md
├── workspace/      ← Edit your fix HERE
│   └── .github/agents/fsm-agent.agent.md   ← UPDATE THIS
└── solution/       ← Reference answer
    └── .github/agents/fsm-agent.agent.md
```

---

## 🤖 How Custom Agents Work

```
.github/agents/fsm-agent.agent.md
```

1. **Discovery** — Copilot reads `description:` to decide when to auto-invoke the agent
2. **Invocation** — User types `@fsm-agent` in Copilot Chat, or Copilot triggers it automatically
3. **Execution** — Agent operates only with the tools listed in `tools:`

### FSM data structure (Python)

```python
fsm_data = {
    "states":      list[str],               # all state names
    "current":     str,                     # active state
    "transitions": list[tuple[str, str]],   # (src, dst) pairs
}
```

All transitions must appear as `(src, dst)` tuples in `fsm_data["transitions"]`.  
The full expected sequence:

```
BOOT → INIT → IDLE → RUNNING ⇄ IDLE
                    ↓
                  ERROR → RESET → IDLE
```

---

## ✅ Validate

Click **"Validate My Fix"** in the simulator.  
The validator checks for:
- `.github/agents/*.agent.md` exists
- `description:` present and specific (≥ 20 chars)
- `tools:` present, `execute` and `web` not included
- Body contains: `fsm`, `transition`, `simulator`
