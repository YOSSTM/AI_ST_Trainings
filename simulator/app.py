"""
VirtualBoard Training — Streamlit app entry point.

Run: streamlit run simulator/app.py
"""
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from board.gpio   import render_led_panel
from board.uart   import render_uart_console
from board.sensor import make_sensor_chart
from board.fsm    import make_fsm_diagram

from exercises.ex01 import EXERCISE as EX01
from exercises.ex02 import EXERCISE as EX02
from exercises.ex03 import EXERCISE as EX03
from exercises.ex04 import EXERCISE as EX04
from exercises.ex05 import EXERCISE as EX05

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VirtualBoard Training",
    page_icon="🔲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EXERCISES = {
    "01 — Copilot Instructions": EX01,
    "02 — Prompt Files":         EX02,
    "03 — Agent Mode":           EX03,
    "04 — Skills":               EX04,
    "05 — Capstone":             EX05,
}

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background:#0e0e1a; color:#cccccc; }
[data-testid="stHeader"]           { background:#09090f; }
[data-testid="stSidebar"]          { background:#09090f; }

.main-title {
    font-family:'Courier New',monospace;
    font-size:22px; font-weight:bold;
    color:#44ff88; letter-spacing:3px;
}
.section-hdr {
    font-family:'Courier New',monospace;
    font-size:12px; font-weight:bold;
    color:#4488ff; letter-spacing:2px;
    border-bottom:1px solid #1a2a4a;
    padding-bottom:5px; margin-bottom:10px;
}
.problem-box {
    background:#220a0a; border-left:3px solid #ff4444;
    padding:10px 12px; border-radius:4px;
    font-family:'Courier New',monospace; font-size:11px; color:#ff8888;
}
.status-row {
    display:flex; justify-content:space-between;
    align-items:center; margin-bottom:10px;
}
.chip-row { display:flex; gap:6px; flex-wrap:wrap; }
.chip {
    padding:2px 7px; border-radius:3px;
    font-family:'Courier New',monospace;
    font-size:10px; font-weight:bold;
}
.chip-pass { background:#0a2d1a; color:#44ff88; }
.chip-warn { background:#2d1e00; color:#ffaa00; }
.chip-fail { background:#2d0a0a; color:#ff5555; }
.badge {
    padding:3px 10px; border-radius:3px;
    font-family:'Courier New',monospace;
    font-size:11px; font-weight:bold; letter-spacing:2px;
}
.badge-pass    { background:#0a2d1a; color:#44ff88; border:1px solid #226633; }
.badge-fail    { background:#2d0a0a; color:#ff5555; border:1px solid #662222; }
.badge-partial { background:#2d1e00; color:#ffaa00; border:1px solid #664400; }
.errnote {
    color:#ff7744; font-family:'Courier New',monospace;
    font-size:10px; margin-bottom:8px;
}
.correction-label {
    font-family:'Courier New',monospace; font-size:11px;
    font-weight:bold; letter-spacing:1px;
    padding:4px 8px; border-radius:4px;
    margin-bottom:8px; display:inline-block;
}
.cl-broken { background:#2d0a0a; color:#ff5555; }
.cl-fixed  { background:#0a2d1a; color:#44ff88; }

/* Streamlit overrides */
div[data-testid="stExpander"] {
    border:1px solid #1a2a3a !important;
    border-radius:6px !important;
}
.stButton > button {
    font-family:'Courier New',monospace;
    font-weight:bold; border-radius:4px;
}
#MainMenu { visibility:hidden; }
footer    { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "validated" not in st.session_state:
    st.session_state.validated = {}

# ── Header ────────────────────────────────────────────────────────────────────
c_title, _, c_mode, c_ex = st.columns([3, 1, 1, 2])
with c_title:
    st.markdown('<div class="main-title">🔲 VirtualBoard Training</div>',
                unsafe_allow_html=True)
with c_mode:
    mode = st.selectbox("Mode", ["Trainee", "Demo", "Correction"],
                        label_visibility="collapsed", key="sel_mode")
with c_ex:
    ex_key = st.selectbox("Exercise", list(EXERCISES.keys()),
                          label_visibility="collapsed", key="sel_ex")

st.markdown('<hr style="border-color:#1a2a3a;margin:6px 0 14px 0;">',
            unsafe_allow_html=True)

ex = EXERCISES[ex_key]
is_validated = st.session_state.validated.get(ex_key, False)


# ── Board renderer ────────────────────────────────────────────────────────────
def render_board(board: dict) -> None:
    # Status bar
    status = board.get("status", {})

    def chip_class(v):
        return {"PASS": "chip-pass", "WARN": "chip-warn", "FAIL": "chip-fail"}.get(v, "chip-fail")

    chips_html = "".join(
        f'<span class="chip {chip_class(v)}">{k}: {v}</span>'
        for k, v in status.items()
    )
    all_pass = all(v == "PASS" for v in status.values())
    any_pass = any(v == "PASS" for v in status.values())
    if all_pass:
        badge_cls, badge_txt = "badge-pass", "BOARD OK"
    elif any_pass:
        badge_cls, badge_txt = "badge-partial", "PARTIAL"
    else:
        badge_cls, badge_txt = "badge-fail", "BOARD FAIL"

    st.markdown(
        f'<div class="status-row">'
        f'  <div class="chip-row">{chips_html}</div>'
        f'  <span class="badge {badge_cls}">{badge_txt}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if board.get("error_note"):
        st.markdown(
            f'<div class="errnote">⚠ {board["error_note"]}</div>',
            unsafe_allow_html=True,
        )

    # LED panel
    components.html(render_led_panel(board["leds"]), height=120, scrolling=False)

    # UART + Sensor side by side
    c1, c2 = st.columns(2)
    with c1:
        components.html(render_uart_console(board["uart"]), height=195, scrolling=False)
    with c2:
        st.plotly_chart(
            make_sensor_chart(board["sensor"]),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # FSM diagram
    st.plotly_chart(
        make_fsm_diagram(board["fsm"]),
        use_container_width=True,
        config={"displayModeBar": False},
    )


# ── Correction mode ───────────────────────────────────────────────────────────
if mode == "Correction":
    st.markdown(
        f'<div class="section-hdr">{ex["title"]} — CORRECTION VIEW</div>',
        unsafe_allow_html=True,
    )
    cb, cf = st.columns(2)
    with cb:
        st.markdown(
            '<span class="correction-label cl-broken">❌  BROKEN — bad config</span>',
            unsafe_allow_html=True,
        )
        render_board(ex["board_broken"])
    with cf:
        st.markdown(
            '<span class="correction-label cl-fixed">✅  FIXED — good config</span>',
            unsafe_allow_html=True,
        )
        render_board(ex["board_fixed"])

    with st.expander("🔍 Explanation — what changed?"):
        st.markdown(ex["explanation"])

# ── Trainee / Demo mode ───────────────────────────────────────────────────────
else:
    board = ex["board_fixed"] if (is_validated or mode == "Demo") else ex["board_broken"]

    col_left, col_right = st.columns([1, 2])

    # ── Left: mission panel ───────────────────────────────────────────────────
    with col_left:
        st.markdown(
            f'<div class="section-hdr">{ex["title"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'**Concept:** {ex["concept"]}')
        st.markdown("")

        if mode == "Demo":
            st.info("Demo mode — the board is fully operational.")
        else:
            st.markdown(ex["mission"])
            st.markdown("")

            if not is_validated:
                st.markdown(
                    f'<div class="problem-box">⚠ {ex["problem"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("")

            with st.expander("💡 Hints  *(try first!)*"):
                for i, h in enumerate(ex["hints"], 1):
                    st.markdown(f"**{i}.** {h}")

            with st.expander("📁 Files to edit"):
                for f in ex["files_to_edit"]:
                    st.code(f, language="")

            st.markdown("")

            if not is_validated:
                if st.button("✅  Validate My Fix",
                             use_container_width=True, type="primary"):
                    ok, msg = ex["validate"]()
                    if ok:
                        st.session_state.validated[ex_key] = True
                        st.success(msg)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.success("🎉 Exercise passed!")
                with st.expander("🔍 What changed?"):
                    st.markdown(ex["explanation"])
                if st.button("🔄 Reset exercise", use_container_width=True):
                    st.session_state.validated[ex_key] = False
                    st.rerun()

    # ── Right: simulator ──────────────────────────────────────────────────────
    with col_right:
        st.markdown(
            '<div class="section-hdr">VIRTUAL BOARD SIMULATOR</div>',
            unsafe_allow_html=True,
        )
        render_board(board)
