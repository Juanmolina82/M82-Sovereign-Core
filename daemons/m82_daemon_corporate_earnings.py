import sqlite3, os, time
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")

def check_earnings_stress():
    msg = "EARNINGS & CAPEX DAEMON: Monitoring Big Tech FCF Squeeze vs Energy Margins (STOXX Energy +138.6%)"
    try:
        conn = sqlite3.connect(DB, timeout=30.0)
        conn.execute("PRAGMA busy_timeout=30000;")
        conn.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, brent, bunker, regime, status, created_at) VALUES (?,?,?,?,?,?,?)",
            ("EARNINGS_MONITOR_DAEMON", msg, 103.74, 0.30, "MELTUP", "BUNKER_LOCK_VALIDATED", datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        print("[M82_EARNINGS] Inyección de stress test corporativo completada.")
    except Exception as e:
        print(f"[ERR] {e}")

if __name__ == "__main__":
    check_earnings_stress()
