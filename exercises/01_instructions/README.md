# Exercise 01 — `copilot-instructions.md`

> **Concept:** Teaching Copilot your tech stack with a persistent instructions file.

---

## 🔴 The Problem

Open the simulator and look at the board — it's in chaos:
- LEDs are named `led1`, `led2` (generic, not embedded)
- UART console shows Python errors
- Sensor reads **-273 °C** (absolute zero)
- FSM uses `state1`, `state2` instead of `BOOT`, `INIT`, `RUNNING`...

**Root cause:** Copilot has no idea this is an embedded project. It generated generic Python code.

---

## 🎯 Your Task

Create the file:
```
exercises/01_instructions/workspace/.github/copilot-instructions.md
```

This file is loaded automatically by GitHub Copilot for **every interaction** in your repo.  
Use it to tell Copilot:
- Target MCU and language (STM32F4, C, HAL library)
- Naming conventions (`GPIO_LED_STATUS`, `UART_Send()`)
- Common peripheral APIs
- Project architecture patterns

---

## 📂 Folder Structure

```
01_instructions/
├── broken/         ← The bad version (for reference only)
│   └── .github/copilot-instructions.md
├── workspace/      ← Edit your fix HERE
│   └── .github/copilot-instructions.md   ← CREATE THIS
└── solution/       ← Reference answer (try first!)
    └── .github/copilot-instructions.md
```

---

## ✅ Validate

When done, click **"Validate My Fix"** in the simulator.  
The validator checks that your file mentions: `embedded`, `GPIO`, `UART`, `naming`, `convention`.

---

## 💡 Key Insight

`copilot-instructions.md` is your **AI coding style guide**.  
It applies to the entire repo, for every developer, for every Copilot chat.  
One file → consistent, context-aware suggestions across the whole team.
