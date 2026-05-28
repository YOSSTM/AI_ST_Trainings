# Exercise 03 — Agent Mode

> **Concept:** Using agent mode to navigate and modify an entire codebase — and giving it the context it needs.

---

## 🔴 The Problem

The FSM is **stuck in INIT** and never transitions forward.

A developer used Copilot Agent and asked: *"complete the FSM transitions"*.  
But the agent had no map of the project — it generated isolated code without knowing:
- Where the FSM is implemented (`src/fsm.c`)
- That `FSM_AddTransition()` must be called to register transitions
- That transitions follow the pattern: `BOOT → INIT → IDLE → RUNNING`

Result: only the `BOOT → INIT` transition was generated, the rest is missing.

---

## 🎯 Your Task

Update the file:
```
exercises/03_agents/workspace/.github/copilot-instructions.md
```

Add an `## Architecture` section that describes:
- The FSM pattern and `FSM_AddTransition()` function
- File locations: `src/fsm.c`, `src/gpio.c`, `src/uart.c`
- The state sequence: `BOOT → INIT → IDLE → RUNNING ⇄ ERROR → RESET → IDLE`
- Agent-specific guidance (where to look, what pattern to follow)

---

## 📂 Folder Structure

```
03_agents/
├── broken/         ← Instructions with no architecture context
│   └── .github/copilot-instructions.md
├── workspace/      ← Edit your fix HERE
│   └── .github/copilot-instructions.md   ← UPDATE THIS
└── solution/       ← Reference answer
    └── .github/copilot-instructions.md
```

---

## 🤖 How Agent Mode Works

In agent mode, Copilot:
1. Reads `copilot-instructions.md` as its **project map**
2. Autonomously opens and reads files it thinks are relevant
3. Makes edits across multiple files in sequence

Without a good project map → the agent wanders, misses files, generates incomplete code.

---

## ✅ Validate

Click **"Validate My Fix"** in the simulator.  
The validator checks for: `fsm`, `state`, `transition`, `agent`, `codebase`.
