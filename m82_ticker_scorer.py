import os, sys, time, sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
MEGA_7 = {'NVDA', 'MSFT', 'AAPL', 'META', 'AMZN', 'GOOGL', 'TSLA'}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def detect_regime(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS price_ticks (asset TEXT PRIMARY KEY, last_price REAL)")
    c.execute("SELECT last_price FROM price_ticks WHERE asset='US10Y'")
    row_us10y = c.fetchone()
    us10y = row_us10y[0] if row_us10y else 5.34

    c.execute("SELECT last_price FROM price_ticks WHERE asset='SPX'")
    row_spx = c.fetchone()
    spx = row_spx[0] if row_spx else 7800.0

    if spx >= 7700.0 and us10y > 5.0:
        return "MELTUP_CONCENTRATED"
    elif us10y > 5.0:
        return "RISK_OFF"
    else:
        return "RISK_ON"

def run_scanner():
    conn = get_db_connection()
    regime = detect_regime(conn)
    
    # Ajuste dinámico por Liquidez + Macro Yield (US10Y > 5.30%)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS price_ticks (asset TEXT PRIMARY KEY, last_price REAL)")
    c.execute("SELECT last_price FROM price_ticks WHERE asset='US10Y'")
    row_us10y = c.fetchone()
    us10y = row_us10y[0] if row_us10y else 5.35

    if us10y >= 5.30:
        drain_scale = 0.30  # Defensivo por tasa de descuento alta
    else:
        drain_scale = 0.50


    tickers_file = os.path.expanduser("~/M82/tickers_sp500.txt")
    if os.path.exists(tickers_file):
        with open(tickers_file, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        tickers = list(MEGA_7) + ['SPY', 'QQQ', 'VENZ34', 'BRENT']

    print(f"🚀 [M82 TICKER SCANNER] Barrido sobre {len(tickers)} activos...")
    print(f" REGIME: {regime} | DRAIN SCALE: {drain_scale*100:.0f}%")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()

    for ticker in tickers:
        base = 75 if (regime == "MELTUP_CONCENTRATED" and ticker in MEGA_7) else 50
        score = int(base * drain_scale)

        prob = 85 if ticker in MEGA_7 else 65
        payoff = 2200 if ticker in MEGA_7 else 1200
        ev = (score / 100.0) * (prob / 100.0) * payoff

        status = 'PENDING' if ev >= 500 else 'SKIPPED_LOW_EV'
        headline = f"Scanner Hit: Dynamic Score Evaluated"
        clean_hl = f"scanner {ticker.lower()} score{score}"
        
        # Intento de inserción con risk_budget_usd; si falla por esquema, realiza fallback simple
        try:
            c.execute("""
                INSERT OR IGNORE INTO m82_multi_stream 
                (daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status, created_at, risk_budget_usd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (f"SCANNER_{ticker}", headline, clean_hl, score, 90, score, ticker, status, now_str, ev * 0.10))
        except sqlite3.OperationalError:
            c.execute("""
                INSERT OR IGNORE INTO m82_multi_stream 
                (daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (f"SCANNER_{ticker}", headline, clean_hl, score, 90, score, ticker, status, now_str))

    conn.commit()
    conn.close()
    print("✅ [BARRIDO FINALIZADO] Tickers registrados exitosamente en m82_database.db")

if __name__ == "__main__":
    run_scanner()
