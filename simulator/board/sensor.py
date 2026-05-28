"""
Sensor chart renderer — returns a Plotly figure.
"""
import plotly.graph_objects as go
import numpy as np


def make_sensor_chart(sensor_data: dict) -> go.Figure:
    """
    sensor_data keys:
        temp_values : list[float]   — temperature readings (°C)
        adc_values  : list[int]     — raw ADC counts (0-4095)
        label       : str           — sensor identifier
    """
    temp_values = [v for v in sensor_data.get("temp_values", []) if v is not None]
    adc_values = sensor_data.get("adc_values", [])
    label = sensor_data.get("label", "Sensor")

    x_temp = list(range(len(temp_values)))
    x_adc = list(range(len(adc_values)))

    fig = go.Figure()

    # Temperature trace
    if temp_values:
        fig.add_trace(go.Scatter(
            x=x_temp,
            y=temp_values,
            mode="lines+markers",
            name="Temp (°C)",
            line=dict(color="#ff8800", width=2),
            marker=dict(size=3, color="#ff8800"),
            yaxis="y",
        ))

    # ADC trace — scaled to 0-100 % for overlay
    if adc_values:
        scaled_adc = [v / 40.95 for v in adc_values]
        fig.add_trace(go.Scatter(
            x=x_adc,
            y=scaled_adc,
            mode="lines",
            name="ADC %",
            line=dict(color="#4488ff", width=1, dash="dot"),
            yaxis="y2",
        ))

    fig.update_layout(
        paper_bgcolor="#0a0a14",
        plot_bgcolor="#0d0d1a",
        font=dict(color="#778899", family="Courier New", size=9),
        margin=dict(l=40, r=35, t=30, b=20),
        height=175,
        title=dict(
            text=f"◈ SENSOR — {label}",
            font=dict(size=10, color="#77aacc", family="Courier New"),
            x=0,
        ),
        legend=dict(
            font=dict(size=8),
            bgcolor="rgba(0,0,0,0)",
            x=0.01, y=0.99,
        ),
        xaxis=dict(
            gridcolor="#111822",
            zerolinecolor="#1a2a3a",
            tickfont=dict(size=8),
        ),
        yaxis=dict(
            gridcolor="#111822",
            zerolinecolor="#1a2a3a",
            tickfont=dict(size=8),
            title=dict(text="°C", font=dict(size=8)),
        ),
        yaxis2=dict(
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(size=8),
            title=dict(text="ADC %", font=dict(size=8)),
            range=[0, 120],
        ),
    )
    return fig
