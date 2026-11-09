#!/usr/bin/env python3
import os, time, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def run_ingest_cycle():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    sample_signals = [
        ("REUTERS_TOP", "Global markets react to central bank interest rate decisions"),
        ("CITGO_OFAC_DESK", "Energy sector export licensing updates issued"),
        ("BRICS_GOLD_RESERVES", "Central banks expand precious metals reserve holdings")
    ]
    
    for source, headline in sample_signals:
        try:
            c.execute("INSERT INTO m82_multi_stream (daemon_source, headline) VALUES (?, ?)", (source, headline))
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    while True:
        try:
            run_ingest_cycle()
        except Exception as e:
            print(f"⚠️ Error en ciclo de ingesta: {e}")
        time.sleep(180)
