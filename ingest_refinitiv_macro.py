#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

data_events = [
    {"source": "M82_WIRE_OIL", "text": "Middle East Oil Exports Rebound as Hormuz Stranglehold Eases"},
    {"source": "M82_WIRE_TECH", "text": "OpenAI Scraps Release of New AI Model Over Safety Concerns"},
    {"source": "M82_WIRE_DEFENSE", "text": "Raytheon Gets $20.7 Billion Contract to Accelerate AMRAAM Missile Production"},
    {"source": "M82_WIRE_BONDS", "text": "US Treasury 2Y/10Y Yield Curve Adjusts Ahead of Inflation Releases"},
    {"source": "M82_WIRE_ECB", "text": "Eurozone Inflation Set to Rise, ECB's Lagarde Says"}
]

def load_macro_data():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()

    now = datetime.datetime.now().isoformat()
    inserted = 0

    for item in data_events:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["text"], now))
        if c.rowcount > 0:
            inserted += 1

    conn.commit()
    conn.close()
    print(f"✅ Ingesta Macro de M82 Wire completada: {inserted} eventos registrados.")

if __name__ == "__main__":
    load_macro_data()
