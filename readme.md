# 📊 Dollarama Inc. (DOL.TO) — Equity Research Dashboard

> **Course:** MBAN5570 — Equity Research Analytics  
> **Authors:** Soni & Warner (2025)  
> **Recommendation:** 🟢 **BUY** | Target: **CAD $212.06** | Upside: **+9.5%**

---

## 🗂️ What This Is

A full-stack, interactive equity research dashboard for Dollarama Inc. built with Python and Streamlit. It covers all three sections of the MBAN5570 assignment:

| Section | What It Does | Where |
|---------|-------------|-------|
| **2.A Traditional Analysis** | 13 financial analysis components | Tabs 1–7 |
| **2.B AI-Assisted Analysis** | ML price model + NLP sentiment + Monte Carlo | Tabs 5, 9, 10 |
| **2.C Critical AI Evaluation** | What AI got right, wrong, accepted, discarded | Tab 10 → Section 2.C |

---

## 📁 Repository Structure

```
dollarama-equity-research/
│
├── dollarama_research.py          # Main Streamlit dashboard (2,400+ lines)
├── dollarama_data_pull.py         # Standalone Yahoo Finance → CSV exporter
├── requirements.txt               # Python dependencies
├── .gitignore                     # Excludes data files, caches, env files
├── README.md                      # This file
│
└── data/                          # Put your CSV exports here (git-ignored)
    ├── dollarama_annual_financials_*.csv
    ├── dollarama_derived_metrics_*.csv
    ├── dollarama_peers_*.csv
    └── dollarama_price_history_*.csv
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Krishna-Soni-Git/Dollarama-Equity-Research.git
cd dollarama-equity-research
```

### 2. Create a Virtual Environment (Recommended)

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the Data (Run Once)

```bash
python dollarama_data_pull.py
```

This creates a `data/` folder with four CSV files:
- `dollarama_annual_financials_[timestamp].csv` — FY2021–FY2025 financials
- `dollarama_derived_metrics_[timestamp].csv` — All computed ratios
- `dollarama_peers_[timestamp].csv` — Dollar Tree & Dollar General
- `dollarama_price_history_[timestamp].csv` — 5 years daily DOL.TO prices

> **Note:** `dollarama_data_pull.py` must be run locally or in Google Colab. Yahoo Finance blocks requests from most cloud/server environments.

### 5. Run the Dashboard

```bash
streamlit run dollarama_research.py
```

Open your browser to **http://localhost:8501**

---

## 📊 Dashboard Tabs

| # | Tab | What It Answers |
|---|-----|----------------|
| 1 | 📊 Performance | Revenue, margins, EPS, SSS, store growth FY2021–2025 |
| 2 | 💰 ROIC & Capital | ROIC vs WACC spread, FCF, buybacks, share count |
| 3 | 🏢 Peer Comps | Dollarama vs Dollar Tree vs Dollar General |
| 4 | 💵 Valuation & DCF | Live DCF, EV/EBITDA comps, sensitivity heatmap |
| 5 | 🎲 Monte Carlo | 10,000-path simulation, probability distribution |
| 6 | ⚠️ Risk & Moat | Moat radar, risk matrix, full risk register |
| 7 | 🔭 Forward Outlook | FY2026–2028 revenue, EPS, store count projections |
| 8 | 📅 FY2025 Partial | Quarterly breakdown Q1–Q4 vs prior year |
| 9 | 🤖 ML Price Prediction | Linear Regression on MA + RSI (Tutorial 5) |
| 10 | 💬 NLP Sentiment | N-gram + polarity scoring on earnings calls (Tutorial 4) + Section 2.C |
| 11 | 🗃️ Raw Data | Full audit trail — raw columns + all derived metrics |

---

## 🔢 Key Numbers (FY2025)

| Metric | Value |
|--------|-------|
| Revenue | $6,413M CAD |
| Net Income | $1,169M CAD |
| EPS | $4.16 (+16.9% YoY) |
| Gross Margin | 45.1% |
| EBITDA Margin | 31.1% |
| Net Margin | 18.2% |
| ROIC | 29.6% (vs WACC 7.8%) |
| Free Cash Flow | $1,397M |
| Net Debt / EBITDA | 1.08× |
| Store Count | 1,616 (target: 2,200 by 2034) |
| Current Price | ~CAD $193.63 |
| **Price Target** | **CAD $212.06 (+9.5%)** |

---

## 🛠️ Sidebar Controls

| Slider | Default | What It Changes |
|--------|---------|----------------|
| WACC | 7.8% | Discount rate for DCF + Monte Carlo |
| Terminal Growth Rate | 2.5% | Perpetual growth in terminal value |
| Stage 1 Revenue Growth | 7% | Years 1–5 FCF growth in DCF |
| Monte Carlo Paths | 5,000 | Number of simulation scenarios |

All charts and valuations update **live** as you move the sliders.

---

## 📂 Data Sources

| Source | Used For | Access |
|--------|----------|--------|
| Yahoo Finance (`yfinance`) | FY2022–2025 financials, 5yr price history | Free, no API key |
| Dollarama Annual Reports | FY2021 fallback + SSS + store count | Hardcoded in app |
| Analyst consensus | $212.06 target price | From whitepaper |

### Data Mode Options (Sidebar)

1. **CSV Files (Recommended)** — Upload the four CSVs from `dollarama_data_pull.py`. No internet needed at runtime. All numbers fully traceable.
2. **yfinance (Live)** — Fetches in real time. Requires internet. May fail on Streamlit Cloud.
3. **Built-in Fallback** — Hardcoded annual report data. Always works offline.

---

## 🤝 For Collaborators

### Cloning and Contributing

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/dollarama-equity-research.git
cd dollarama-equity-research

# Create your own branch
git checkout -b feature/your-name-changes

# After making changes
git add .
git commit -m "Add: brief description of your change"
git push origin feature/your-name-changes

# Open a Pull Request on GitHub to merge into main
```

### Environment Setup for Collaborators

```bash
# Install all dependencies
pip install -r requirements.txt

# Generate data files (run locally, not on cloud)
python dollarama_data_pull.py

# Launch dashboard
streamlit run dollarama_research.py
```

### What Each File Does

| File | Should You Edit It? | Notes |
|------|---------------------|-------|
| `dollarama_research.py` | ✅ Yes — main dashboard | All 11 tabs live here |
| `dollarama_data_pull.py` | ✅ Yes — data pipeline | Modify ticker, date range, peers here |
| `requirements.txt` | ✅ If you add a library | Pin versions for reproducibility |
| `data/*.csv` | ❌ No — auto-generated | Re-run data pull to refresh |
| `.env` | ❌ No — local only | Never commit API keys |

### Adding a New Tab

1. Add a tab label to the `st.tabs([...])` list (around line 894)
2. Add a `with tabs[N]:` block at the end of the file
3. Use the existing `show()`, `data_note()`, `base_layout()` helpers for consistent styling

### Coding Conventions

- All financial figures in **CAD millions** unless labeled otherwise
- Column names follow **Compustat-style** abbreviations (`revt`, `ni`, `epspx`, etc.)
- All derived metrics computed in `process_dol()` — add new metrics there
- Dark theme colours: `BG="#0E0E1A"`, `GOLD="#B8943A"`, `GREEN="#3D9E6A"`

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Yahoo Finance 403 error | Use CSV mode — run `dollarama_data_pull.py` locally first |
| Blank charts on Streamlit Cloud | Switch data mode to "CSV Files" and upload CSVs in sidebar |
| `streamlit: command not found` | Run `python -m streamlit run dollarama_research.py` |
| CSV upload not working | Ensure files are the exact output of `dollarama_data_pull.py` |
| Port already in use | Run `streamlit run dollarama_research.py --server.port 8502` |

---

## 📦 Dependencies

```
streamlit>=1.32.0
plotly>=5.20.0
pandas>=2.0.0
numpy>=1.26.0
yfinance>=0.2.38
python-dotenv>=1.0.0
```

Full pinned versions in `requirements.txt`.

---

## ⚠️ Known Data Discrepancies

These are documented differences between the dashboard and the whitepaper — all understood and explained:

1. **EBITDA** — Dashboard uses Yahoo Finance derivation (`Gross Profit − SG&A + D&A`). Whitepaper uses Dollarama's directly reported EBITDA from press releases. Difference: ~$100–160M. Both are valid methodologies.

2. **Total Debt** — Whitepaper includes IFRS 16 lease liabilities (~$1.7–2.4B). Dashboard shows financial debt only (bank loans + bonds). This is a presentation choice, not an error.

3. **Valuation multiples** — Dashboard uses fiscal year-end stock price from Yahoo Finance. Whitepaper uses the snapshot price of $193.63 from a specific analysis date. Numbers will differ slightly.

4. **FCF Conversion ratio** — Whitepaper values in the FCF table appear inconsistently calculated. Dashboard uses the consistent formula: `FCF ÷ Net Income`.

---

## 📜 License & Academic Use

This project was developed for **MBAN5570 — Equity Research Analytics** at [Your Institution]. All financial data is sourced from public filings and Yahoo Finance.

> ⚠️ This is an academic project. Nothing in this dashboard constitutes financial advice.

---

*Last updated: March 2026 | Soni & Warner*