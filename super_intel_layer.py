import sqlite3, time, os, requests, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
NTFY_TOPIC = "M82-Molina-Alerts-v2"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=15000;")
    return conn

def send_to_ntfy(title, message):
    try:
        url = f"https://ntfy.sh/{NTFY_TOPIC}"
        headers = {
            "Title": title,
            "Priority": "high",
            "Tags": "zap,chart_with_upwards_trend,fire",
            "User-Agent": "M82-Quant-Engine/2.0"
        }
        res = requests.post(url, data=message.encode('utf-8'), headers=headers, timeout=5)
        return res.status_code
    except Exception as e:
        return f"ERR:{type(e).__name__}"

def regime_v2():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS price_ticks (asset TEXT PRIMARY KEY, last_price REAL)")
    c.execute("SELECT last_price FROM price_ticks WHERE asset='US10Y'")
    row_us10y = c.fetchone()
    us10y = row_us10y[0] if row_us10y else 5.34

    c.execute("SELECT last_price FROM price_ticks WHERE asset='SPX'")
    row_spx = c.fetchone()
    spx = row_spx[0] if row_spx else 7800.0

    conn.close()

    if spx >= 7700.0 and us10y > 5.0:
        return "MELTUP_CONCENTRATED", us10y, spx
    elif us10y > 5.0:
        return "RISK_OFF", us10y, spx
    else:
        return "RISK_ON", us10y, spx

def super_filter():
    conn = get_db_connection()
    regime, us10y, spx = regime_v2()

    c = conn.cursor()
    c.execute("""
        SELECT id, daemon_source, headline, alpha_score, final_score, asset_impact, created_at 
        FROM m82_multi_stream 
        WHERE status='PENDING' 
        ORDER BY RANDOM()
        LIMIT 30
    """)
    pending_rows = c.fetchall()

    for row in pending_rows:
        id_, src, hl, alpha, final, asset, created_at = row
        score = min(100, final if (final is not None and final > 0) else alpha)
        
        if regime == "MELTUP_CONCENTRATED":
            prob = 35 if asset == "VENZ34" else 85 if ('AI' in str(src) or 'TECH' in str(src) or 'SAMSUNG' in str(src)) else 70
            payoff = 800 if asset == "VENZ34" else 2200
        else:
            prob = 80
            payoff = 1500

        ev = (score / 100.0) * (prob / 100.0) * payoff

        if ev < 500:
            conn.execute("UPDATE m82_multi_stream SET status='SKIPPED_LOW_EV', final_score=? WHERE id=?", (score, id_))
        else:
            title = f"DANEKA M82: 🚨 #M82 BREAKING [{asset}]"
            body = f"[{src} | {created_at}]\n{hl}\n\nScore: {score} | EV: ${ev:.0f} | Regime: {regime}\n\n🏛 @MolinaHoldings LLC | AGI Quantum Node"
            
            st_code = send_to_ntfy(title, body)
            conn.execute("UPDATE m82_multi_stream SET status='DISPATCHED', final_score=? WHERE id=?", (score, id_))
            print(f"🔥 [NTFY STATUS {st_code}] [{src}] -> {asset} | Score: {score}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    super_filter()
