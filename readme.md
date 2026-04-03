# Dollarama Inc. (DOL.TO) — Equity Research Dashboard

> **Course:** MBAN5570 — Equity Research Analytics
> **Authors:** Soni & Warner (2025)
> **Version:** v6B — Aligned with Google Colab v6B
> **Recommendation:** 🟢 **BUY** | Target: **CAD $212** | Upside: **~25%** (live vs ~$173)
> **Data:** Live from Yahoo Finance — auto-loads on startup, no files needed

---

## What This Is

A fully interactive equity research dashboard for Dollarama Inc. (DOL.TO) built with Python and Streamlit. It covers the complete MBAN5570 assignment across **13 sidebar-navigated tabs** with three clearly labelled sections:

| Section | Coverage | Tabs |
|---------|----------|------|
| 2.A Traditional Analysis | Business model, financials, valuation, risk, IPO compounding | 01–08 |
| Live Valuation Demo | DCF live model + Monte Carlo simulation | 09–10 |
| 2.B / 2.C AI-Assisted & Critical Evaluation | ML price model, NLP sentiment, AI critical review | 11–13 |

---

## Quick Start

### 1 — Clone the Repository

```bash
git clone https://github.com/Krishna-Soni-Git/dollarama-equity-research.git
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

**Full 13-tab dashboard (recommended for complete presentation):**
```bash
streamlit run Dashboard.py
```

**4-tab live demo only (DCF, Monte Carlo, ML, NLP — for the 4-minute AI tools section):**
```bash
streamlit run dollarama_research.py
```

**No Python? Open the static HTML companion directly in any browser:**
```
dollarama_dashboard_alternative.html
```

Open **http://localhost:8501** in your browser (Streamlit files only).

---

## Pulling the Latest Code After Cloning

```bash
# Pull latest changes
git checkout main
git pull origin main

# Reinstall if dependencies changed
pip install -r requirements.txt

# Run
streamlit run Dashboard.py         # full dashboard
streamlit run dollarama_research.py # live demo only
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
├── Dashboard.py                       # Full 13-tab Streamlit dashboard (main file)
├── dollarama_research.py              # Condensed 4-tab live demo (DCF, Monte Carlo, ML, NLP)
├── dollarama_data_pull.py             # Optional: exports Yahoo Finance data to CSV
├── dollarama_dashboard_alternative.html  # Static HTML companion dashboard
├── requirements.txt                   # Python dependencies
├── readme.md                          # This file
├── .env                               # Local environment variables (not committed)
├── .gitignore                         # Excludes venv, .env, __pycache__, etc.
├── config.toml                        # Streamlit theme config (light/dark default)
│
├── Output/                            # Generated outputs (reports, exports)
│
├── Paper/
│   ├── dollarama_report_v6b.docx      # Full equity research white paper (v6B)
│   └── dollarama_whitepaper.docx      # Final submission white paper
│
└── PPT/
    └── dollarama_updated.pptx         # Presentation slide deck
```

### Which file to run

| File | Purpose | Command |
|------|---------|---------|
| `Dashboard.py` | Full 13-tab dashboard — use for **complete presentation** | `streamlit run Dashboard.py` |
| `dollarama_research.py` | 4-tab live demo — use for **4-minute AI tools demo** (DCF, Monte Carlo, ML, NLP) | `streamlit run dollarama_research.py` |
| `dollarama_dashboard_alternative.html` | Static HTML — opens in any browser, **no Python required** | Open in browser directly |

---

## Dashboard Tabs

Navigate using the **sidebar buttons** on the left. The sidebar also shows the live price pulled from Yahoo Finance and the BUY / $212 Target badge.

### Traditional Analysis (2.A)

| # | Tab | What It Shows |
|---|-----|--------------|
| 01 | Company Overview | Investment thesis, live KPIs, 5-year price chart with MA50/MA200, volume |
| 02 | Macro & Industry | BoC rate, CPI, CAD/USD, Porter's Five Forces, competitive landscape, peer revenue growth |
| 03 | Income Statement | Revenue, gross profit, EBIT, net income, EBITDA, margins, EPS, per-$100 breakdown FY2022–FY2026 |
| 04 | Balance Sheet | Assets, equity, debt, working capital, current ratio, asset composition FY2022–FY2026 |
| 05 | Cash Flow | Operating / investing / financing CF, FCF waterfall, CapEx intensity, FCF conversion |
| 06 | Financial Ratios | Profitability, ROA, liquidity, leverage heatmap, comprehensive ratio table |
| 07 | Valuation Multiples | Live P/E, EV/EBITDA vs sector benchmarks, peer comparison (DLTR, DG), composite signal |
| 08 | IPO Compounding | IPO-to-date CAGR since Oct 2009 at $17.00 CAD, $10K investment growth, 10% benchmark check |

### Live Valuation Demo

| # | Tab | What It Shows |
|---|-----|--------------|
| 09 | DCF Live Model | CAPM/WACC derivation table, 5-year FCF projection, Gordon Growth terminal value, dynamic sensitivity table centred on slider position |
| 10 | Monte Carlo | 5,000-path stochastic DCF simulation, histogram, CDF, probability boxes |

### AI-Assisted Analysis (2.B / 2.C)

| # | Tab | What It Shows |
|---|-----|--------------|
| 11 | ML Price Model | Linear regression on MA + RSI features, chronological 80/20 split, R², RMSE, data leakage critique (Tutorial 5) |
| 12 | NLP Sentiment | N-gram frequency, polarity & subjectivity by earnings call, deep-dive transcript highlighting (Tutorial 4) |
| 13 | AI Critical Review | Section 2.C — what AI got right, wrong, accepted, discarded, and the three integration principles |

---

## Interactive Sliders

All charts and valuations update live as you move the sliders.

### Tab 09 — DCF Live Model

| Slider | Default | Range |
|--------|---------|-------|
| WACC (%) | **5.5%** | 3.0% – 12.0% |
| Terminal Growth Rate (%) | **2.5%** | 1.0% – 4.0% |
| Stage 1 FCF Growth (%) | **8.0%** | 3.0% – 15.0% |

At defaults → **~$213 CAD** (+23% upside). Sensitivity table recentres on your slider position dynamically.

### Tab 10 — Monte Carlo

| Slider | Default | Range |
|--------|---------|-------|
| WACC mean (%) | **9.0%** | 5.0% – 12.0% |
| Terminal Growth mean (%) | **2.5%** | 1.0% – 4.0% |
| FCF Growth mean (%) | **8.0%** | 3.0% – 15.0% |
| Simulation Paths | **5,000** | 1,000 / 2,500 / 5,000 / 10,000 |

### Tab 11 — ML Price Model

| Slider | Default | Range |
|--------|---------|-------|
| MA window (days) | **10** | 5 – 30 |
| RSI window (days) | **14** | 7 – 21 |
| Test set (%) | **20%** | 10% – 40% |

### Tab 12 — NLP Sentiment

| Control | Default |
|---------|---------|
| Earnings call selector | FY2025 Annual |
| Min word frequency | 3 |

---

## Key Numbers

| Metric | Value | Source |
|--------|-------|--------|
| FY range | FY2022 – FY2026 | yfinance (FY2022–FY2025) + Dollarama IR (FY2026) |
| FY2026 Revenue | $7.24B CAD | Dollarama IR Q1–Q3 actuals + Q4 consensus |
| FY2026 EPS | $4.76 CAD | Dollarama IR (verified) |
| FY2026 EBITDA Margin | 32.9% | Integration dip from Reject Shop acquisition |
| FY2025 FCF | $1.40B CAD | Dollarama IR (DCF base FCF) |
| FY2025 ROIC | ~30% | EBIT×(1−tax)÷(Assets−CL−Cash) |
| Revenue CAGR (FY2022–2026) | +14% | Exceeds >5% rubric threshold ✓ |
| EPS CAGR (FY2022–2026) | +21% | Exceeds >7% rubric threshold ✓ |
| Shareholder earnings | ~22%/yr | EPS growth +21% + dividend ~1% |
| IPO price | $17.00 CAD | Oct 27, 2009 |
| IPO CAGR | ~27%/yr | $10K → ~$100K |
| DCF target (WACC 5.5%) | **$212–$213 CAD** | Hardcoded: FCF $1.397B, Net debt $2.155B, 277M shares |
| Price target | **CAD $212** | EV/EBITDA multiple approach (~29×) |

---

## Data Architecture

```
Data Source         Coverage                    Tab(s)
────────────────────────────────────────────────────────────────
yfinance LIVE       FY2022–FY2025 financials    01–08, 11
                    Current price + multiples   01, 07
                    5-yr daily price history    01, 11
                    IPO-to-date history         08
HARDCODED           FY2026 (Q1–Q3 IR actuals +  02–08
(Dollarama IR)      Q4 consensus, Mar 24 2026)
HARDCODED           DLTR / DG SEC FY2025 10-K   07
(SEC filings)
COMPUTED LIVE       DCF, Monte Carlo            09, 10
                    ML regression               11
                    NLP polarity scoring        12
```

**Why FY2026 is hardcoded:** Dollarama's FY2026 results were reported March 24, 2026. yfinance annual data for FY2026 is not yet available via the API. The hardcoded values come from Dollarama Q1–Q3 press releases (actuals) plus Q4 analyst consensus.

**Why peer data is hardcoded:** yfinance returns partial/incorrect annual data for DLTR and DG. The dashboard uses verified figures from SEC 10-K filings (DLTR Feb 1 2025, DG Jan 31 2025) as fallback regardless of live data availability.

---

## Colour Palette (Colab v6B)

| Name | Hex | Used For |
|------|-----|---------|
| `BRAND` | `#E63946` | Dollarama red — primary accent, positive words in NLP |
| `ACCENT` | `#1D3557` | Dark navy — sidebar background, headings |
| `P1` | `#457B9D` | Mid blue — chart series, callout borders |
| `P2` | `#A8DADC` | Light teal — chart series, subjectivity bars |
| `P3` | `#F4A261` | Orange — warning callouts |
| `GREEN` | `#2A9D8F` | Teal green — positive signals, profitable MC paths |

---

## Peer Comparison Data

Peer company data uses **verified FY2025 SEC 10-K filings** — not Yahoo Finance's live peer feed.

| | DLTR (USD) | DG (USD) |
|--|--|--|
| Revenue | $30,607M | $40,612M |
| EBITDA Margin | 11.9% | 9.6% |
| ROIC | 13.6% | 15.2% |
| EV/EBITDA | 6.5× | 7.4× |

> **Note on DLTR:** FY2025 net income of −$4,268M reflects a one-time Family Dollar goodwill impairment write-down — not an operational loss. Always flag this when presenting the peer comparison. DLTR is excluded from net income / net margin comparisons.

---

## Theme Configuration

The `config.toml` file in the project root controls which theme loads by default:

```toml
# config.toml

[theme]
base = "light"               # Change to "dark" for dark mode default
primaryColor = "#E63946"     # Dollarama red
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F1F3F5"
textColor = "#111827"
font = "sans serif"
```

To switch to dark by default, change `base = "light"` to `base = "dark"`. Users can also toggle at any time via ☰ → Settings in the Streamlit interface.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'X'` | Run `pip install -r requirements.txt` |
| `streamlit: command not found` | Run `python -m streamlit run Dashboard.py` |
| Yahoo Finance timeout or empty data | Restart the app — Yahoo rate-limits repeated requests. Dashboard falls back to hardcoded FY2022–FY2026 values automatically. |
| `sklearn` not found | Run `pip install scikit-learn>=1.3.0` |
| `yfinance` install fails (C compiler error) | Run `pip install "yfinance>=0.2.50,<1.0.0"` — avoids curl_cffi |
| Port already in use | Run `streamlit run Dashboard.py --server.port 8502` |
| Peer data looks wrong | Expected — DLTR/DG always use verified 10-K fallback, not live Yahoo data |
| DCF price is not ~$212 | Check WACC slider is at 5.5%, FCF Growth at 8.0%, TGR at 2.5% |
| Beta in CAPM table changes between sessions | Correct — Beta is pulled live from yfinance and will vary with market data |

---

## Dependencies

| Package | Min Version | Used For |
|---------|------------|---------|
| streamlit | 1.40.0 | Dashboard framework, sidebar nav, widgets, sliders |
| plotly | 5.20.0 | All interactive charts (bar, scatter, heatmap, histogram) |
| pandas | 2.2.0 | Data loading, transformation, tables, styling |
| numpy | 1.26.0 | Numerical computing, Monte Carlo simulation |
| yfinance | 0.2.50 (`<1.0.0`) | Live DOL.TO financial data — see note below |
| scikit-learn | 1.3.0 | Linear Regression, R², RMSE (Tab 11 — Tutorial 5) |

> **Why `yfinance<1.0.0`?** yfinance 1.x introduced `curl_cffi` as a mandatory dependency which requires a C compiler. This fails on Windows without Visual Studio Build Tools and on macOS without Xcode Command Line Tools. Version 0.2.x installs cleanly everywhere with no compilation step.

> **Note:** `matplotlib` is **not required** by this dashboard. All charts use Plotly exclusively.

---

## Known Data Notes

1. **FY2026 EBITDA margin dip** — The 170bps dip from 33.5% (FY2025) to 32.9% (FY2026) is entirely attributable to Reject Shop integration costs from the December 2025 acquisition. The core Canadian business margins are intact. Recovery to ~33% is modelled by FY2027.

2. **Negative equity in FY2022** — Dollarama carried −$66M shareholders' equity in FY2022 because share buybacks exceeded retained earnings. This is capital efficiency, not distress. This is why ROIC is computed as `EBIT×(1−tax)÷(Assets−CL−Cash)` rather than the conventional NOPAT/Equity formula.

3. **DCF vs target price** — The $212 target is primarily driven by the EV/EBITDA multiple approach (29× FY2026 EBITDA of $2.39B). The DCF at WACC 5.5% (CAPM-calculated rate) corroborates this at ~$213. At a conservative stress-test WACC of 9%, the DCF gives ~$93 — a floor, not a base case.

4. **Beta changes between sessions** — Beta is pulled live from Yahoo Finance on each session load. It was ~0.26 at the time of the initial analysis and is currently ~0.37. This changes the displayed Ke and calculated WACC in the CAPM table, but does not affect the DCF output because the slider is hardcoded at 5.5%.

5. **Sensitivity table is dynamic** — Unlike a static heatmap, the sensitivity table in Tab 09 recentres on your slider values every time you move a slider. The ▶ marker indicates your current WACC row.

---

> ⚠️ This is an academic project for MBAN5570 — Equity Research Analytics at Saint Mary's University. Nothing here constitutes financial advice. All data is sourced from Yahoo Finance (yfinance), Dollarama Investor Relations press releases, and SEC 10-K filings.

*March 2026 · Soni & Warner · MBAN5570 · Saint Mary's University*