#!/usr/bin/env python3
import os
import sqlite3
import time
from datetime import datetime, timezone

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def heartbeat():
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    conn = sqlite3.connect(DB_PATH, timeout=60.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            timestamp TEXT
        )
    """)
    conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
    conn.close()
    print(f"[{now_utc}] 🏛️ M82 CITADEL ORCHESTRATOR (L5 EDGE) :: BUNKER 0.30x LOCK :: WAL HEALTHY", flush=True)

if __name__ == "__main__":
    while True:
        try:
            heartbeat()
        except Exception as e:
            print(f"[ORCH ERROR] {e}", flush=True)
        time.sleep(60)
