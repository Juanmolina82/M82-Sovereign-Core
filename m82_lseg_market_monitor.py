import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
MONITOR_CSV = os.path.expanduser("~/M82/lseg_market_monitor.csv")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS m82_market_monitor_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        symbol TEXT,
        price REAL,
        pct_change REAL,
        event_type TEXT,
        event_magnitude REAL,
        status TEXT
    );
    """)
    conn.commit()
    conn.close()

def process_monitor_events():
    if not os.path.exists(MONITOR_CSV):
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    with open(MONITOR_CSV, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row.get("Symbol", "").strip()
            price = float(row.get("Price", 0.0))
            change = float(row.get("Change", 0.0))
            event_type = row.get("EventType", "UNKNOWN").strip()
            event_mag = float(row.get("EventMagnitude", 0.0))
            
            cur.execute("""
            INSERT INTO m82_market_monitor_events 
            (timestamp, symbol, price, pct_change, event_type, event_magnitude, status) 
            VALUES (?, ?, ?, ?, ?, ?, 'INGESTED_WORKSPACE_MONITOR')
            """, (ts, sym, price, change, event_type, event_mag))
            
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] Market Monitor Events Ingested OK.")

if __name__ == "__main__":
    init_db()
    process_monitor_events()
