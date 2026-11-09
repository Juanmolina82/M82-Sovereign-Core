import sqlite3, time, os
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")

while True:
    try:
        conn = sqlite3.connect(DB, timeout=15.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=15000;")
        
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        h_french = f"[FRENCH_DEBT_CONTAGION | {now_str}] Tracking OAT/Bund 137bps | EU Energy Tariffs"
        conn.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, status, created_at) VALUES (?,?,?,?)",
            ("FRENCH_DEBT_CONTAGION", h_french, "PROCESSED", now_str)
        )
        
        h_icsid = f"[ARBITRATION_ICSID | {now_str}] ICSID litigation risk & Hormuz bypass legal framework"
        conn.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, status, created_at) VALUES (?,?,?,?)",
            ("ARBITRATION_ICSID", h_icsid, "PROCESSED", now_str)
        )
        
        conn.commit()
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.commit()
        conn.close()
        print(f"[{datetime.now()}] [DAEMONS STREAMS] Streams paralelos actualizados.")
    except Exception as e:
        print(f"[DAEMONS STREAMS ERROR]: {e}")
    time.sleep(60)
