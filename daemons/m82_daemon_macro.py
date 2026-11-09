import sqlite3, time, os
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")

while True:
    try:
        umich = 46.3
        drain = -176
        conn = sqlite3.connect(DB, timeout=15.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=15000;")
        
        headline = f"MACRO METRICS | UMICH: {umich} | DRAIN: {drain}B | LATAM INFLATION HIGH | CHINA-EU DEAL"
        conn.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, final_score, status, created_at, drain) VALUES (?,?,?,?,?,?)",
            ("MACRO_MONITOR_DAEMON", headline, 0, "PROCESSED", datetime.now().isoformat(), drain)
        )
        conn.commit()
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.commit()
        conn.close()
        print(f"[{datetime.now()}] [DAEMON MACRO] UMich {umich} | Drain {drain}B | China/LatAm Integrated")
    except Exception as e:
        print(f"[DAEMON MACRO ERROR]: {e}")
    time.sleep(60)
