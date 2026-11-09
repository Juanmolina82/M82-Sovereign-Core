import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
SECTORS_CSV = os.path.expanduser("~/M82/lseg_all_sectors.csv")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS m82_all_sectors_telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        sector TEXT,
        ric_symbol TEXT,
        price REAL,
        pct_change REAL,
        volume_notional REAL,
        m82_action_tag TEXT,
        status TEXT
    );
    """)
    conn.commit()
    conn.close()

def process_all_sectors():
    if not os.path.exists(SECTORS_CSV):
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    with open(SECTORS_CSV, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sec = row.get("Sector", "MACRO_GENERAL").strip()
            ric = row.get("RIC_Symbol", "").strip()
            price = float(row.get("Price", 0.0))
            change = float(row.get("ChangePct", 0.0))
            notional = float(row.get("VolumeNotional", 0.0))
            tag = row.get("M82Tag", "HOLD_BUNKER").strip()
            
            cur.execute("""
            INSERT OR IGNORE INTO m82_all_sectors_telemetry 
            (timestamp, sector, ric_symbol, price, pct_change, volume_notional, m82_action_tag, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 'VERIFIED_ALL_SECTORS')
            """, (ts, sec, ric, price, change, notional, tag))
            
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] M82 All-Sectors Telemetry Ingested OK.")

if __name__ == "__main__":
    init_db()
    process_all_sectors()
