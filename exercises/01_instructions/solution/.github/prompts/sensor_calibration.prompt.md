---
mode: edit
description: TMP36 ADC calibration in Python — converts 12-bit ADC reading to Celsius using Vref=3.3V, offset=0.5V
---

# Sensor Calibration Skill — TMP36 via ADC

Convert a raw 12-bit ADC reading to temperature in degrees Celsius.

## Formula

```python
def convert_adc_to_temperature(adc_value: int, vref: float = 3.3, resolution: int = 4096) -> float:
    """Convert 12-bit ADC reading to Celsius (TMP36, Vref=3.3V)."""
    voltage = (adc_value / resolution) * vref      # ADC counts → volts
    temperature = (voltage - 0.5) * 100.0           # TMP36 transfer function
    return round(temperature, 2)
```

## Module context

- Lives in `simulator/board/sensor.py`
- Output feeds `make_sensor_chart(sensor_data)` as `temp_values` list
- Use `[ERROR]` in `uart_data["messages"]` if calibration fails
