# Exercise 02 — Prompt Files (`.prompt.md`)

> **Concept:** Writing structured, reusable prompts that give Copilot precise generation instructions.

---

## 🔴 The Problem

The UART console is outputting garbled data — buffer overflow, truncated messages, raw hex dumps.

A developer asked Copilot: *"write a uart handler"* — one vague line.  
Copilot had no idea about:
- The expected message format
- Buffer size limits
- Which HAL API to use
- Error handling requirements

Result: broken UART handler that crashes the board.

---

## 🎯 Your Task

Create the file:
```
exercises/02_prompts/workspace/.github/prompts/uart_handler.prompt.md
```

A `.prompt.md` is a **reusable prompt template** that anyone on the team can invoke.  
It should describe **exactly** what Copilot needs to generate.

---

## 📂 Folder Structure

```
02_prompts/
├── broken/         ← The vague prompt (for reference)
│   └── .github/prompts/uart_handler.prompt.md
├── workspace/      ← Write your fix HERE
│   └── .github/prompts/uart_handler.prompt.md   ← CREATE THIS
└── solution/       ← Reference answer
    └── .github/prompts/uart_handler.prompt.md
```

---

## 🔧 What a Good Prompt File Looks Like

```markdown
---
mode: edit
description: Generate UART message handler for STM32 HAL
---

Generate a C function `UART_LogMessage(LogLevel_t level, const char *msg)`
that:
- Uses `HAL_UART_Transmit(&huart2, buf, len, HAL_MAX_DELAY)`
- Formats output as: `[LEVEL]  message\r\n`
- Uses a 64-byte local buffer with `snprintf`
- Returns `HAL_StatusTypeDef`
```

---

## ✅ Validate

Click **"Validate My Fix"** in the simulator.  
The validator checks that your prompt file mentions: `uart`, `format`, `message`, `HAL_UART`.
