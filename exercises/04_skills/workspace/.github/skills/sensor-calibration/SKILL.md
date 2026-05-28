---
name: sensor-calibration
description: "TODO — write a specific description (min 25 chars). Example: TMP36 ADC-to-temperature calibration for VirtualBoard simulator (Vref=3.3V, 12-bit ADC)"
---

<!-- TODO — Follow the 3-step process below to write this skill:

STEP 1 — Front-matter (required fields)
  name:        must match this folder name exactly: sensor-calibration
  description: be specific — Copilot uses this to decide when to load the skill

STEP 2 — When to use (triggers)
  Write a short paragraph or bullet list explaining when Copilot should apply this skill.
  Example: "Use when converting raw ADC readings from a TMP36 sensor to degrees Celsius."

STEP 3 — Procedure / domain knowledge
  Document the formula and the function signature Copilot should generate:
    - Sensor: TMP36
    - ADC resolution: 12-bit (0 to 4095)
    - Reference voltage: Vref = 3.3V
    - Formula:
        voltage = (adc_raw / (2**bits - 1)) * vref
        temp_c  = (voltage - 0.5) / 0.01
    - Function: convert_adc_to_temperature(adc_raw, vref=3.3, bits=12) -> float
    - Range check: return float('nan') if outside [-40, 125] °C

💬 Ask Copilot Chat to help: "Fill in this SKILL.md for TMP36 ADC calibration in Python"
See solution/ for a complete reference.
-->
