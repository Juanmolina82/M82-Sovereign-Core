import sqlite3, os, time
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")

def monitor_carry():
    while True:
        try:
            conn = sqlite3.connect(DB, timeout=30.0)
            conn.execute("PRAGMA busy_timeout=30000;")
            conn.execute(
                "INSERT INTO m82_multi_stream (daemon_source, headline, brent, bunker, regime, status, created_at) VALUES (?,?,?,?,?,?,?)",
                ("ARBITRATION_CARRY_DAEMON", "CARRY MONITOR: LatAm fiscal rigidity / ICSID claims yielding high carry - Lock 0.30x", 103.74, 0.30, "MELTUP", "CARRY_OPTIMAL", datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
        except Exception as e:
            pass
        time.sleep(600)

if __name__ == "__main__":
    monitor_carry()
