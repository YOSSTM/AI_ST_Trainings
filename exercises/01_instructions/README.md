# Exercise 01 — `copilot-instructions.md` & `applyTo`

> **Concept:** Two config files that tell Copilot what your project is and where rules apply.

---

## 🔴 The Problem

The board is in chaos:
- LEDs named `led1`, `led2` (generic, not project-specific)
- UART shows Python errors and missing context
- FSM uses `state1`, `state2` instead of `BOOT`, `INIT`, `RUNNING`

**Root cause:** Copilot has no project context — no instructions file, no scope.  
It generated generic Python code without knowing this is a Python/Streamlit simulator.

---

## 🎯 Your Task

### Part A — Global instructions

Create the file:
```
exercises/01_instructions/workspace/.github/copilot-instructions.md
```

This file is loaded automatically for **every** Copilot interaction in your repo.  
Use it to tell Copilot:
- Language and framework: Python 3, Streamlit, Plotly
- Board module structure and naming conventions
- Simulator architecture patterns

### Part B — Scoped instructions

Edit the file:
```
exercises/01_instructions/workspace/.github/instructions/simulator.instructions.md
```

Add an `applyTo` front-matter field to restrict the instructions to simulator Python files:

```yaml
---
applyTo: "simulator/**/*.py"
---
```

Without `applyTo`, instructions bleed into test files, notebooks, and CI configs.

---

## 📂 Folder Structure

```
01_instructions/
├── broken/         ← Missing / vague versions (for reference)
│   ├── .github/copilot-instructions.md
│   └── .github/instructions/simulator.instructions.md
├── workspace/      ← Edit your fix HERE
│   ├── .github/copilot-instructions.md              ← Part A
│   └── .github/instructions/simulator.instructions.md  ← Part B
└── solution/       ← Reference answer
    ├── .github/copilot-instructions.md
    └── .github/instructions/simulator.instructions.md
```

---

## ✅ Validate

Click **"Validate My Fix"** in the simulator.  
The validator checks:
- `copilot-instructions.md` mentions: `python`, `streamlit`, `board`, `naming`, `simulator`
- `simulator.instructions.md` has `applyTo` scoped to `simulator/**/*.py`

---

## 💡 Key Insights

| File | Scope | When active |
|------|-------|-------------|
| `copilot-instructions.md` | Whole repo | Every Copilot interaction |
| `*.instructions.md` + `applyTo` | Specific files/paths | Only when Copilot works on matching files |

`applyTo` uses glob patterns — `simulator/**/*.py` means only Python files under the `simulator/` tree.
