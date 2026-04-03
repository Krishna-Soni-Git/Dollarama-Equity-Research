"""
dollarama_data_pull.py
======================
Pulls Dollarama Inc. (DOL.TO) financial data from Yahoo Finance
and saves it as CSV files in the same folder as this script.

Run this once, or whenever you want to refresh the data.
The Streamlit dashboard reads these CSV files as its backup data source.

USAGE
-----
    python dollarama_data_pull.py              # pull & save CSVs
    python dollarama_data_pull.py --show       # print what is in the CSVs
    python dollarama_data_pull.py --schedule   # auto-refresh every 24 hours

OUTPUT FILES
------------
    dollarama_financials.csv    -- annual income / balance / cash flow data
    dollarama_prices.csv        -- monthly price history

REQUIREMENTS
------------
    pip install yfinance pandas
"""

import argparse, os, sys, time
from datetime import datetime

try:
    import pandas as pd
    import yfinance as yf
except ImportError as e:
    print(f"\n  Missing package: {e}")
    print("    Fix:  pip install yfinance pandas\n")
    sys.exit(1)

# ============================================================
# CONFIGURATION
# ============================================================
TICKER         = "DOL.TO"
PEER_TICKERS   = ["DLTR", "DG"]
N_YEARS        = 5
PRICE_PERIOD   = "10y"
PRICE_FREQ     = "1mo"
SCHEDULE_HOURS = 24

_HERE          = os.path.dirname(os.path.abspath(__file__))
FINANCIALS_CSV = os.path.join(_HERE, "dollarama_financials.csv")
PRICES_CSV     = os.path.join(_HERE, "dollarama_prices.csv")

STORE_DATA = {2021: 1391, 2022: 1541, 2023: 1582, 2024: 1607, 2025: 1616}
SSS_DATA   = {2021:  7.2, 2022:  9.5, 2023:  5.2, 2024:  4.8, 2025:  4.5}


# ============================================================
# YAHOO FINANCE HELPERS
# ============================================================
def _safe(df, key, yr, divisor=1e6, default=0.0):
    try:
        cols = [c for c in df.columns if c.year == yr]
        if not cols:
            return default
        val = df.loc[key, cols[0]] if key in df.index else default
        return float(val / divisor) if pd.notna(val) else default
    except Exception:
        return default


def _statements(t):
    try:
        fin = t.income_stmt
        if fin is None or fin.empty:
            fin = t.financials
    except Exception:
        fin = t.financials
    try:
        bal = t.balance_sheet
    except Exception:
        bal = pd.DataFrame()
    try:
        cf = t.cash_flow
        if cf is None or cf.empty:
            cf = t.cashflow
    except Exception:
        cf = pd.DataFrame()
    return fin, bal, cf


def fetch_financials(symbol, n_years=N_YEARS, currency="CAD"):
    print(f"  [{symbol}] fetching financials...", end="", flush=True)
    t = yf.Ticker(symbol)
    fin, bal, cf = _statements(t)
    if fin is None or fin.empty:
        raise ValueError(f"No income statement for {symbol}")
    years = sorted(c.year for c in fin.columns)[-n_years:]
    print(f" years {years}", flush=True)
    rows = []
    for yr in years:
        revt  = _safe(fin, "Total Revenue", yr)
        cogs  = _safe(fin, "Cost Of Revenue", yr)
        xsga  = _safe(fin, "Selling General And Administrative", yr)
        if xsga == 0:
            xsga = _safe(fin, "Operating Expense", yr)
        dp    = _safe(cf,  "Reconciled Depreciation", yr)
        if dp == 0:
            dp = _safe(fin, "Reconciled Depreciation", yr)
        xint  = _safe(fin, "Interest Expense", yr)
        if xint == 0:
            xint = max(0.0, -_safe(fin, "Net Interest Income", yr))
        txt   = _safe(fin, "Tax Provision", yr)
        ni    = _safe(fin, "Net Income", yr)
        epspx = _safe(fin, "Diluted EPS", yr, divisor=1)
        che   = _safe(bal, "Cash And Cash Equivalents", yr)
        if che == 0:
            che = _safe(bal, "Cash Cash Equivalents And Short Term Investments", yr)
        invt  = _safe(bal, "Inventory", yr)
        at_v  = _safe(bal, "Total Assets", yr)
        lct   = _safe(bal, "Current Liabilities", yr)
        dltt  = _safe(bal, "Long Term Debt", yr)
        dlc   = _safe(bal, "Current Debt", yr)
        ceq   = _safe(bal, "Stockholders Equity", yr)
        csho  = _safe(bal, "Diluted Average Shares", yr, divisor=1e6)
        if csho == 0:
            csho = _safe(bal, "Share Issued", yr, divisor=1e6)
        oancf  = _safe(cf, "Operating Cash Flow", yr)
        capx   = abs(_safe(cf, "Capital Expenditure", yr))
        prstkc = abs(_safe(cf, "Repurchase Of Capital Stock", yr))
        rows.append({
            "ticker": symbol, "fyear": yr, "currency": currency,
            "revt": round(revt,2), "cogs": round(cogs,2), "xsga": round(xsga,2),
            "dp": round(dp,2), "xint": round(xint,2), "txt": round(txt,2),
            "ni": round(ni,2), "epspx": round(epspx,4),
            "che": round(che,2), "invt": round(invt,2), "at": round(at_v,2),
            "lct": round(lct,2), "dltt": round(dltt,2), "dlc": round(dlc,2),
            "ceq": round(ceq,2), "oancf": round(oancf,2), "capx": round(capx,2),
            "prstkc": round(prstkc,2), "csho": round(csho,4), "prcc_f": 0.0,
            "store_count": STORE_DATA.get(yr,0) if symbol==TICKER else 0,
            "sss_growth":  SSS_DATA.get(yr,0.0) if symbol==TICKER else 0.0,
            "pulled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    df = pd.DataFrame(rows)
    df = df[df["revt"] > 0].reset_index(drop=True)
    try:
        hist = t.history(period=PRICE_PERIOD, interval=PRICE_FREQ)
        if not hist.empty:
            for idx, row in df.iterrows():
                sub = hist[hist.index.year == int(row["fyear"])]
                if not sub.empty:
                    df.at[idx, "prcc_f"] = round(float(sub["Close"].iloc[-1]), 2)
    except Exception:
        pass
    print(f"  [{symbol}] done  {len(df)} rows")
    return df


def fetch_prices(symbol):
    print(f"  [{symbol}] fetching prices...", end="", flush=True)
    t    = yf.Ticker(symbol)
    hist = t.history(period=PRICE_PERIOD, interval=PRICE_FREQ)
    if hist.empty:
        raise ValueError(f"No price history for {symbol}")
    df = hist.reset_index()[["Date","Open","High","Low","Close","Volume"]].copy()
    df.columns = ["date","open","high","low","close","volume"]
    df["date"]      = df["date"].dt.strftime("%Y-%m-%d")
    df["ticker"]    = symbol
    df["pulled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f" {len(df)} rows")
    return df


# ============================================================
# CSV READ HELPERS  (imported by dashboard)
# ============================================================
def load_financials_csv(path=FINANCIALS_CSV, ticker=TICKER):
    """
    Read the financials CSV and return a DataFrame for one ticker.
    Returns None if not found or empty.
    Drops metadata columns so the result is ready for process_dol().
    """
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path)
        df = df[df["ticker"] == ticker].sort_values("fyear").reset_index(drop=True)
        if df.empty:
            return None
        return df.drop(columns=["ticker","currency","pulled_at"], errors="ignore")
    except Exception:
        return None


def csv_age_hours(path=FINANCIALS_CSV):
    """Hours since the CSV was last written. Returns inf if not found."""
    if not os.path.exists(path):
        return float("inf")
    try:
        return (datetime.now().timestamp() - os.path.getmtime(path)) / 3600
    except Exception:
        return float("inf")


def csv_status(path=FINANCIALS_CSV):
    """Status dict about the CSV backup for use in the dashboard."""
    if not os.path.exists(path):
        return {"exists": False, "stale": True, "age_hours": float("inf"),
                "message": "No CSV found — run:  python dollarama_data_pull.py"}
    age   = csv_age_hours(path)
    stale = age > 24
    try:
        df  = pd.read_csv(path)
        dol = df[df["ticker"] == TICKER]
        n   = len(dol)
        yrs = sorted(dol["fyear"].astype(int).tolist()) if not dol.empty else []
    except Exception:
        n, yrs = 0, []
    return {
        "exists":    True,
        "age_hours": round(age, 1),
        "stale":     stale,
        "n_rows":    n,
        "years":     yrs,
        "path":      path,
        "message": (
            f"CSV backup  {n} years {yrs}  saved {age:.0f}h ago"
            if not stale else
            f"CSV is {age:.0f}h old  run dollarama_data_pull.py to refresh"
        ),
    }


# ============================================================
# DISPLAY
# ============================================================
def show_csvs():
    W = 72
    print("\n" + "=" * W)
    print("  CSV CONTENTS")
    print("=" * W)
    if not os.path.exists(FINANCIALS_CSV):
        print(f"\n  Not found: {FINANCIALS_CSV}")
    else:
        df  = pd.read_csv(FINANCIALS_CSV)
        age = csv_age_hours(FINANCIALS_CSV)
        print(f"\n  {FINANCIALS_CSV}")
        print(f"  Saved {age:.0f}h ago  |  {len(df)} rows")
        print("  " + "-" * (W - 2))
        hdr = (f"  {'Ticker':<8} {'Year':<6} {'Curr':<5} "
               f"{'Revenue':>10} {'EBITDA':>10} {'NI':>9} "
               f"{'EPS':>7} {'FCF':>9} {'Price':>8}")
        print(hdr)
        print("  " + "-" * (W - 2))
        for _, r in df.sort_values(["ticker","fyear"]).iterrows():
            ebitda = r.get("revt",0)-r.get("cogs",0)-r.get("xsga",0)+r.get("dp",0)
            fcf    = r.get("oancf",0) - r.get("capx",0)
            print(f"  {str(r.get('ticker','')):<8} {int(r.get('fyear',0)):<6} "
                  f"{str(r.get('currency','')):<5} "
                  f"${r.get('revt',0):>8,.0f}M  ${ebitda:>8,.0f}M  "
                  f"${r.get('ni',0):>7,.0f}M  ${r.get('epspx',0):>5.2f}  "
                  f"${fcf:>7,.0f}M  ${r.get('prcc_f',0):>7.2f}")
    if not os.path.exists(PRICES_CSV):
        print(f"\n  Not found: {PRICES_CSV}")
    else:
        dp  = pd.read_csv(PRICES_CSV)
        age = csv_age_hours(PRICES_CSV)
        print(f"\n  {PRICES_CSV}")
        print(f"  Saved {age:.0f}h ago  |  {len(dp)} rows")
        for tkr, grp in dp.groupby("ticker"):
            print(f"    {tkr}: {len(grp)} months "
                  f"({grp['date'].min()} to {grp['date'].max()})  "
                  f"${grp['close'].min():.2f} - ${grp['close'].max():.2f}")
    print()


# ============================================================
# MAIN PULL
# ============================================================
def run_pull():
    print(f"\n{'='*60}")
    print(f"  DOLLARAMA DATA PULL  --  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"  Saving to: {_HERE}\n")
    errors = []
    all_fin, all_px = [], []

    print("-- DOL.TO (CAD) " + "-"*44)
    try:
        all_fin.append(fetch_financials(TICKER, N_YEARS, "CAD"))
    except Exception as e:
        errors.append(f"DOL.TO financials: {e}"); print(f"  FAILED: {e}")
    try:
        all_px.append(fetch_prices(TICKER))
    except Exception as e:
        errors.append(f"DOL.TO prices: {e}"); print(f"  FAILED prices: {e}")

    print()
    print("-- Peers (USD) " + "-"*45)
    for sym in PEER_TICKERS:
        try:
            all_fin.append(fetch_financials(sym, N_YEARS, "USD"))
        except Exception as e:
            errors.append(f"{sym}: {e}"); print(f"  FAILED {sym}: {e}")

    print()
    print("-- Writing CSVs " + "-"*44)
    if all_fin:
        try:
            out = pd.concat(all_fin, ignore_index=True)
            out.to_csv(FINANCIALS_CSV, index=False)
            print(f"  Saved {FINANCIALS_CSV}  ({len(out)} rows)")
        except Exception as e:
            errors.append(f"CSV write: {e}"); print(f"  FAILED: {e}")
    if all_px:
        try:
            outp = pd.concat(all_px, ignore_index=True)
            outp.to_csv(PRICES_CSV, index=False)
            print(f"  Saved {PRICES_CSV}  ({len(outp)} rows)")
        except Exception as e:
            errors.append(f"Prices CSV write: {e}"); print(f"  FAILED: {e}")

    show_csvs()
    if errors:
        print(f"Completed with {len(errors)} error(s):")
        for e in errors: print(f"  * {e}")
        return False
    print(f"Done.  Files: {FINANCIALS_CSV}")
    return True


# ============================================================
# CLI
# ============================================================
def main():
    global FINANCIALS_CSV, PRICES_CSV
    parser = argparse.ArgumentParser(
        description="Pull Dollarama data from Yahoo Finance and save as CSV",
        epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--show",       action="store_true",
                        help="Print CSV contents without fetching")
    parser.add_argument("--schedule",   action="store_true",
                        help=f"Auto-refresh every {SCHEDULE_HOURS}h")
    parser.add_argument("--output-dir", default=None,
                        help="Folder to save CSVs (default: script folder)")
    args = parser.parse_args()

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        FINANCIALS_CSV = os.path.join(args.output_dir, "dollarama_financials.csv")
        PRICES_CSV     = os.path.join(args.output_dir, "dollarama_prices.csv")

    if args.show:
        show_csvs(); return

    if not args.schedule:
        sys.exit(0 if run_pull() else 1)

    print(f"\nScheduled mode -- every {SCHEDULE_HOURS}h.  Ctrl+C to stop.\n")
    while True:
        run_pull()
        import datetime as _dt
        nxt = (datetime.now() + _dt.timedelta(hours=SCHEDULE_HOURS)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nNext pull: {nxt}")
        time.sleep(SCHEDULE_HOURS * 3600)


if __name__ == "__main__":
    main()