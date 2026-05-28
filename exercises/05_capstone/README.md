# Exercise 05 — Capstone

> **Concept:** Putting it all together — all Copilot configs working in harmony.

---

## 🔴 The Problem

**The board is completely dead.** Every single module is failing.

A new developer joined the team and deleted all the Copilot config files  
*"to start fresh with Copilot"*. Copilot regenerated everything from scratch  
with zero context. Total failure across all systems.

---

## 🎯 Your Task

Recreate all the Copilot configs in:
```
exercises/05_capstone/workspace/.github/
```

You need:

| File | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Embedded context, naming, architecture |
| `.github/prompts/uart_handler.prompt.md` | UART message handler generation |
| `.github/prompts/sensor_calibration.prompt.md` | ADC/TMP36 calibration skill |

---

## 📂 Your Workspace

```
05_capstone/
├── README.md               ← This file
└── workspace/
    └── .github/
        ├── copilot-instructions.md            ← CREATE/UPDATE
        └── prompts/
            ├── uart_handler.prompt.md         ← CREATE
            └── sensor_calibration.prompt.md   ← CREATE
```

---

## 💡 Strategy

1. Go back to **Correction mode** on each exercise (01–04) to review what works
2. Copy the best parts of your previous workspace fixes
3. Combine them into this workspace folder
4. Click **Validate** — the checker requires both `copilot-instructions.md`  
   and at least one prompt file with embedded content

---

## ✅ Validate

Click **"Validate My Fix"** in the simulator.  
Checks: instructions file with embedded keywords + at least one prompt with UART or sensor content.

---

## 🏆 Completion

When the board comes back to life, you've demonstrated mastery of:

- **`copilot-instructions.md`** — persistent project context
- **`.prompt.md`** — reusable, structured generation prompts
- **Agent mode** — codebase-aware autonomous editing
- **Skills** — domain expertise encoded for Copilot

These four tools turn GitHub Copilot from autocomplete  
into a **context-aware embedded SW engineering partner**.
