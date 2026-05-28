---
name: sensor-calibration
description: "TMP36 ADC-to-temperature calibration for VirtualBoard simulator — converts 12-bit ADC reading to °C (Vref=3.3V). Use when generating or reviewing sensor code in simulator/board/sensor.py."
---

# Sensor Calibration — TMP36

## When to Use

Apply this skill when:
- Implementing or reviewing `convert_adc_to_temperature()` in `simulator/board/sensor.py`
- Generating test data for the sensor chart (`make_sensor_chart()`)
- Debugging temperature readings that seem wrong (too high, too low, or `nan`)

## Formula

```
voltage (V) = (adc_raw / (2**bits - 1)) × vref
temp   (°C) = (voltage − 0.5) / 0.01
```

## Function Signature

```python
def convert_adc_to_temperature(
    adc_raw: int,
    vref: float = 3.3,
    bits: int = 12,
) -> float:
    """
    Convert a raw ADC reading to temperature in °C using TMP36 formula.

    Args:
        adc_raw: raw ADC integer (0 to 2**bits - 1)
        vref:    reference voltage in volts (default 3.3V)
        bits:    ADC resolution in bits (default 12 → 4095 max)

    Returns:
        Temperature in °C rounded to 1 decimal place.
        Returns float('nan') if result is outside [-40, 125] °C.
    """
    voltage = (adc_raw / (2**bits - 1)) * vref
    temp_c = (voltage - 0.5) / 0.01
    if temp_c < -40.0 or temp_c > 125.0:
        return float("nan")
    return round(temp_c, 1)
```

## Constraints

- No external dependencies — `math` stdlib only (for `isnan`)
- Range check: return `float('nan')` for readings outside [-40, 125] °C
- Module location: `simulator/board/sensor.py`
- Output feeds `make_sensor_chart(sensor_data)` as `temp_values: list[float]`
