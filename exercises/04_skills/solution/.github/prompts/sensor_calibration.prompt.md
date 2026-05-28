---
mode: edit
description: TMP36 ADC-to-temperature calibration in Python (12-bit ADC, Vref=3.3V) for the VirtualBoard simulator
---

## Sensor: TMP36 — Python implementation (12-bit ADC, Vref = 3.3 V)

Generate the function `convert_adc_to_temperature()` in `simulator/board/sensor.py`.

### Formula

```
Voltage (V) = (adc_raw / (2**bits - 1)) × vref
Temp   (°C) = (voltage − 0.5) / 0.01
```

### Function signature

```python
def convert_adc_to_temperature(
    adc_raw: int,
    vref: float = 3.3,
    bits: int = 12,
) -> float:
    """
    Convert a raw ADC reading to temperature in °C using TMP36 formula.

    Args:
        adc_raw: raw ADC integer value (0 to 2**bits - 1)
        vref:    reference voltage in volts (default 3.3V)
        bits:    ADC resolution in bits (default 12)

    Returns:
        Temperature in °C rounded to 1 decimal place.
        Returns float('nan') if result is outside [-40, 125] °C.
    """
    ...
```

### Constraints

- No external dependencies — `math` stdlib only for `isnan`
- Range check: return `float('nan')` if `temp_c < -40.0 or temp_c > 125.0`
- Round result to 1 decimal place: `round(temp_c, 1)`
- Add to `make_sensor_chart()` docstring: document accepted `sensor_data` keys
