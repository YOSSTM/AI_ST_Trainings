"""
GPIO / LED panel renderer.
Returns raw HTML with CSS animations — use with st.components.v1.html().
"""


def render_led_panel(leds: list) -> str:
    """
    Render LED strip as animated HTML.

    Each LED dict:
        id    : str   — label shown below the LED
        color : str   — 'red' | 'green' | 'blue' | 'yellow' | 'orange' | 'white'
        on    : bool  — lit or dark
        blink : str   — None | 'slow' | 'fast'
    """
    COLORS = {
        "red":    {"on": "#ff2222", "glow": "#ff0000"},
        "green":  {"on": "#22ff44", "glow": "#00ff22"},
        "blue":   {"on": "#2255ff", "glow": "#0033ff"},
        "yellow": {"on": "#ffee00", "glow": "#ffcc00"},
        "orange": {"on": "#ff8800", "glow": "#ff6600"},
        "white":  {"on": "#ffffff", "glow": "#cccccc"},
    }

    led_items = []
    for led in leds:
        c = COLORS.get(led.get("color", "red"), COLORS["red"])
        on = led.get("on", False)
        blink = led.get("blink")
        label = led.get("id", "LED")

        if not on:
            style = "background:#1a1a1a;box-shadow:none;border:1px solid #333;"
            anim = ""
        else:
            style = (
                f"background:{c['on']};"
                f"box-shadow:0 0 10px {c['glow']},0 0 22px {c['glow']}55;"
                f"border:1px solid {c['on']};"
            )
            if blink == "fast":
                anim = "animation:led-blink .35s ease-in-out infinite;"
            elif blink == "slow":
                anim = "animation:led-blink 1.4s ease-in-out infinite;"
            else:
                anim = ""

        led_items.append(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:5px;">
          <div style="width:26px;height:26px;border-radius:50%;{style}{anim}"></div>
          <span style="color:#778899;font-size:9px;font-family:'Courier New',monospace;
                        text-align:center;max-width:72px;word-break:break-all;
                        line-height:1.2;">{label}</span>
        </div>""")

    return f"""<!DOCTYPE html><html><head><style>
@keyframes led-blink {{
  0%,100% {{ opacity:1; }}
  50%     {{ opacity:0.07; }}
}}
body {{ margin:0; background:#0d1f0d; }}
</style></head><body>
<div style="background:#0d1f0d;border:1px solid #1e3e1e;border-radius:8px;padding:14px 18px;">
  <div style="color:#55cc77;font-family:'Courier New',monospace;font-size:11px;
              font-weight:bold;letter-spacing:3px;margin-bottom:12px;">
    ◈ GPIO / LED PANEL
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:22px;align-items:flex-start;">
    {''.join(led_items)}
  </div>
</div>
</body></html>"""
