#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "CITADEL_DESK", "headline": "CITADEL ENTERPRISE AMERICAS: Directory scan mapped (Data Operations / Multi-Asset)"},
    {"source": "CITADEL_DESK", "headline": "CITADEL M82_MACROURITIES: Institutional holdings update registered"}
]

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    count = 0
    for item in feeds:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["headline"], now))
        if c.rowcount > 0: count += 1
        
    conn.commit()
    conn.close()
    print(f"🏢 [DAEMON CITADEL]: Inyectadas {count} trazas institucionales.")

if __name__ == "__main__":
    run()
