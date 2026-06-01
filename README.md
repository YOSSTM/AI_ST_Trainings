# 🔲 VirtualBoard Training

> Master GitHub Copilot's advanced features through hands-on embedded systems simulation — no hardware required.

---

## 🎯 What You'll Learn

| Exercise | Concept | What Breaks Without It |
|----------|---------|------------------------|
| 01 | `copilot-instructions.md` | Copilot generates Python instead of embedded C |
| 02 | `.prompt.md` files | UART output is garbage — prompts are too vague |
| 03 | Agent mode | FSM is stuck — agent can't navigate the codebase |
| 04 | Skills | Sensor reads -273°C — no domain knowledge |
| 05 | Capstone | The whole board is dead |

---

## 🚀 Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run simulator/app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🗺️ How It Works

```
Select exercise → Board is BROKEN visually
      ↓
Read the mission → Understand what's wrong
      ↓
Fix the Copilot config in VS Code
      ↓
Click Validate → Board comes ALIVE
      ↓
"Correction" mode → See the diff explained
```

### Three Modes

| Mode | Purpose |
|------|---------|
| **Trainee** | Work through exercises step by step |
| **Demo** | Trainer shows the fully working board |
| **Correction** | Side-by-side broken vs fixed comparison |

---

## 📁 Structure

```
exercises/
├── 01_instructions/     ← Fix copilot-instructions.md
│   ├── README.md        ← Exercise brief
│   ├── broken/          ← The bad config (for reference)
│   ├── workspace/       ← Edit your fix HERE
│   └── solution/        ← Reference answer
├── 02_prompts/          ← Fix the .prompt.md file
├── 03_agents/           ← Configure agent context
├── 04_skills/           ← Write a Copilot skill
└── 05_capstone/         ← Fix everything!

simulator/               ← The Streamlit web app
├── app.py               ← Entry point
├── board/               ← Simulator components
└── exercises/           ← Exercise configs & board states
```

---

## 🧪 Running Each Exercise

1. **Launch** the simulator: `streamlit run simulator/app.py`
2. **Select** an exercise from the top dropdown
3. **Read** the mission panel on the left — the board is broken!
4. Open the matching `exercises/0X_*/workspace/` folder in VS Code
5. **Fix** the Copilot config file described in the mission
6. Click **✅ Validate My Fix** — watch the simulator come alive
7. Switch to **Correction** mode to see the full explanation

---

*Built for Embedded SW engineers learning GitHub Copilot — ACI ST Training*
