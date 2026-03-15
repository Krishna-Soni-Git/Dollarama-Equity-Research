# Dollarama Inc. (DOL.TO) — Equity Research Dashboard

> **Course:** MBAN5570 — Equity Research Analytics
> **Authors:** Soni & Warner (2025)
> **Recommendation:** 🟢 **BUY** | Target: **CAD $212.06** | Upside: **+9.5%**
> **Data:** Live from Yahoo Finance — auto-loads on startup, no files needed

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

Open **http://localhost:8501** in your browser.

---

## Pulling the Latest Code After Cloning

```bash
# Pull latest changes
git checkout main
git pull origin main

# Reinstall if dependencies changed
pip install -r requirements.txt

# Run
streamlit run dollarama_research.py
```

### If you have local changes to keep

```bash
git stash          # save your changes
git pull origin main
git stash pop      # restore your changes on top
```

### Preview what changed before pulling

```bash
git fetch origin
git log HEAD..origin/main --oneline
git pull origin main
```

---

## Project Structure

```
dollarama-equity-research/
│
├── dollarama_research.py        # Main Streamlit dashboard (~2,560 lines)
├── dollarama_data_pull.py       # Optional: exports Yahoo Finance data to CSV
├── requirements.txt             # Python dependencies
├── .gitignore                   # Excludes venv, .env, __pycache__, etc.
├── README.md                    # This file
│
└── .streamlit/
    └── config.toml              # Streamlit theme config (light/dark default)
```

---

## Theme Support (Light & Dark)

The dashboard fully supports both Streamlit light and dark modes and **auto-adapts** when you switch.

### Setting the default theme

The `.streamlit/config.toml` file controls which theme loads by default:

```toml
# .streamlit/config.toml

[theme]
base = "light"               # Change to "dark" for dark mode default
primaryColor = "#9A7B2F"
backgroundColor = "#F8F9FA"
secondaryBackgroundColor = "#F1F3F5"
textColor = "#111827"
font = "sans serif"
```

To switch to dark by default, change `base = "light"` to `base = "dark"`. Users can also switch at any time using the ☰ menu → Settings in the Streamlit interface.

### How theme adaptation works

- **Sidebar background** — switches between `#F1F3F5` (light) and `#0E1117` (dark) automatically via JavaScript
- **Button text** — `#374151` on light, `#E2E8F0` on dark — always readable
- **Charts** — use transparent backgrounds that inherit the page colour
- **Inline text** — uses `color:inherit` to follow Streamlit's active theme

---

## Dashboard Tabs

Navigate using the sidebar buttons on the left:

| # | Tab | What It Shows |
|---|-----|--------------|
| 1 | 📊 Performance | Revenue, EBITDA, margins, EPS, SSS, store count FY2021–2025 |
| 2 | 💰 ROIC & Capital | ROIC vs WACC spread, FCF, buybacks, share count |
| 3 | 🏢 Peer Comps | Dollarama vs Dollar Tree vs Dollar General + analytical report |
| 4 | 💵 Valuation & DCF | Live DCF model, EV/EBITDA comps, sensitivity heatmap |
| 5 | 🎲 Monte Carlo | 5,000-path simulation, probability distribution, tornado chart |
| 6 | ⚠️ Risk & Moat | Competitive moat radar, risk matrix (bubble chart), risk register |
| 7 | 🔭 Forward Outlook | FY2026–2028 revenue, EPS, and store count forecasts |
| 8 | 📅 FY2025 Partial | Quarterly bridge Q1–Q4 FY2025 |
| 9 | 🤖 ML — Price Model | Linear Regression on MA + RSI features (Tutorial 5) |
| 10 | 💬 NLP — Sentiment | N-gram frequency + polarity scoring on earnings calls (Tutorial 4) + Section 2.C |
| 11 | 🗃️ Raw Data | Full audit trail — all raw columns and derived metrics |

---

## Interactive Controls

The **Valuation & DCF** and **Monte Carlo** tabs have live sliders built directly into each tab:

| Slider | Default | Tab |
|--------|---------|-----|
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

Peer company data uses **verified FY2025 SEC 10-K filings** — not Yahoo Finance's live peer feed, which returns partial/incorrect annual data.

| | DLTR (USD) | DG (USD) |
|--|--|--|
| Revenue | $30,607M | $40,612M |
| EBITDA Margin | 11.9% | 9.6% |
| ROIC | 13.6% | 15.2% |
| EV/EBITDA | 6.5× | 7.4× |
| Stock price | $65 USD → CAD $93.60 | $73 USD → CAD $105.12 |

> **Note on DLTR:** Net income of −$4,268M reflects a one-time goodwill impairment write-down on the Family Dollar acquisition — not an operational loss. Compare margins and EBITDA for a fair picture. Prices converted at USD/CAD 1.44 (Bank of Canada, Feb 2025 average).

---

## Contributing

```bash
# Create your own branch
git checkout -b feature/your-name-changes

# Make changes, then commit and push
git add .
git commit -m "Add: short description of change"
git push origin feature/your-name-changes

# Open a Pull Request on GitHub
```

### Adding a new tab

1. Add an entry to the `_NAV` list in the sidebar section
2. Add an `if _tab == N:` block in the tab content section
3. Increment `active_tab` range as needed

### Coding conventions

- All Dollarama figures in **CAD millions** unless labelled
- Peer figures in **USD millions**
- Column names follow Compustat style: `revt`, `ni`, `epspx`, `at`, `lct`, `che`, etc.
- All derived metrics computed in `process_dol()` — add new metrics there
- Colours: `GOLD="#9A7B2F"`, `GREEN="#1A6B45"`, `BLUE="#1D5FA0"`, `RED="#B91C1C"`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'X'` | Run `pip install -r requirements.txt` |
| `ModuleNotFoundError: matplotlib` | Run `pip install matplotlib>=3.7.0` |
| `streamlit: command not found` | Run `python -m streamlit run dollarama_research.py` |
| Sidebar buttons invisible in dark mode | Refresh the page — JS theme watcher re-applies colours within 1.5s |
| Yahoo Finance timeout or empty data | Restart the app — Yahoo rate-limits repeated requests |
| Charts look wrong on dark mode | Add `.streamlit/config.toml` to your project folder (see Theme Support above) |
| `sklearn` not found | Run `pip install scikit-learn>=1.3.0` |
| `yfinance` install fails (C compiler error) | Your pip installed yfinance 1.x — run `pip install "yfinance>=0.2.50,<1.0.0"` |
| Port already in use | Run `streamlit run dollarama_research.py --server.port 8502` |
| Peer data looks wrong | Expected — DLTR/DG always use verified 10-K fallback, not live Yahoo data |

---

## Dependencies

| Package | Min Version | Latest (Mar 2026) | Used For |
|---------|------------|-------------------|---------|
| streamlit | 1.40.0 | 1.55.0 | Dashboard framework, sidebar nav, widgets |
| plotly | 5.20.0 | 6.6.0 | All interactive charts |
| pandas | 2.2.0 | 3.0.1 | Data loading, transformation, tables |
| numpy | 1.26.0 | 2.4.3 | Numerical computing, Monte Carlo simulation |
| matplotlib | 3.7.0 | 3.10.8 | Colour gradients in DataFrames (`cmap="Greens"`) |
| yfinance | 0.2.50 (`<1.0.0`) | 0.2.66 stable | Live DOL.TO financial data |
| scikit-learn | 1.3.0 | 1.8.0 | Linear Regression in ML tab (Tutorial 5) |
| python-dotenv | 1.0.0 | 1.2.2 | Optional — loads `.env` for local config |

> **Why `yfinance<1.0.0`?** yfinance 1.x introduced `curl_cffi` as a dependency, which requires a C compiler to install. This fails silently on Windows machines without Visual Studio Build Tools and on older macOS without Xcode Command Line Tools. Version 0.2.x has no native compilation requirements and installs cleanly everywhere.

---

## Known Data Notes

1. **EBITDA definition** — Dashboard derives EBITDA as `(Gross Profit − SG&A) + D&A` from Yahoo Finance line items. Dollarama's press releases report EBITDA directly, which can differ by ~$100–160M due to Yahoo's line item reclassifications.

2. **Peer prices in CAD** — DLTR and DG stock prices are converted from USD to CAD at 1.44 (Bank of Canada February 2025 average). Ratios (EV/EBITDA, P/E, margins) are unaffected.

3. **FY2021 data** — Yahoo Finance returns at most 4 years of annual data. FY2021 is backfilled from verified Dollarama annual report values hardcoded in `FALLBACK_DOL`.

4. **DLTR loss** — Dollar Tree's FY2025 net loss of −$4,268M is entirely from a goodwill impairment on the Family Dollar acquisition, not operational performance. Always flag this when presenting the peer comparison.

---

> ⚠️ This is an academic project for MBAN5570. Nothing here constitutes financial advice.

*Last updated: March 2026 · Soni & Warner*