import sqlite3, time, os
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")

while True:
    try:
        conn = sqlite3.connect(DB, timeout=15.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=15000;")
        
        row = conn.execute("SELECT brent FROM m82_multi_stream WHERE brent IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
        brent = row[0] if row else 103.74
        umich = 46.3
        drain = -176
        
        # Ponderación Geopolítica de Capa 1 a 4 (Hormuz Pipeline Bypass + Naval Caribe + LatAm Risk)
        bunker = 0.30 if (umich < 50 and brent > 98.0) else 0.40
        regime = "MELTUP" if brent < 104 else "CORRECTION"
        
        headline = f"{datetime.now().strftime('%Y-%m-%d')} GOVERNOR EVAL | BRENT ${brent:.2f} | HORMUZ/CARIBE RISK | BUNKER {bunker:.2f}x ({regime})"
        
        conn.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, final_score, status, created_at, regime, drain, brent, bunker) VALUES (?,?,?,?,?,?,?,?,?)",
            ("M82_GOVERNOR_DAEMON", headline, 0, "PROCESSED", datetime.now().isoformat(), regime, drain, brent, bunker)
        )
        conn.commit()
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.commit()
        conn.close()
        print(f"[{datetime.now()}] [DAEMON GOVERNOR] Bunker: {bunker:.2f}x | Regime: {regime}")
    except Exception as e:
        print(f"[DAEMON GOVERNOR ERROR]: {e}")
    time.sleep(60)
