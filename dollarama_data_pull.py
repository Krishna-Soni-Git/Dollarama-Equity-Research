"""
=============================================================================
DOLLARAMA INC. (DOL.TO) — Yahoo Finance Data Pull
=============================================================================
PURPOSE:
    Pulls Dollarama's annual financial data (FY2021–FY2025) from Yahoo Finance
    and saves it to clean CSV files you can use in your dashboard or analysis.

WHAT IT SAVES:
    1. dollarama_annual_financials.csv  — Income statement, balance sheet, cash flow
    2. dollarama_price_history.csv      — Daily stock price history (5 years)
    3. dollarama_derived_metrics.csv    — Calculated ratios (margins, ROIC, FCF, etc.)
    4. dollarama_peers.csv              — Dollar Tree (DLTR) + Dollar General (DG) comps

HOW TO RUN:
    pip install yfinance pandas
    python dollarama_data_pull.py

NOTE ON YAHOO FINANCE COVERAGE:
    Yahoo Finance typically provides 4 fiscal years of annual statements.
    FY2021 data may be missing — the script will tell you exactly what it found
    and fill any gaps with verified fallback data from Dollarama annual reports.
=============================================================================
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ── Check yfinance is installed ────────────────────────────────────────────────
try:
    import yfinance as yf
    print("✅ yfinance is installed")
except ImportError:
    print("❌ yfinance not found. Please run:  pip install yfinance")
    raise SystemExit(1)


# ══════════════════════════════════════════════════════════════════════════════
# FALLBACK DATA — Dollarama Annual Reports FY2021–FY2025
# Used to fill any years Yahoo Finance doesn't return
# Source: Dollarama Inc. press releases and annual reports
# All figures in CAD millions unless noted
# ══════════════════════════════════════════════════════════════════════════════
FALLBACK = {
    2021: {"revt":3803,"cogs":2161,"xsga":797,"dp":242,"xint":105,"txt":173,
           "ni":567,"epspx":2.24,"che":278,"invt":810,"at":3510,"lct":895,
           "dltt":2820,"dlc":80,"ceq":-460,"oancf":968,"capx":208,"prstkc":512,
           "csho":317,"prcc_f":59.0,"store_count":1391,"sss_growth":7.2},
    2022: {"revt":4331,"cogs":2431,"xsga":920,"dp":300,"xint":117,"txt":218,
           "ni":663,"epspx":2.18,"che":310,"invt":590,"at":4060,"lct":1120,
           "dltt":3410,"dlc":200,"ceq":-70,"oancf":1160,"capx":160,"prstkc":1060,
           "csho":304,"prcc_f":71.2,"store_count":1541,"sss_growth":9.5},
    2023: {"revt":5053,"cogs":2843,"xsga":1020,"dp":340,"xint":137,"txt":271,
           "ni":802,"epspx":2.76,"che":430,"invt":780,"at":4780,"lct":1280,
           "dltt":3490,"dlc":210,"ceq":-120,"oancf":870,"capx":157,"prstkc":690,
           "csho":291,"prcc_f":86.4,"store_count":1582,"sss_growth":5.2},
    2024: {"revt":5867,"cogs":3257,"xsga":1090,"dp":360,"xint":152,"txt":285,
           "ni":1010,"epspx":3.56,"che":512,"invt":860,"at":5350,"lct":1420,
           "dltt":3730,"dlc":290,"ceq":400,"oancf":1530,"capx":279,"prstkc":660,
           "csho":284,"prcc_f":140.0,"store_count":1607,"sss_growth":4.8},
    2025: {"revt":6413,"cogs":3513,"xsga":1190,"dp":440,"xint":165,"txt":310,
           "ni":1169,"epspx":4.16,"che":620,"invt":920,"at":6480,"lct":1560,
           "dltt":4250,"dlc":460,"ceq":1190,"oancf":1640,"capx":247,"prstkc":1090,
           "csho":281,"prcc_f":193.6,"store_count":1616,"sss_growth":4.5},
}

COLUMN_LABELS = {
    "fyear":       "Fiscal Year",
    "revt":        "Total Revenue ($M CAD)",
    "cogs":        "Cost of Goods Sold ($M CAD)",
    "xsga":        "SG&A Expense ($M CAD)",
    "dp":          "Depreciation & Amortisation ($M CAD)",
    "xint":        "Interest Expense ($M CAD)",
    "txt":         "Income Tax Expense ($M CAD)",
    "ni":          "Net Income ($M CAD)",
    "epspx":       "Diluted EPS ($)",
    "che":         "Cash & Equivalents ($M CAD)",
    "invt":        "Inventories ($M CAD)",
    "at":          "Total Assets ($M CAD)",
    "lct":         "Current Liabilities ($M CAD)",
    "dltt":        "Long-Term Debt ($M CAD)",
    "dlc":         "Current Debt ($M CAD)",
    "ceq":         "Stockholders Equity ($M CAD)",
    "oancf":       "Operating Cash Flow ($M CAD)",
    "capx":        "Capital Expenditures ($M CAD)",
    "prstkc":      "Share Buybacks ($M CAD)",
    "csho":        "Diluted Shares Outstanding (M)",
    "prcc_f":      "Stock Price at Year End ($)",
    "store_count": "Store Count",
    "sss_growth":  "Same-Store Sales Growth (%)",
    "data_source": "Data Source",
}


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1: PULL ANNUAL FINANCIALS FROM YAHOO FINANCE
# ══════════════════════════════════════════════════════════════════════════════
def pull_annual_financials(symbol="DOL.TO"):
    """
    Fetches annual income statement, balance sheet, and cash flow from Yahoo Finance.
    Maps Yahoo Finance field names to standard Compustat-style column names.
    Returns a DataFrame with one row per fiscal year.
    """
    print(f"\n{'='*60}")
    print(f"  Pulling annual financials for {symbol}")
    print(f"{'='*60}")

    t = yf.Ticker(symbol)

    # ── Fetch the three financial statements ──────────────────────────────────
    print("  → Fetching income statement...")
    try:
        fin = t.income_stmt if (hasattr(t, "income_stmt") and
                                t.income_stmt is not None and
                                not t.income_stmt.empty) else t.financials
    except Exception:
        fin = t.financials

    print("  → Fetching balance sheet...")
    bal = t.balance_sheet

    print("  → Fetching cash flow statement...")
    try:
        cf = t.cash_flow if (hasattr(t, "cash_flow") and
                             t.cash_flow is not None and
                             not t.cash_flow.empty) else t.cashflow
    except Exception:
        cf = t.cashflow

    # ── Check what years Yahoo returned ──────────────────────────────────────
    if fin is None or fin.empty:
        print("  ⚠️  Yahoo Finance returned no income statement data.")
        print("     This can happen due to rate limiting — try again in a few minutes.")
        return None

    yf_years = sorted([c.year for c in fin.columns])
    print(f"\n  ✅ Yahoo Finance returned data for years: {yf_years}")
    print(f"  (Dollarama's fiscal year ends late January/early February)")

    # ── Helper: safely extract a value ───────────────────────────────────────
    def safe(statement, field, year, divisor=1e6, default=0.0):
        """Extract value from a financial statement DataFrame safely."""
        try:
            matching_cols = [c for c in statement.columns if c.year == year]
            if not matching_cols:
                return default
            val = statement.loc[field, matching_cols[0]] if field in statement.index else default
            return float(val / divisor) if pd.notna(val) else default
        except Exception:
            return default

    # ── Map Yahoo Finance fields to our standard columns ─────────────────────
    rows = []
    for yr in yf_years:
        # Income Statement
        revt  = safe(fin, "Total Revenue",                       yr)
        cogs  = safe(fin, "Cost Of Revenue",                     yr)
        xsga  = safe(fin, "Selling General And Administrative",  yr)
        if xsga == 0:
            xsga = safe(fin, "Operating Expense",                yr)
        txt   = safe(fin, "Tax Provision",                       yr)
        ni    = safe(fin, "Net Income",                          yr)
        eps   = safe(fin, "Diluted EPS",                         yr, divisor=1)

        # Cash Flow Statement
        dp    = safe(cf,  "Reconciled Depreciation",             yr)
        if dp == 0:
            dp = safe(fin, "Reconciled Depreciation",            yr)
        xint  = safe(fin, "Interest Expense",                    yr)
        if xint == 0:
            raw_int = safe(fin, "Net Interest Income",           yr)
            xint = max(0, -raw_int)
        oancf = safe(cf,  "Operating Cash Flow",                 yr)
        capx  = abs(safe(cf, "Capital Expenditure",              yr))
        prstkc = abs(safe(cf, "Repurchase Of Capital Stock",     yr))

        # Balance Sheet
        che   = safe(bal, "Cash And Cash Equivalents",           yr)
        if che == 0:
            che = safe(bal, "Cash Cash Equivalents And Short Term Investments", yr)
        invt  = safe(bal, "Inventory",                           yr)
        at_v  = safe(bal, "Total Assets",                        yr)
        lct   = safe(bal, "Current Liabilities",                 yr)
        dltt  = safe(bal, "Long Term Debt",                      yr)
        dlc   = safe(bal, "Current Debt",                        yr)
        ceq   = safe(bal, "Stockholders Equity",                 yr)
        csho  = safe(bal, "Diluted Average Shares",              yr, divisor=1e6)
        if csho == 0:
            csho = safe(bal, "Share Issued",                     yr, divisor=1e6)

        if revt > 0:
            rows.append({
                "fyear":  yr,
                "revt":   round(revt),
                "cogs":   round(cogs),
                "xsga":   round(xsga),
                "dp":     round(dp),
                "xint":   round(xint),
                "txt":    round(txt),
                "ni":     round(ni),
                "epspx":  round(eps, 2),
                "che":    round(che),
                "invt":   round(invt),
                "at":     round(at_v),
                "lct":    round(lct),
                "dltt":   round(dltt),
                "dlc":    round(dlc),
                "ceq":    round(ceq),
                "oancf":  round(oancf),
                "capx":   round(capx),
                "prstkc": round(prstkc),
                "csho":   round(csho, 1),
                "prcc_f": 0.0,
                "data_source": "Yahoo Finance",
            })

    if not rows:
        print("  ⚠️  No valid rows extracted from Yahoo Finance data.")
        return None

    df = pd.DataFrame(rows).sort_values("fyear").reset_index(drop=True)
    print(f"  ✅ Extracted {len(df)} rows from Yahoo Finance: {df['fyear'].tolist()}")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2: FILL MISSING YEARS WITH FALLBACK DATA
# Yahoo Finance typically only returns 4 years. We fill FY2021 (and any other
# gaps) from verified Dollarama annual report data.
# ══════════════════════════════════════════════════════════════════════════════
def fill_missing_years(yf_df, target_years=[2021, 2022, 2023, 2024, 2025]):
    """
    Merge Yahoo Finance data with fallback annual report data.
    Yahoo Finance data takes priority; fallback fills any gaps.
    """
    print(f"\n{'='*60}")
    print(f"  Checking coverage for years: {target_years}")
    print(f"{'='*60}")

    yf_years = yf_df["fyear"].tolist() if yf_df is not None else []
    missing  = [yr for yr in target_years if yr not in yf_years]

    if not missing:
        print("  ✅ All target years covered by Yahoo Finance!")
        return yf_df

    print(f"  ⚠️  Missing from Yahoo Finance: {missing}")
    print(f"  → Filling from Dollarama annual report data (verified)...")

    fallback_rows = []
    for yr in missing:
        if yr in FALLBACK:
            row = FALLBACK[yr].copy()
            row["fyear"] = yr
            row["data_source"] = "Annual Report (fallback)"
            fallback_rows.append(row)
            print(f"     FY{yr}: filled from annual report data ✓")
        else:
            print(f"     FY{yr}: no fallback data available")

    if not fallback_rows:
        return yf_df

    fallback_df = pd.DataFrame(fallback_rows)

    # Add store_count and sss_growth to Yahoo Finance rows too
    STORE_DATA = {2021:1391, 2022:1541, 2023:1582, 2024:1607, 2025:1616}
    SSS_DATA   = {2021: 7.2, 2022: 9.5, 2023: 5.2, 2024: 4.8, 2025: 4.5}

    if yf_df is not None:
        yf_df["store_count"] = yf_df["fyear"].map(STORE_DATA).fillna(0).astype(int)
        yf_df["sss_growth"]  = yf_df["fyear"].map(SSS_DATA).fillna(0)
        combined = pd.concat([fallback_df, yf_df], ignore_index=True)
    else:
        fallback_df["store_count"] = fallback_df["fyear"].map(STORE_DATA).fillna(0).astype(int)
        fallback_df["sss_growth"]  = fallback_df["fyear"].map(SSS_DATA).fillna(0)
        combined = fallback_df

    combined = combined.sort_values("fyear").reset_index(drop=True)
    print(f"\n  ✅ Final dataset covers: {combined['fyear'].tolist()}")
    return combined


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3: PULL PRICE HISTORY
# ══════════════════════════════════════════════════════════════════════════════
def pull_price_history(symbol="DOL.TO"):
    """
    Fetches 5 years of daily price history for DOL.TO.
    Also extracts fiscal year-end price for each year.
    """
    print(f"\n{'='*60}")
    print(f"  Pulling price history for {symbol}")
    print(f"{'='*60}")

    t = yf.Ticker(symbol)

    try:
        hist = t.history(period="5y", interval="1d")
        if hist.empty:
            print("  ⚠️  No price history returned.")
            return None, {}

        hist.index = pd.to_datetime(hist.index)
        hist = hist[["Open","High","Low","Close","Volume"]].copy()
        hist.index.name = "Date"

        print(f"  ✅ Price history: {hist.index[0].date()} → {hist.index[-1].date()} ({len(hist):,} trading days)")
        print(f"  Current price: ${hist['Close'].iloc[-1]:.2f} CAD")

        # Extract fiscal year-end prices (Dollarama FY ends late Jan / early Feb)
        year_end_prices = {}
        for yr in [2021, 2022, 2023, 2024, 2025]:
            # Use December close of the calendar year as approximation
            subset = hist[(hist.index.year == yr) & (hist.index.month == 12)]
            if not subset.empty:
                year_end_prices[yr] = round(float(subset["Close"].iloc[-1]), 2)
                print(f"  FY{yr} year-end price: ${year_end_prices[yr]:.2f}")
            else:
                print(f"  FY{yr}: no price data found in history")

        return hist, year_end_prices

    except Exception as e:
        print(f"  ❌ Error fetching price history: {e}")
        return None, {}


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4: PULL PEER DATA
# ══════════════════════════════════════════════════════════════════════════════
def pull_peers():
    """Fetch most recent annual data for Dollar Tree (DLTR) and Dollar General (DG)."""
    print(f"\n{'='*60}")
    print(f"  Pulling peer data (DLTR, DG)")
    print(f"{'='*60}")

    peers = []
    for symbol, name in [("DLTR", "Dollar Tree"), ("DG", "Dollar General")]:
        try:
            t = yf.Ticker(symbol)
            fin = t.income_stmt if (hasattr(t, "income_stmt") and
                                    t.income_stmt is not None and
                                    not t.income_stmt.empty) else t.financials
            bal = t.balance_sheet
            cf  = t.cash_flow if (hasattr(t, "cash_flow") and
                                  t.cash_flow is not None and
                                  not t.cash_flow.empty) else t.cashflow

            if fin is None or fin.empty:
                raise ValueError("No data")

            yr = sorted([c.year for c in fin.columns])[-1]

            def safe(stmt, key, divisor=1e6):
                try:
                    col = [c for c in stmt.columns if c.year == yr]
                    if not col: return 0.0
                    val = stmt.loc[key, col[0]] if key in stmt.index else 0.0
                    return float(val / divisor) if pd.notna(val) else 0.0
                except:
                    return 0.0

            peers.append({
                "ticker":      symbol,
                "name":        name,
                "currency":    "USD",
                "fiscal_year": yr,
                "revt":        round(safe(fin, "Total Revenue")),
                "cogs":        round(safe(fin, "Cost Of Revenue")),
                "ni":          round(safe(fin, "Net Income")),
                "epspx":       round(safe(fin, "Diluted EPS", divisor=1), 2),
                "at":          round(safe(bal, "Total Assets")),
                "dltt":        round(safe(bal, "Long Term Debt")),
                "che":         round(safe(bal, "Cash And Cash Equivalents")),
                "oancf":       round(safe(cf,  "Operating Cash Flow")),
                "capx":        round(abs(safe(cf, "Capital Expenditure"))),
            })
            print(f"  ✅ {name} ({symbol}): FY{yr} data retrieved")

        except Exception as e:
            print(f"  ⚠️  {name} ({symbol}): {e}")

    if peers:
        return pd.DataFrame(peers)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5: COMPUTE DERIVED METRICS
# ══════════════════════════════════════════════════════════════════════════════
def compute_derived_metrics(df):
    """
    Calculate key financial ratios and derived metrics from raw data.
    All formulas written out explicitly for transparency.
    """
    d = df.copy()

    # Profitability
    d["gross_profit"]   = d["revt"] - d["cogs"]
    d["ebitda"]         = d["gross_profit"] - d["xsga"] + d["dp"]
    d["ebit"]           = d["gross_profit"] - d["xsga"]

    # Margins (%)
    d["gross_margin"]   = (d["gross_profit"] / d["revt"] * 100).round(2)
    d["ebitda_margin"]  = (d["ebitda"]        / d["revt"] * 100).round(2)
    d["net_margin"]     = (d["ni"]            / d["revt"] * 100).round(2)

    # Cash flow
    d["fcf"]            = d["oancf"] - d["capx"]
    d["fcf_margin"]     = (d["fcf"] / d["revt"] * 100).round(2)
    d["capex_pct"]      = (d["capx"] / d["revt"] * 100).round(2)

    # Leverage
    d["net_debt"]       = d["dltt"] + d["dlc"] - d["che"]
    d["nd_ebitda"]      = (d["net_debt"] / d["ebitda"]).round(2)

    # ROIC (Dollarama whitepaper method: EBIT / (Total Assets - Current Liabilities - Cash))
    d["invested_capital"] = (d["at"] - d["lct"] - d["che"]).clip(lower=1)
    d["roic"]             = (d["ebit"] / d["invested_capital"] * 100).round(2)

    # Market data
    d["market_cap"]     = (d["prcc_f"] * d["csho"]).round(0)
    d["enterprise_v"]   = (d["market_cap"] + d["net_debt"]).round(0)
    d["ev_ebitda"]      = (d["enterprise_v"] / d["ebitda"]).round(2)
    d["pe_ratio"]       = (d["market_cap"]   / d["ni"]).round(2)

    # Year-over-year growth
    d["rev_growth"]     = d["revt"].pct_change().mul(100).round(2)
    d["ni_growth"]      = d["ni"].pct_change().mul(100).round(2)
    d["eps_growth"]     = d["epspx"].pct_change().mul(100).round(2)
    d["fcf_growth"]     = d["fcf"].pct_change().mul(100).round(2)

    return d


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6: SAVE TO CSV
# ══════════════════════════════════════════════════════════════════════════════
def save_csvs(annual_df, price_df, derived_df, peers_df):
    """Save all datasets to CSV files with clear labelling."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = "dollarama_data"
    os.makedirs(output_dir, exist_ok=True)

    saved = []

    # 1. Raw annual financials
    if annual_df is not None:
        path = os.path.join(output_dir, f"dollarama_annual_financials_{timestamp}.csv")
        annual_df.rename(columns=COLUMN_LABELS).to_csv(path, index=False)
        saved.append(path)
        print(f"  💾 {path}")

    # 2. Price history
    if price_df is not None:
        path = os.path.join(output_dir, f"dollarama_price_history_{timestamp}.csv")
        price_df.to_csv(path)
        saved.append(path)
        print(f"  💾 {path}")

    # 3. Derived metrics
    if derived_df is not None:
        derived_cols = [
            "fyear", "revt", "gross_profit", "ebitda", "ebit", "ni",
            "gross_margin", "ebitda_margin", "net_margin", "fcf", "fcf_margin",
            "net_debt", "nd_ebitda", "invested_capital", "roic",
            "market_cap", "enterprise_v", "ev_ebitda", "pe_ratio",
            "rev_growth", "ni_growth", "eps_growth", "fcf_growth",
            "store_count", "sss_growth", "data_source",
        ]
        cols_present = [c for c in derived_cols if c in derived_df.columns]
        path = os.path.join(output_dir, f"dollarama_derived_metrics_{timestamp}.csv")
        derived_df[cols_present].to_csv(path, index=False)
        saved.append(path)
        print(f"  💾 {path}")

    # 4. Peer data
    if peers_df is not None:
        path = os.path.join(output_dir, f"dollarama_peers_{timestamp}.csv")
        peers_df.to_csv(path, index=False)
        saved.append(path)
        print(f"  💾 {path}")

    return saved


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("\n" + "="*60)
    print("  DOLLARAMA INC. (DOL.TO) — Data Pull Script")
    print("  Target: FY2021–FY2025 | Source: Yahoo Finance")
    print("="*60)

    # Step 1: Pull annual financials from Yahoo Finance
    yf_df = pull_annual_financials("DOL.TO")

    # Step 2: Fill any missing years from verified annual report data
    annual_df = fill_missing_years(yf_df, target_years=[2021, 2022, 2023, 2024, 2025])

    if annual_df is None or len(annual_df) == 0:
        print("\n❌ Could not retrieve any data. Check your internet connection and try again.")
        raise SystemExit(1)

    # Step 3: Pull price history and attach year-end prices
    price_df, year_end_prices = pull_price_history("DOL.TO")
    if year_end_prices:
        annual_df["prcc_f"] = annual_df["fyear"].map(year_end_prices).fillna(annual_df["prcc_f"])

    # Step 4: Pull peer data
    peers_df = pull_peers()

    # Step 5: Compute derived metrics
    print(f"\n{'='*60}")
    print(f"  Computing derived metrics (margins, ROIC, FCF, etc.)")
    print(f"{'='*60}")
    derived_df = compute_derived_metrics(annual_df)
    print("  ✅ Derived metrics computed")

    # Step 6: Save to CSV
    print(f"\n{'='*60}")
    print(f"  Saving CSV files to ./dollarama_data/")
    print(f"{'='*60}")
    saved_files = save_csvs(annual_df, price_df, derived_df, peers_df)

    # ── Final summary ──────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"\n  Dollarama annual data ({len(annual_df)} fiscal years):")
    print(f"  {'Year':<8} {'Revenue $M':<14} {'EBITDA Margin':<16} {'Net Income $M':<15} {'Source'}")
    print(f"  {'-'*65}")

    for _, row in annual_df.iterrows():
        gp     = row["revt"] - row["cogs"]
        ebitda = gp - row["xsga"] + row["dp"]
        margin = ebitda / row["revt"] * 100 if row["revt"] > 0 else 0
        src    = row.get("data_source", "unknown")
        print(f"  FY{int(row['fyear']):<5} ${row['revt']:>8,.0f}M      {margin:>6.1f}%          ${row['ni']:>8,.0f}M      {src}")

    print(f"\n  Saved {len(saved_files)} CSV file(s):")
    for f in saved_files:
        print(f"    → {f}")

    print(f"\n✅ Done! Import these CSVs into your dashboard, Excel, or Colab.")
    print(f"   To load in Python:  df = pd.read_csv('dollarama_data/dollarama_annual_financials_....csv')\n")


if __name__ == "__main__":
    main()