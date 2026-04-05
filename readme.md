# Dollarama Inc. (DOL.TO) — Equity Research Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-green)
![Status](https://img.shields.io/badge/Status-Presentation%20Ready-brightgreen)

**MBAN5570 — Equity Research Analytics**  
**Soni & Warner · Saint Mary's University · 2025**

***THIS IS A SCHOOL PROJECT NOT MEANT FOR FINANCIAL ADVICE***


</div>

---

## Investment Thesis

> **BUY · DOL.TO · Target $212 CAD · ~23% upside from $172.59**

On March 24, 2026, Dollarama reported that revenue grew 13.1% and EPS grew 12.1% — and the stock fell 9%. The selloff was driven by a single factor: a 170 basis-point EBITDA margin dip from integrating The Reject Shop acquisition in Australia. We view this as a temporary headwind, not a structural impairment. ROIC of ~38% versus WACC of 9% — a 29 percentage-point value-creation spread — has widened for five consecutive years. Our DCF at the CAPM-calculated WACC of 5.5% produces **$213 intrinsic value**. The analyst consensus is **$212.06**. Two independent methods within $1 of each other.

---

## Live Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dollarama-equity-research.streamlit.app)

> If deploying yourself, see [Quick Start](#quick-start) below.

---

## What the Dashboard Contains

The dashboard is built in Streamlit and organised into **13 interactive tabs** across three analytical layers, matching the MBAN5570 course structure exactly.

### Traditional Analysis (Section 2.A) — Tabs 01–08

| Tab | Title | What It Shows |
|-----|-------|---------------|
| **01** | Company Overview | Investment thesis, 6 KPI cards, 5-year price chart with 50/200-day MAs, daily volume |
| **02** | Macro & Industry | Top-down framework: BoC rate cycle, Canada-US trade context, peer revenue growth comparison |
| **03** | Income Statement | Revenue, EBITDA, net income, EPS and margins FY2022–FY2026 with CAGR analysis |
| **04** | Balance Sheet | Asset composition, equity recovery, debt structure, current ratio, net debt/EBITDA trends |
| **05** | Cash Flow | OCF, CapEx, FCF, financing activities FY2022–FY2026; FCF conversion analysis |
| **06** | Financial Ratios | Profitability, leverage, liquidity, efficiency heatmap; ROIC methodology note |
| **07** | Valuation Multiples | 7 live multiples vs sector benchmarks; peer comparison (DLTR, DG); composite signal |
| **08** | IPO Compounding | Stock compounding since Oct 9, 2009 ($17.50 IPO); $10k investment calculator; CAGR vs TSX |

### Live Valuation Demo — Tabs 09–10

| Tab | Title | What It Shows |
|-----|-------|---------------|
| **09** | DCF Live Model | CAPM/WACC derivation table; 5-year FCF projection; 10×5 sensitivity matrix; real-time price update on slider change |
| **10** | Monte Carlo | 5,000-path simulation; histogram + CDF; P5/P25/P50/P75/P95 percentiles; probability analysis |

### AI-Assisted Analysis (Sections 2.B & 2.C) — Tabs 11–13

| Tab | Title | What It Shows |
|-----|-------|---------------|
| **11** | ML Price Model | Linear regression (Tutorial 5): 10-day MA + 14-day RSI; R²=0.884, RMSE=$3.84, MA coeff=1.0027; data leakage explanation |
| **12** | NLP Sentiment | Earnings call polarity scoring (Tutorial 4): 5 real transcripts FY2022–FY2026 Q3; custom lexicon; trend chart |
| **13** | AI Critical Review | Section 2.C: what AI got right, wrong, accepted, discarded; ROIC error correction; ML leakage proof |

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Krishna-Soni-Git/dollarama-equity-research.git
cd dollarama-equity-research

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run Dashboard.py
```

The dashboard opens at `http://localhost:8501`

### Optional — Export data to Excel first

```bash
# Pull live data from Yahoo Finance and save to dollarama_snapshot.xlsx
python dollarama_data_export.py
```

This creates a 13-sheet Excel workbook and a `csv/` folder with individual files. Run this once before a presentation to have the data cached locally.

---

## Presentation Mode

The dashboard ships with **`PRESENTATION_MODE = True`** hardcoded near the top of `Dashboard.py`. This is the most important setting.

```python
# Line ~56 in Dashboard.py
PRESENTATION_MODE = True   # ← True = frozen snapshot | False = live yfinance
```

| Mode | Behaviour | When to Use |
|------|-----------|-------------|
| `True` (default) | All market data frozen to **April 3, 2026 snapshot** — identical numbers on any machine, any day, forever | Recording, presentation, submission, sharing |
| `False` | Pulls live from Yahoo Finance — price, beta, P/E, analyst target all drift | Live demo only, with awareness numbers will change |

The sidebar shows a **🔒 PRESENTATION MODE** badge (red) or **📡 LIVE MODE** badge (green) so it is always clear which mode is active.

### What is frozen in Presentation Mode

| Value | Frozen To |
|-------|-----------|
| Current price | $172.59 CAD |
| Market cap | $47.07B |
| Enterprise value | $52.13B |
| Trailing P/E | 36.5× |
| Beta | 0.37 |
| Analyst consensus target | **$212.06** |
| All 7 valuation multiples | Analysis values |
| DCF price | **$213** (computed from hardcoded FCF/debt/shares) |
| Monte Carlo | Same every run (fixed random seed + hardcoded inputs) |
| NLP scores | Hardcoded transcripts — never changes |
| Financial statements | Historical data — never changes |

---

## Key Verified Numbers

All numbers below match the dashboard exactly (PRESENTATION_MODE=True, April 3, 2026).

### Investment Summary

| Metric | Value | Source |
|--------|-------|--------|
| Current price | $172.59 CAD | Yahoo Finance snapshot |
| Price target | $212 CAD | EV/EBITDA + DCF convergence |
| Analyst consensus | $212.06 | Yahoo Finance (16 analysts) |
| Implied upside | ~23% | ($212 / $172.59 − 1) |
| Market cap | $47.07B | Yahoo Finance snapshot |
| Enterprise value | $52.13B | Yahoo Finance snapshot |

### CAPM / WACC Derivation (Tab 09)

| Input | Value | Source |
|-------|-------|--------|
| Risk-free rate (Rf) | 3.50% | Bank of Canada, 10yr GoC bond, March 2026 |
| Beta (β) | 0.37 | Yahoo Finance, 5-year monthly |
| Equity risk premium | 6.50% | Damodaran (NYU), Canada 2026 |
| Cost of equity (Ke) | **5.92%** | Rf + β × ERP = 3.5 + 0.37×6.5 |
| Cost of debt (Kd) | 3.12% | 4.25% × (1 − 26.5%) |
| Weights | 12% / 88% | FY2025 balance sheet |
| **WACC calculated** | **5.57% → 5.5%** | Blended; slider rounded to 5.5% |

### DCF Model (Tab 09)

| Input | Value | Source |
|-------|-------|--------|
| Base FCF | $1.397B | FY2025 actual (Yahoo Finance) |
| FCF growth (Stage 1) | 8.0%/yr | Half of 14% historical CAGR — conservative |
| Forecast horizon | 5 years | Colab Cell 35 methodology |
| Terminal growth rate | 2.5% | Canada long-run GDP |
| Net debt | $2.155B | FY2025, ex IFRS 16 leases |
| Diluted shares | 277M | FY2025 weighted average |
| **DCF at WACC 5.5%** | **$213** | PV FCFs $7.50B + PV terminal $53.66B |
| DCF at WACC 9% (stress) | ~$93 | Stress floor |

### Monte Carlo (Tab 10)

| Statistic | Value |
|-----------|-------|
| Paths | 5,000 |
| WACC mean (stress) | 9.0% (normal, SD 0.8%) |
| P5 / P25 / P50 / P75 / P95 | $70 / $84 / $95 / $109 / $134 |
| Prob. > $212 target | 0.1% |
| Prob. > $172.59 (profitable) | 0.4% |
| Prob. < $130 (stress) | 93.6% |

### ML Price Model (Tab 11)

| Metric | Value |
|--------|-------|
| Features | 10-day MA + 14-day RSI |
| Training data | 1,255 trading days (DOL.TO daily) |
| Train / test split | 80% / 20% chronological |
| R² (test set) | **0.884** |
| RMSE (test set) | **$3.84** |
| MA coefficient | **1.0027** ← ≈1.0 = data leakage |
| Used in valuation? | **No** — excluded |

### NLP Sentiment (Tab 12)

| Earnings Call | Polarity | Positive | Negative | Signal |
|---------------|----------|----------|----------|--------|
| FY2022 Annual | −8.6% | 11 | 26 | Negative |
| FY2023 Annual | +10.0% | 19 | 2 | Positive |
| FY2024 Annual | +14.6% | 24 | 0 | Positive |
| FY2025 Annual | **+14.8%** | **26** | **0** | **Positive ↑ (peak)** |
| FY2026 Q3 | +12.6% | 24 | 1 | Positive |

### Financial Performance (FY2022–FY2026)

| Metric | FY2022 | FY2023 | FY2024 | FY2025 | FY2026A | CAGR |
|--------|--------|--------|--------|--------|---------|------|
| Revenue ($B) | $4.331 | $5.053 | $5.867 | $6.413 | $7.244 | **14% ✓** |
| EBITDA Margin | 29.6% | 30.3% | 32.1% | 33.5% | 32.9%† | Expanding |
| Diluted EPS ($) | $2.18 | $2.76 | $3.56 | $4.16 | $4.76 | **22% ✓** |
| FCF ($B) | $1.004 | $0.713 | $1.251 | $1.397 | $1.380 | Strong |
| ROIC | ~40% | ~39% | ~43% | ~38% | ~28%† | vs WACC 9% |

† FY2026 dip reflects Reject Shop acquisition integration. Recovery to ~33% modelled FY2027.  
✓ Exceeds rubric threshold (>5% revenue, >7% EPS).

---

## Repository Structure

```
dollarama-equity-research/
│
├── Dashboard.py                 # Main Streamlit app — 13 tabs, all analysis
├── dollarama_data_export.py     # Optional: export live data to Excel + CSV
├── requirements.txt             # Python dependencies (pip install -r)
├── README.md                    # This file
└── .gitignore                   # Keeps secrets and temp files out of repo
```

---

## Data Sources

| Data | Source | Notes |
|------|--------|-------|
| FY2022–FY2025 financials | Yahoo Finance (yfinance) | Live pull via DOL.TO ticker |
| FY2026 income statement | Dollarama Investor Relations | Q1–Q3 actuals + Q4 consensus (March 24, 2026) |
| Current market data | Yahoo Finance info dict | Frozen to April 3, 2026 in presentation mode |
| Peer data (DLTR, DG) | SEC EDGAR FY2025 10-K | DLTR: Feb 1 2025 · DG: Jan 31 2025 · USD |
| Risk-free rate (3.50%) | Bank of Canada | 10yr GoC bond, March 2026 |
| Equity risk premium (6.50%) | Damodaran, NYU (2026) | Canada market ERP |
| IPO price ($17.50 CAD) | CBC News / TSX / Dollarama IR | First trading day: October 9, 2009 |
| Earnings call transcripts | Dollarama IR / Seeking Alpha | FY2022–FY2026 Q3 (NLP Tutorial 4) |
| Daily price history | Yahoo Finance (yfinance) | 1,255 trading days (ML Tutorial 5) |

---

## Course Context

This project was built for **MBAN5570 — Equity Research Analytics** at Saint Mary's University. The dashboard directly supports all required analytical components:

- **Section 2.A** — Traditional equity research (all 12 professor-required subsections)
- **Section 2.B** — AI-assisted analysis: DCF/MC (Colab Cell 35), ML (Tutorial 5), NLP (Tutorial 4)
- **Section 2.C** — Critical evaluation of AI outputs with explicit accounting justification

The rubric thresholds assessed: Revenue CAGR >5% ✓ (14%), EPS CAGR >7% ✓ (22%), Shareholder earnings >10% ✓ (~23%/yr), IPO compounding >10% ✓ (~15%/yr from $17.50).

---

## Technical Requirements

```
streamlit >= 1.40.0
plotly >= 5.20.0
pandas >= 2.2.0
numpy >= 1.26.0
yfinance >= 0.2.50, < 1.0.0
scikit-learn >= 1.3.0
openpyxl >= 3.1.0   # for data export only
```

**Python 3.9+ required.** Tested on Python 3.10, 3.11, 3.12 across Windows, macOS, and Linux.

> **Note on yfinance:** Pinned below 1.0.0 because yfinance 1.x requires a C compiler for installation (`curl_cffi` dependency). Version 0.2.x installs cleanly on all platforms with no compilation step.

---

## Deployment

### Streamlit Community Cloud (recommended — free)

1. Push this repo to GitHub (already done)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo → branch `main` → main file: `Dashboard.py`
4. Click **Deploy**

Streamlit reads `requirements.txt` automatically. The app will be live at a public URL you can share directly in your presentation.

### Local

```bash
pip install -r requirements.txt
streamlit run Dashboard.py
```

---

## Disclaimer

Academic project prepared for MBAN5570 — Equity Research Analytics at Saint Mary's University. This dashboard and all associated documents do not constitute financial advice. All data is sourced from public platforms and verified against Dollarama Investor Relations disclosures. Every metric and formula is traceable to a verified source.

**Soni & Warner · Saint Mary's University · 2025**

---

<div align="center">
<sub>Built with Streamlit · Data from Yahoo Finance, Dollarama IR, SEC EDGAR · Analysis verified April 2026</sub>
</div>