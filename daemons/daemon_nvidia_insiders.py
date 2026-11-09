#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "NVDA_INSIDER", "headline": "NVDA: Mark Stevens sells indirect shares via Form 4 filings"},
    {"source": "NVDA_INSIDER", "headline": "NVDA: Colette Kress executes scheduled option exercise and Open Market sale"},
    {"source": "NVDA_INSIDER", "headline": "NVDA: Insider Model shows Net Selling pressure over last 12 months"},
    {"source": "NVDA_CORPORATE", "headline": "Nvidia sets biggest-ever buyback plan amidst AI chip market competition"}
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
    print(f"🟢 [DAEMON NVDA]: Inyectadas {count} alertas de insiders.")

if __name__ == "__main__":
    run()
