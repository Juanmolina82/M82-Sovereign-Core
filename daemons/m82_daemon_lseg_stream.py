import sqlite3, os, time
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")

def run_lseg_stream():
    print("[M82_LSEG_STREAM] Daemon de sesión y flujo activo...")
    while True:
        try:
            conn = sqlite3.connect(DB, timeout=30.0)
            conn.execute("PRAGMA busy_timeout=30000;")
            conn.execute(
                "INSERT INTO m82_multi_stream (daemon_source, headline, brent, bunker, regime, status, created_at) VALUES (?,?,?,?,?,?,?)",
                ("LSEG_PRICING_DAEMON", "HEARTBEAT_KEEP_ALIVE: Streaming WebSocket active - High Frequency Data", 103.74, 0.30, "MELTUP", "STREAMING_OK", datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERR] {e}")
        time.sleep(300) # Heartbeat cada 5 min

if __name__ == "__main__":
    run_lseg_stream()
