import os, sys, sqlite3, time
from datetime import datetime

try:
    import yfinance as yf
except ImportError:
    pass

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TARGET_TICKERS = ['NVDA', 'MSFT', 'AAPL', 'META', 'AMZN', 'GOOGL', 'TSLA', 'SPY', 'QQQ']

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def analyze_gex_flow():
    conn = get_db_connection()
    c = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"🎯 [M82 OPTIONS & GEX FLOW] Analizando cadena de opciones en Megacaps...")

    for ticker in TARGET_TICKERS:
        try:
            t = yf.Ticker(ticker)
            expirations = t.expirations
            if not expirations:
                continue

            near_exp = expirations[0]
            opt_chain = t.option_chain(near_exp)
            calls = opt_chain.calls
            puts = opt_chain.puts

            call_vol = calls['volume'].sum() if 'volume' in calls else 0
            put_vol = puts['volume'].sum() if 'volume' in puts else 0

            pc_ratio = (put_vol / call_vol) if call_vol > 0 else 1.0

            if pc_ratio < 0.50:
                score = 88
                signal = "HEAVY_CALL_SWEEP_SHORT_GAMMA"
            elif pc_ratio > 1.80:
                score = 35
                signal = "HEAVY_PUT_HEDGE"
            else:
                score = 60
                signal = "NEUTRAL_GAMMA_DELTA"

            drain_scale = 0.50
            final_score = int(score * drain_scale)
            ev = (final_score / 100.0) * (0.85 if ticker in TARGET_TICKERS[:7] else 0.65) * 2200

            status = 'PENDING' if ev >= 500 else 'SKIPPED_LOW_EV'
            headline = f"GEX Flow Signal: {signal} | Put/Call Ratio: {pc_ratio:.2f} (Exp: {near_exp})"
            clean_hl = f"gex {ticker.lower()} pc{pc_ratio:.2f} score{final_score}"

            c.execute("""
                INSERT OR IGNORE INTO m82_multi_stream 
                (daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status, created_at, risk_budget_usd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (f"GEX_{ticker}", headline, clean_hl, final_score, 92, final_score, ticker, status, now_str, ev * 0.10))

            print(f"  └─ {ticker}: PC Ratio {pc_ratio:.2f} -> Score: {final_score} | Status: {status}")

        except Exception as e:
            continue

    conn.commit()
    conn.close()
    print("✅ [GEX FLOW ANALYZED] Cadenas de opciones escaneadas e inyectadas en la DB.")

if __name__ == "__main__":
    analyze_gex_flow()
