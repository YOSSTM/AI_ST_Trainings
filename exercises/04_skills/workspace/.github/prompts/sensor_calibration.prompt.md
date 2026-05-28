---
description: TODO — TMP36 sensor calibration skill (Python)
---

# TODO: Write a Python sensor calibration skill here.
#
# Include:
#   - Function signature: convert_adc_to_temperature(adc_raw, vref=3.3, bits=12) -> float
#   - ADC to temperature formula (TMP36, Vref=3.3V, 12-bit):
#       voltage = (adc_raw / 4095.0) * 3.3
#       temp_c  = (voltage - 0.5) / 0.01
#   - Range validation: return float('nan') if outside [-40, 125] °C
#   - Module location: simulator/board/sensor.py
#
# See solution/ for the complete reference skill.
