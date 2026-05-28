"""
FSM state-machine diagram renderer — returns a Plotly figure.
"""
import plotly.graph_objects as go
import numpy as np


def make_fsm_diagram(fsm_data: dict) -> go.Figure:
    """
    fsm_data keys:
        states      : list[str]
        current     : str            — highlighted state
        transitions : list[tuple]    — (src, dst) pairs
    """
    states = fsm_data.get("states", [])
    current = fsm_data.get("current", "")
    transitions = fsm_data.get("transitions", [])

    n = len(states)
    if n == 0:
        return go.Figure()

    # Place states in a circle
    angles = [2 * np.pi * i / n - np.pi / 2 for i in range(n)]
    pos = {s: (float(np.cos(a)) * 0.72, float(np.sin(a)) * 0.65)
           for s, a in zip(states, angles)}

    fig = go.Figure()

    # ── Transition arrows ─────────────────────────────────────────────────────
    R = 0.16  # approximate node radius in x-units
    for src, dst in transitions:
        if src not in pos or dst not in pos:
            continue
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        dx, dy = x1 - x0, y1 - y0
        dist = np.sqrt(dx ** 2 + dy ** 2)
        if dist < 1e-6:
            continue
        # Push arrow endpoints to node borders
        ax = x0 + dx / dist * R
        ay = y0 + dy / dist * R
        hx = x1 - dx / dist * R
        hy = y1 - dy / dist * R

        fig.add_annotation(
            x=hx, y=hy,
            ax=ax, ay=ay,
            axref="x", ayref="y",
            arrowhead=2,
            arrowcolor="#2a4a6a",
            arrowwidth=1.5,
            showarrow=True,
            text="",
        )

    # ── State nodes ────────────────────────────────────────────────────────────
    for state in states:
        x, y = pos[state]
        is_cur = state == current

        fill = "#cc4400" if is_cur else "#0a2235"
        border = "#ff6622" if is_cur else "#1a4a6a"
        lw = 2 if is_cur else 1
        txt_color = "#ffffff" if is_cur else "#88aacc"

        fig.add_shape(
            type="rect",
            x0=x - R, y0=y - 0.085,
            x1=x + R, y1=y + 0.085,
            fillcolor=fill,
            line=dict(color=border, width=lw),
        )
        fig.add_annotation(
            x=x, y=y,
            text=state,
            showarrow=False,
            font=dict(color=txt_color, size=9, family="Courier New"),
        )

    fig.update_layout(
        showlegend=False,
        paper_bgcolor="#0a0a14",
        plot_bgcolor="#0a0a14",
        xaxis=dict(visible=False, range=[-1.15, 1.15]),
        yaxis=dict(visible=False, range=[-0.95, 0.95], scaleanchor="x", scaleratio=1.0),
        margin=dict(l=10, r=10, t=34, b=10),
        height=210,
        title=dict(
            text=f"◈ FSM — Current state: <b>{current}</b>",
            font=dict(size=10, color="#88aacc", family="Courier New"),
            x=0,
        ),
    )
    return fig
