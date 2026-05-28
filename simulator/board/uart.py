"""
UART console renderer.
Returns raw HTML — use with st.components.v1.html().
"""


def render_uart_console(uart_data: dict) -> str:
    """
    uart_data keys:
        messages : list[str]
        baud     : int
    """
    messages = uart_data.get("messages", [])
    baud = uart_data.get("baud", 115200)

    lines_html = []
    for msg in messages:
        ml = msg.lower()
        if "[error]" in ml or "fault" in ml or "segfault" in ml or "undefined" in ml:
            color = "#ff4455"
        elif "[warn]" in ml or "overflow" in ml or "warn" in ml:
            color = "#ffaa00"
        elif "[info]" in ml:
            color = "#44ff88"
        elif "[debug]" in ml:
            color = "#88aaff"
        elif msg.startswith("0x") or ("0x" in msg and len(msg) < 30):
            color = "#ff6666"   # raw hex dump → clearly broken
        elif "print(" in ml or "typeerror" in ml or "nameerror" in ml:
            color = "#ff7755"   # Python errors in embedded context = wrong
        else:
            color = "#aabbcc"

        lines_html.append(
            f'<div style="color:{color};margin:1px 0;white-space:pre;">{msg}</div>'
        )

    return f"""<!DOCTYPE html><html><head><style>
@keyframes cursor-blink {{
  0%,100% {{ opacity:1; }}
  50%     {{ opacity:0; }}
}}
body {{ margin:0; background:#0a0a14; }}
</style></head><body>
<div style="background:#0a0a14;border:1px solid #1a2a4a;border-radius:8px;padding:12px 14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <span style="color:#5577ff;font-family:'Courier New',monospace;font-size:11px;
                 font-weight:bold;letter-spacing:3px;">◈ UART CONSOLE</span>
    <span style="color:#334466;font-family:'Courier New',monospace;font-size:10px;">
      {baud:,} baud
    </span>
  </div>
  <div style="background:#05050e;border-radius:4px;padding:10px 12px;
              height:115px;overflow-y:auto;
              font-family:'Courier New',monospace;font-size:11px;line-height:1.65;">
    {''.join(lines_html)}
    <span style="color:#44ff88;animation:cursor-blink 1s infinite;">█</span>
  </div>
</div>
</body></html>"""
