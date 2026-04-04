"""
=============================================================================
DOLLARAMA DATA EXPORT — dollarama_data_export.py
MBAN5570 · Soni & Warner, 2025

PURPOSE:
  Run this script ONCE to pull everything from Yahoo Finance and save it
  as a single Excel workbook (dollarama_snapshot.xlsx) plus individual CSVs.

  The Dashboard.py then reads from these files instead of calling yfinance
  every time it starts — so your partner gets identical numbers on Wednesday
  without needing an internet connection for market data.

RUN (once, today):
  python dollarama_data_export.py

OUTPUT:
  dollarama_snapshot.xlsx     ← all data in one Excel workbook (13 sheets)
  csv/                        ← same data as individual CSV files

DASHBOARD USAGE:
  The dashboard automatically detects dollarama_snapshot.xlsx in the same
  folder. When found, it loads from that file instead of yfinance.
  When not found, it falls back to live yfinance as before.
=============================================================================
"""

import os
import json
import math
import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# HARDCODED DATA (same as Dashboard.py — does not come from yfinance)
# ─────────────────────────────────────────────────────────────────────────────
TICKER   = "DOL.TO"
IPO_DATE = "2009-10-09"  # First trading day on TSX (CBC News, Oct 9 2009)

FY2026_INCOME = {
    "Total Revenue":              7_244.4e6,
    "Cost Of Revenue":            3_970.5e6,
    "Gross Profit":               3_273.9e6,
    "Operating Income":           1_913.6e6,
    "EBIT":                       1_913.6e6,
    "Interest Expense":            -205.0e6,
    "Pretax Income":              1_735.0e6,
    "Tax Provision":               378.7e6,
    "Net Income":                 1_309.9e6,
    "EBITDA":                     2_386.4e6,
    "Normalized EBITDA":          2_386.4e6,
    "Reconciled Depreciation":      472.8e6,
    "Basic Average Shares":         274.0e6,
    "Diluted Average Shares":       275.0e6,
}

FY2026_BALANCE = {
    "Total Assets":               9_200.0e6,
    "Stockholders Equity":        1_500.0e6,
    "Current Assets":             2_100.0e6,
    "Current Liabilities":        1_600.0e6,
    "Cash And Cash Equivalents":    220.0e6,
    "Total Debt":                 5_400.0e6,
    "Long Term Debt":             5_100.0e6,
    "Inventory":                    720.0e6,
}

FY2026_CASHFLOW = {
    "Operating Cash Flow":        1_650.0e6,
    "Capital Expenditure":         -270.0e6,
    "Free Cash Flow":             1_380.0e6,
}

PEER_DATA = {
    "Company":       ["Dollarama (DOL.TO)", "Dollar Tree (DLTR)", "Dollar General (DG)"],
    "Revenue ($M)":  [7244, 30607, 40612],
    "EBITDA Margin": ["32.9%", "11.9%", "9.6%"],
    "ROIC":          ["~28%", "13.6%", "15.2%"],
    "EV/EBITDA":     ["~29x", "6.5x", "7.4x"],
    "Source":        ["Dollarama IR Mar 2026", "SEC 10-K FY2025", "SEC 10-K FY2025"],
    "Note":          ["FY2026 actuals", "Net loss = $4.27B goodwill impairment", ""],
}

DCF_PARAMS = {
    "Parameter":     ["Base FCF ($B)", "Net Debt ($B)", "Shares (M)",
                      "WACC — base case", "WACC — stress test",
                      "Terminal Growth Rate", "Stage 1 FCF Growth",
                      "Forecast Horizon", "DCF Price — base", "DCF Price — stress",
                      "Rf (GoC 10yr)", "Beta (yfinance live)", "ERP (Damodaran CA)",
                      "IPO Price (CAD)", "IPO Date"],
    "Value":         ["1.397", "2.155", "277",
                      "5.5%", "9.0%",
                      "2.5%", "8.0%",
                      "5 years", "~$213", "~$93",
                      "3.5%", "0.37", "6.5%",
                      "$17.50", "Oct 9 2009"],
    "Source":        ["Dollarama IR (FY2025 actual)", "FY2025 balance sheet ex IFRS 16",
                      "Dollarama IR diluted WA",
                      "CAPM calculated (5.57%) rounded", "Stress test — ~2x CAPM",
                      "Mid-point long-run Canada GDP", "Half of 14% historical CAGR",
                      "Colab Cell 35", "At WACC 5.5%", "At WACC 9.0%",
                      "Bank of Canada Mar 2026", "Yahoo Finance 5yr monthly", "Damodaran 2026",
                      "TSX / Dollarama IR", "Dollarama IR"],
}

FB_FINANCIALS = {
    "Metric":           ["Revenue ($B)", "Gross Profit ($B)", "EBIT ($B)",
                         "Net Income ($B)", "EBITDA ($B)", "EPS (CAD)",
                         "Operating CF ($B)", "CapEx ($B)", "FCF ($B)",
                         "Total Assets ($B)", "Total Debt ($B)", "Equity ($B)", "Cash ($B)",
                         "Gross Margin %", "Net Margin %", "EBITDA Margin %"],
    "FY2022":           [4.331, 1.904, 0.983, 0.663, 1.283, 2.18,
                         1.164, 0.160, 1.004, 4.060, 3.607, -0.066, 0.093,
                         44.0, 15.3, 29.6],
    "FY2023":           [5.053, 2.207, 1.190, 0.802, 1.530, 2.76,
                         0.870, 0.157, 0.713, 4.722, 3.721,  0.237, 0.088,
                         43.6, 15.9, 30.3],
    "FY2024":           [5.867, 2.610, 1.520, 1.010, 1.882, 3.56,
                         1.530, 0.279, 1.251, 5.455, 4.047,  0.713, 0.099,
                         44.5, 17.2, 32.1],
    "FY2025":           [6.413, 2.902, 1.713, 1.169, 2.149, 4.16,
                         1.640, 0.247, 1.397, 6.479, 4.714,  1.191, 0.090,
                         45.1, 18.2, 33.5],
    "FY2026A":          [7.244, 3.274, 1.914, 1.310, 2.386, 4.76,
                         1.650, 0.270, 1.380, 9.200, 5.400,  1.500, 0.220,
                         45.2, 18.1, 32.9],
    "CAGR / Trend":     ["+14% ✓", "", "+18%", "+19%", "+17%", "+21% ✓",
                         "", "3-4% rev", "", "", "Elevated post-TRS", "Improving", "",
                         "Stable", "Expanding", "Expanding"],
    "Source":           ["yfinance (FY22-25) / Dollarama IR (FY26)"] * 16,
}

NLP_RESULTS = {
    "Earnings Call":   ["FY2022 Annual", "FY2023 Annual", "FY2024 Annual",
                        "FY2025 Annual", "FY2026 Q3"],
    "Polarity Score":  ["-8.6%", "+10.0%", "+14.6%", "+14.8%", "+12.6%"],
    "Positive Words":  [11, 19, 24, 26, 24],
    "Negative Words":  [26,  2,  0,  0,  1],
    "Subjectivity %":  ["2.3%", "4.7%", "3.7%", "4.0%", "5.5%"],
    "Signal":          ["Negative", "Positive", "Positive", "Positive ↑ (peak)", "Positive"],
    "Source":          ["Dollarama IR / Seeking Alpha"] * 5,
}

MC_RESULTS = {
    "Parameter":  ["WACC mean", "TGR mean", "FCF Growth mean", "Paths",
                   "P5", "P25", "P50 (Median)", "P75", "P95",
                   "Prob > $212 target", "Prob > $173 (profitable)", "Prob < $130 (stress)"],
    "Value":      ["9.0%", "2.5%", "8.0%", "5,000",
                   "$70", "$84", "$95", "$109", "$134",
                   "0.1%", "0.4%", "93.6%"],
    "Note":       ["Deliberately pessimistic risk lens (not base case)",
                   "Consistent with DCF", "Consistent with DCF", "Speed/precision balance",
                   "5th percentile scenario", "25th percentile scenario",
                   "Median of all 5,000 simulations",
                   "75th percentile scenario", "95th percentile scenario",
                   "Model-dependent — scenario output not forecast",
                   "At 9% WACC mean", "At 9% WACC mean"],
}

ML_RESULTS = {
    "Parameter":  ["Model type", "Features", "Train/test split", "Data",
                   "R² (test set)", "RMSE (test set)", "MA coefficient",
                   "Interpretation", "Used in valuation?"],
    "Value":      ["Linear Regression (sklearn OLS)", "10-day MA + 14-day RSI",
                   "80/20 chronological", "1,255 trading days (DOL.TO live)",
                   "0.884", "$3.84", "1.0027",
                   "Data leakage — MA derived from price itself. "
                   "Coefficient ≈ 1.0 confirms model predicts price "
                   "using a lagged copy of price.",
                   "NO — Tutorial 5 deliverable only. Explicitly excluded."],
}

SNAPSHOT_INFO = {
    "Field":       ["currentPrice", "marketCap", "enterpriseValue",
                    "trailingPE", "forwardPE", "beta",
                    "targetMeanPrice",
                    "pegRatio", "priceToSalesTrailing12Months",
                    "priceToBook", "enterpriseToRevenue", "enterpriseToEbitda",
                    "sharesOutstanding",
                    "Snapshot date", "Source"],
    "Value":       [172.59, 47_070_000_000, 52_130_000_000,
                    36.5, 36.64, 0.37,
                    212.06,
                    3.24, 7.53,
                    40.82, 8.26, 31.55,
                    272_700_000,
                    "April 3, 2026", "Yahoo Finance / Dashboard screenshots"],
    "Note":        ["Live price at time of analysis", "$47.07B", "$52.13B",
                    "From screenshot", "Analysis fallback", "Live yfinance (DCF tab screenshot)",
                    "Our analysis target — hardcoded",
                    "Analysis fallback", "Analysis fallback",
                    "Analysis fallback", "Analysis fallback", "Analysis fallback",
                    "Implied from market cap / price",
                    "", ""],
}


def pull_yfinance():
    """Pull live data from Yahoo Finance. Returns dict of DataFrames + info."""
    print("  Connecting to Yahoo Finance...")
    import yfinance as yf

    dol = yf.Ticker(TICKER)

    print("  Pulling info dict...")
    info = dol.info
    curr_price = (info.get("currentPrice") or info.get("regularMarketPrice") or 172.59)
    print(f"  Current price: ${curr_price:.2f}")

    print("  Pulling annual financial statements (FY2022-FY2025)...")
    income  = dol.financials
    balance = dol.balance_sheet
    cashflow = dol.cashflow

    print("  Pulling 5-year daily price history...")
    end   = datetime.today()
    start = end - timedelta(days=5 * 365)
    hist  = dol.history(start=start.strftime("%Y-%m-%d"),
                        end=end.strftime("%Y-%m-%d"), interval="1d")

    print("  Pulling IPO-to-date price history...")
    try:
        hist_ipo = dol.history(start=IPO_DATE, auto_adjust=True)
    except Exception:
        hist_ipo = hist.copy()
        print("  (IPO history failed — using 5yr history as fallback)")

    # Snapshot the info dict as a tidy DataFrame
    info_keys = [
        "currentPrice", "regularMarketPrice", "marketCap", "enterpriseValue",
        "trailingPE", "forwardPE", "pegRatio", "beta", "targetMeanPrice",
        "priceToSalesTrailing12Months", "priceToBook",
        "enterpriseToRevenue", "enterpriseToEbitda", "sharesOutstanding",
        "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
    ]
    info_df = pd.DataFrame({
        "Field": info_keys,
        "Value": [info.get(k, "") for k in info_keys],
        "Pulled at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    return {
        "info":       info,
        "info_df":    info_df,
        "income":     income,
        "balance":    balance,
        "cashflow":   cashflow,
        "hist":       hist,
        "hist_ipo":   hist_ipo,
        "curr_price": curr_price,
    }


def save_xlsx(data, path="dollarama_snapshot.xlsx"):
    """Write everything to a single Excel workbook."""
    print(f"\nWriting {path}...")

    with pd.ExcelWriter(path, engine="openpyxl") as writer:

        # ── Sheet 1: README ────────────────────────────────────────────────
        readme = pd.DataFrame({
            "Item": [
                "File",
                "Generated",
                "Ticker",
                "Purpose",
                "",
                "HOW DASHBOARD USES THIS FILE",
                "1. Place dollarama_snapshot.xlsx in same folder as Dashboard.py",
                "2. Set PRESENTATION_MODE = True in Dashboard.py",
                "3. Run: streamlit run Dashboard.py",
                "4. All tabs load from this file — no yfinance calls needed",
                "",
                "SHEETS IN THIS FILE",
                "01_live_info        — Market data snapshot (price, beta, P/E, etc.)",
                "02_income           — Annual income statements FY2022-FY2025 (yfinance)",
                "03_balance          — Balance sheets FY2022-FY2025 (yfinance)",
                "04_cashflow         — Cash flow statements FY2022-FY2025 (yfinance)",
                "05_fy2026_hardcoded — FY2026 data (Dollarama IR Q1-Q3 + Q4 consensus)",
                "06_financials_fb    — Full FY2022-FY2026 verified summary table",
                "07_peers            — DLTR / DG peer data (SEC FY2025 10-K)",
                "08_dcf_params       — DCF model parameters and outputs",
                "09_monte_carlo      — Monte Carlo simulation results",
                "10_ml_model         — ML price model results",
                "11_nlp_sentiment    — NLP polarity scoring results",
                "12_price_history    — 5-year daily price history (DOL.TO)",
                "13_price_ipo        — IPO-to-date price history (since Oct 2009)",
            ],
        })
        readme.to_excel(writer, sheet_name="00_README", index=False)

        # ── Sheet 2: Live info snapshot ────────────────────────────────────
        snap_df = pd.DataFrame(SNAPSHOT_INFO)
        if data and "info_df" in data:
            # Merge live values on top of our snapshot
            live_df = data["info_df"]
            snap_df.to_excel(writer, sheet_name="01_live_info_snap", index=False)
            live_df.to_excel(writer, sheet_name="01_live_info_live", index=False)
        else:
            snap_df.to_excel(writer, sheet_name="01_live_info_snap", index=False)

        # ── Sheets 3-5: Annual statements ─────────────────────────────────
        if data:
            for name, df in [("02_income",   data["income"]),
                             ("03_balance",  data["balance"]),
                             ("04_cashflow", data["cashflow"])]:
                if df is not None and not df.empty:
                    df.to_excel(writer, sheet_name=name)
                else:
                    pd.DataFrame({"Note": ["yfinance unavailable — using hardcoded FB values"]}).to_excel(
                        writer, sheet_name=name, index=False)

        # ── Sheet 6: FY2026 hardcoded ──────────────────────────────────────
        fy26 = pd.DataFrame({
            "Statement": (["Income"] * len(FY2026_INCOME) +
                          ["Balance"] * len(FY2026_BALANCE) +
                          ["Cash Flow"] * len(FY2026_CASHFLOW)),
            "Line Item":  (list(FY2026_INCOME.keys()) +
                           list(FY2026_BALANCE.keys()) +
                           list(FY2026_CASHFLOW.keys())),
            "Value ($)":  (list(FY2026_INCOME.values()) +
                           list(FY2026_BALANCE.values()) +
                           list(FY2026_CASHFLOW.values())),
            "Source":     ["Dollarama IR Q1-Q3 actuals + Q4 consensus"] * (
                           len(FY2026_INCOME) + len(FY2026_BALANCE) + len(FY2026_CASHFLOW)),
        })
        fy26.to_excel(writer, sheet_name="05_fy2026_hardcoded", index=False)

        # ── Sheet 7: Full financials summary ──────────────────────────────
        fin_df = pd.DataFrame(FB_FINANCIALS)
        fin_df.to_excel(writer, sheet_name="06_financials_fb", index=False)

        # ── Sheet 8: Peers ─────────────────────────────────────────────────
        peers_df = pd.DataFrame(PEER_DATA)
        peers_df.to_excel(writer, sheet_name="07_peers", index=False)

        # ── Sheet 9: DCF params ───────────────────────────────────────────
        dcf_df = pd.DataFrame(DCF_PARAMS)
        dcf_df.to_excel(writer, sheet_name="08_dcf_params", index=False)

        # ── Sheet 10: Monte Carlo ─────────────────────────────────────────
        mc_df = pd.DataFrame(MC_RESULTS)
        mc_df.to_excel(writer, sheet_name="09_monte_carlo", index=False)

        # ── Sheet 11: ML model ────────────────────────────────────────────
        ml_df = pd.DataFrame(ML_RESULTS)
        ml_df.to_excel(writer, sheet_name="10_ml_model", index=False)

        # ── Sheet 12: NLP ─────────────────────────────────────────────────
        nlp_df = pd.DataFrame(NLP_RESULTS)
        nlp_df.to_excel(writer, sheet_name="11_nlp_sentiment", index=False)

        # ── Sheets 13-14: Price history ───────────────────────────────────
        if data:
            for name, df in [("12_price_history", data["hist"]),
                             ("13_price_ipo",     data["hist_ipo"])]:
                if df is not None and not df.empty:
                    df_out = df[["Open","High","Low","Close","Volume"]].copy()
                    # Strip timezone — Excel cannot handle tz-aware datetime index
                    if hasattr(df_out.index, "tz") and df_out.index.tz is not None:
                        df_out.index = df_out.index.tz_convert(None)
                    df_out.index.name = "Date"
                    df_out.to_excel(writer, sheet_name=name)
                else:
                    pd.DataFrame({"Note": ["Price history unavailable"]}).to_excel(
                        writer, sheet_name=name, index=False)

    print(f"  ✓ Saved {path}")
    return path


def save_csvs(data, folder="csv"):
    """Save each sheet as an individual CSV."""
    os.makedirs(folder, exist_ok=True)
    print(f"\nWriting CSVs to {folder}/...")

    files = {
        "01_live_info_snapshot.csv":   pd.DataFrame(SNAPSHOT_INFO),
        "05_fy2026_hardcoded.csv":     pd.DataFrame({
            "Line Item": (list(FY2026_INCOME.keys()) + list(FY2026_BALANCE.keys()) + list(FY2026_CASHFLOW.keys())),
            "Value":     (list(FY2026_INCOME.values()) + list(FY2026_BALANCE.values()) + list(FY2026_CASHFLOW.values())),
        }),
        "06_financials_summary.csv":   pd.DataFrame(FB_FINANCIALS),
        "07_peers.csv":                pd.DataFrame(PEER_DATA),
        "08_dcf_params.csv":           pd.DataFrame(DCF_PARAMS),
        "09_monte_carlo.csv":          pd.DataFrame(MC_RESULTS),
        "10_ml_model.csv":             pd.DataFrame(ML_RESULTS),
        "11_nlp_sentiment.csv":        pd.DataFrame(NLP_RESULTS),
    }

    if data:
        for name, df in [("02_income.csv",   data.get("income")),
                         ("03_balance.csv",  data.get("balance")),
                         ("04_cashflow.csv", data.get("cashflow")),
                         ("12_price_history.csv", data.get("hist")),
                         ("13_price_ipo.csv",     data.get("hist_ipo"))]:
            if df is not None and not df.empty:
                files[name] = df

        # Live info dict
        if "info_df" in data:
            files["01_live_info_live.csv"] = data["info_df"]

    for fname, df in files.items():
        fpath = os.path.join(folder, fname)
        df.to_csv(fpath, index=(df.index.name == "Date"))
        print(f"  ✓ {fname}")


def main():
    print("=" * 60)
    print("DOLLARAMA DATA EXPORT")
    print(f"Ticker: {TICKER}  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Try to pull live yfinance data
    data = None
    try:
        data = pull_yfinance()
        print(f"\n✓ Live data pulled successfully")
        print(f"  Current price: ${data['curr_price']:.2f}")
        print(f"  Income statement: {data['income'].shape if data['income'] is not None else 'N/A'}")
        print(f"  Price history: {len(data['hist'])} rows" if data['hist'] is not None else "")
    except Exception as e:
        print(f"\n⚠ yfinance failed: {e}")
        print("  Saving hardcoded data only (no live statements or price history)")

    # Save Excel + CSV regardless
    xlsx_path = save_xlsx(data)
    save_csvs(data)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"""
Files saved:
  {xlsx_path}        ← share this with your team
  csv/               ← individual CSVs for reference

HOW TO USE:
  1. Copy dollarama_snapshot.xlsx to the same folder as Dashboard.py
  2. Make sure PRESENTATION_MODE = True in Dashboard.py  (it already is)
  3. Run: streamlit run Dashboard.py

The dashboard will automatically detect the xlsx file and load from it.
Your partner gets identical numbers on Wednesday — no internet needed
for market data.

NOTE: The dashboard still calls yfinance for financial statements
(income / balance / cash flow) because those are historical and never
change. If there is no internet at all on Wednesday, the fallback
hardcoded values (FB dict in Dashboard.py) are used automatically.
""")


if __name__ == "__main__":
    main()