# Exercise 04 — Skills

> **Concept:** Writing reusable domain-knowledge prompts that give Copilot expertise it can't infer from code alone.

---

## 🔴 The Problem

The sensor is reading **998 °C** — the board triggered overheat protection and crashed.

Copilot was asked to implement ADC-to-temperature conversion.  
Without any domain knowledge about the TMP36 sensor, it did this:

```c
// What Copilot generated (WRONG):
float tempC = (float)HAL_ADC_GetValue(&hadc1);  // raw ADC count used directly!
```

The raw 12-bit ADC count is **0–4095**, not degrees Celsius.

---

## 🎯 Your Task

Create the file:
```
exercises/04_skills/workspace/.github/prompts/sensor_calibration.prompt.md
```

This prompt acts as a **reusable skill** that gives Copilot the domain knowledge  
to correctly convert ADC readings to temperature for the TMP36 sensor.

---

## 📂 Folder Structure

```
04_skills/
├── broken/         ← Missing skill (empty prompts folder)
├── workspace/      ← Create your skill HERE
│   └── .github/prompts/sensor_calibration.prompt.md   ← CREATE THIS
└── solution/       ← Reference answer
    └── .github/prompts/sensor_calibration.prompt.md
```

---

## 🔬 The Physics (TMP36 on STM32)

```
ADC raw  →  Voltage  →  Temperature

Voltage (V) = (ADC_raw / 4095.0) × Vref        where Vref = 3.3 V
Temp (°C)   = (Voltage − 0.5) / 0.01
```

Example: raw = 1287 → V = 1.037 V → Temp = 53.7 °C  
(Wait — that means room temperature raw ≈ 753… verify with your Vref!)

---

## ✅ Validate

Click **"Validate My Fix"** in the simulator.  
The validator checks for: `adc`, `calibr`, `vref`, `temperature`, `formula`.

---

## 💡 Key Insight

**Skills** are reusable prompts that encode domain knowledge.  
Unlike `copilot-instructions.md` (always active), skills are invoked on demand.  
They're perfect for: sensor calibration, communication protocol encoding, safety patterns, etc.
