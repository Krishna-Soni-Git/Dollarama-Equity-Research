# Dollarama Inc. (DOL.TO) — Equity Research Dashboard

> **Course:** MBAN5570 — Equity Research Analytics
> **Authors:** Soni & Warner (2025)
> **Recommendation:** 🟢 **BUY** | Target: **CAD $212.06** | Upside: **+9.5%**
> **Data:** Live from Yahoo Finance (auto-loads on startup)

---

## What This Is

A fully interactive equity research dashboard for Dollarama Inc. built with Python and Streamlit. It covers the complete MBAN5570 assignment across 11 sidebar-navigated tabs:

| Section | Coverage | Tabs |
|---------|----------|------|
| 2.A Traditional Analysis | Business model, financials, valuation, peers, risk | 1–8 |
| 2.B AI-Assisted Analysis | ML price model, NLP sentiment, Monte Carlo simulation | 5, 9, 10 |
| 2.C Critical AI Evaluation | What AI got right, wrong, accepted, discarded | Tab 10 → Section 2.C |

---

## Quick Start

### 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/dollarama-equity-research.git
cd dollarama-equity-research
```

### 2 — Create a Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### 4 — Run the Dashboard

```bash
streamlit run dollarama_research.py
```

Open **http://localhost:8501** in your browser. The dashboard fetches live data from Yahoo Finance automatically — no data files needed.

---

## Pulling the Latest Code After Cloning

Once you have cloned the repo, use these commands to stay up to date:

```bash
# Switch to the main branch
git checkout main

# Pull the latest changes from GitHub
git pull origin main

# If dependencies have changed, reinstall them
pip install -r requirements.txt

# Run the dashboard
streamlit run dollarama_research.py
```

### If you have local changes you want to keep

```bash
# Save your local changes temporarily
git stash

# Pull the latest code
git pull origin main

# Restore your saved changes on top
git stash pop
```

### Check what changed before pulling

```bash
# See what commits are new on the remote
git fetch origin
git log HEAD..origin/main --oneline

# Then pull when ready
git pull origin main
```

---

## Project Structure

```
dollarama-equity-research/
│
├── dollarama_research.py      # Main Streamlit dashboard (2,300+ lines)
├── dollarama_data_pull.py     # Optional: exports Yahoo Finance data to CSV
├── requirements.txt           # Python dependencies (this file)
├── .gitignore                 # Excludes venv, .env, cache files
└── README.md                  # This file
```

---

## Dashboard Tabs

Navigate using the sidebar buttons on the left:

| # | Tab | What It Shows |
|---|-----|--------------|
| 1 | 📊 Performance | Revenue, EBITDA, margins, EPS, store count FY2021–2025 |
| 2 | 💰 ROIC & Capital | ROIC vs WACC spread, FCF, buybacks, share count |
| 3 | 🏢 Peer Comps | Dollarama vs Dollar Tree vs Dollar General + analytical report |
| 4 | 💵 Valuation & DCF | Live DCF model, EV/EBITDA comps, sensitivity heatmap |
| 5 | 🎲 Monte Carlo | 5,000-path simulation, probability distribution |
| 6 | ⚠️ Risk & Moat | Competitive moat radar, risk matrix, risk register |
| 7 | 🔭 Forward Outlook | FY2026–2028 revenue, EPS, and store count forecasts |
| 8 | 📅 FY2025 Partial | Quarterly bridge Q1–Q4 FY2025 |
| 9 | 🤖 ML — Price Model | Linear Regression on MA + RSI (Tutorial 5) |
| 10 | 💬 NLP — Sentiment | N-gram frequency + polarity scoring on earnings calls (Tutorial 4) |
| 11 | 🗃️ Raw Data | Full audit trail — all raw columns and derived metrics |

---

## Interactive Controls

The **Valuation & DCF** and **Monte Carlo** tabs have live sliders built directly into the tab (not the sidebar):

| Slider | Default | Where |
|--------|---------|-------|
| WACC (%) | 7.8% | Valuation & DCF, Monte Carlo |
| Terminal Growth (%) | 2.5% | Valuation & DCF, Monte Carlo |
| Stage 1 Revenue Growth (%) | 9.0% | Valuation & DCF, Monte Carlo |
| Simulation Paths | 5,000 | Monte Carlo only |

All charts and valuations update live as you move the sliders.

---

## Key Numbers (FY2025)

| Metric | Value |
|--------|-------|
| Revenue | $6,413M CAD |
| Net Income | $1,169M CAD |
| EPS | $4.16 CAD (+16.9% YoY) |
| EBITDA Margin | 31.1% |
| ROIC | 29.6% (vs WACC 7.8%) |
| Free Cash Flow | $1,397M CAD |
| Net Debt / EBITDA | 1.08× |
| Store Count | 1,616 (target: 2,200 by 2034) |
| Current Price | ~CAD $193.63 |
| **Price Target** | **CAD $212.06 (+9.5%)** |

---

## Peer Comparison Data

Peer company data (Dollar Tree and Dollar General) is sourced from verified FY2025 SEC 10-K filings — **not** from Yahoo Finance's live feed, which returns partial and unreliable peer data.

| | DLTR | DG |
|--|--|--|
| Revenue | $30,607M USD | $40,612M USD |
| EBITDA Margin | 11.9% | 9.6% |
| ROIC | 13.6% | 15.2% |
| EV/EBITDA | 6.5× | 7.4× |
| Stock price | $65 USD → CAD $93.60 | $73 USD → CAD $105.12 |

> **Note:** DLTR net income is -$4,268M due to a one-time goodwill impairment write-down on the Family Dollar acquisition — not an operational loss. Prices converted at USD/CAD 1.44 (Bank of Canada, Feb 2025).

---

## Contributing

```bash
# Create your own branch
git checkout -b feature/your-name-changes

# Make your changes, then commit
git add .
git commit -m "Add: short description of change"
git push origin feature/your-name-changes

# Open a Pull Request on GitHub to merge into main
```

### Adding a new tab

1. Add a label to the `_NAV` list in the sidebar section (~line 546)
2. Add `if _tab == N:` block at the end of the tab section
3. Increment the `active_tab` range check if needed

### Coding conventions

- All Dollarama figures in **CAD millions** unless noted
- Peer figures in **USD millions**
- Column names follow Compustat style: `revt`, `ni`, `epspx`, `at`, `lct`, `che`, etc.
- All derived metrics computed in `process_dol()` — add new metrics there
- Chart colours: `GOLD="#B8943A"`, `GREEN="#3D9E6A"`, `BLUE="#3A7EC0"`, `RED="#CC4444"`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `streamlit: command not found` | Run `python -m streamlit run dollarama_research.py` |
| Yahoo Finance timeout / empty data | Restart the app — Yahoo rate-limits heavy usage |
| Charts not rendering | Ensure `plotly>=6.0.0` — run `pip install --upgrade plotly` |
| `sklearn` not found | Run `pip install scikit-learn>=1.4.0` |
| Port already in use | Run `streamlit run dollarama_research.py --server.port 8502` |
| yfinance returns wrong peer data | Expected — peers always use verified 10-K fallback values |

---

## Dependencies

| Package | Min Version | Latest | Used For |
|---------|------------|--------|---------|
| streamlit | 1.45.0 | 1.55.0 | Dashboard framework |
| plotly | 6.0.0 | 6.6.0 | All interactive charts |
| pandas | 2.2.0 | 3.0.1 | Data manipulation |
| numpy | 1.26.0 | 2.4.3 | Numerical computing, Monte Carlo |
| yfinance | 0.2.50 | 1.2.0 | Live DOL.TO financial data |
| scikit-learn | 1.4.0 | 1.8.0 | ML tab Linear Regression |
| python-dotenv | 1.0.0 | 1.2.2 | Optional .env config loading |

---

## Known Data Notes

1. **EBITDA definition** — Dashboard uses Yahoo Finance derivation: `(Gross Profit − SG&A) + D&A`. Dollarama's press releases report EBITDA directly from their income statement, which differs by ~$100–160M. Both are valid; the difference comes from how Yahoo reclassifies line items.

2. **Peer prices in CAD** — DLTR and DG stock prices are converted from USD to CAD at the Bank of Canada February 2025 average rate of 1.44. EV/EBITDA and other ratios are unaffected (they are currency-neutral).

3. **FY2021 data** — Yahoo Finance only returns 4 years of annual data. FY2021 figures are backfilled from verified Dollarama annual report values.

---

> ⚠️ This is an academic project for MBAN5570. Nothing here constitutes financial advice.

*Last updated: March 2026 · Soni & Warner*