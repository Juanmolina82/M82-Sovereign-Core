import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
BLOCK_CSV = os.path.expanduser("~/M82/lseg_block_trades.csv")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("CREATE TABLE IF NOT EXISTS m82_block_trades (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, ric TEXT, side TEXT, shares INTEGER, price REAL, notional_usd REAL, venue TEXT, status TEXT);")
    conn.commit()
    conn.close()

def process_block_trades():
    if not os.path.exists(BLOCK_CSV):
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(BLOCK_CSV, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ric = row.get("RIC", "").strip()
            side = row.get("Side", "BUY").strip().upper()
            shares = int(row.get("Shares", 0))
            price = float(row.get("Price", 0.0))
            notional = shares * price
            venue = row.get("Venue", "DARK_POOL")
            cur.execute("INSERT INTO m82_block_trades (timestamp, ric, side, shares, price, notional_usd, venue, status) VALUES (?, ?, ?, ?, ?, ?, ?, 'INGESTED_LSEG')", (ts, ric, side, shares, price, notional, venue))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    process_block_trades()
