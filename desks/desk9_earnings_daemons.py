#!/usr/bin/env python3
import sqlite3, os, time, random

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

DAEMONS = [
    ("EARNINGS_TOP_RESULTS_DAEMON", "EARNINGS", "Top Financial Results & Guidance Beats"),
    ("EARNINGS_BY_SECTOR_DAEMON", "EARNINGS", "Sector Margin & Revenue Multiples Tracker"),
    ("EARNINGS_UPCOMING_DAEMON", "EARNINGS", "Upcoming Earnings Calendar & Wall St Consensus"),
    ("EARNINGS_SURPRISE_DAEMON", "EARNINGS", "EPS & EBITDA Surprise Metric Analyzer"),
    ("EARNINGS_PREVIEW_DAEMON", "EARNINGS", "Institutional Earnings Previews & Transcripts")
]

def register_daemons():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    for name, desk, vector in DAEMONS:
        c.execute("""
            INSERT OR REPLACE INTO m82_daemons_registry (daemon_name, desk_category, vector_type, status, last_heartbeat)
            VALUES (?, ?, ?, 'ACTIVE', CURRENT_TIMESTAMP)
        """, (name, desk, vector))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    register_daemons()
    print("✅ 5 Daemons de Earnings registrados e instanciados en m82_daemons_registry.")
