#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

headlines_refinitiv = [
    {"source": "M82_WIRE_AI", "text": "Anthropic IPO prospectus shows sweeping AI vision, surging costs"},
    {"source": "M82_WIRE_MARKETS", "text": "Nvidia sets biggest-ever buyback plan as AI chip competition weighs on stock performance"},
    {"source": "M82_WIRE_GEO", "text": "US, Iran separately talk with mediators in latest bid to end war"},
    {"source": "M82_WIRE_TRADE", "text": "China, US pledge tariff cuts on $60 billion of goods including agriculture, toys, toasters"},
    {"source": "M82_WIRE_BANKING", "text": "Goldman's board has discussed plan to name John Waldron as next CEO, WSJ reports"},
    {"source": "M82_WIRE_TECH", "text": "SpaceX's Starship makes orbital debut deploying Starlinks before early landing"},
    {"source": "M82_WIRE_MACRO", "text": "US FAA delays Boeing 737 MAX 10 certification, shares dive 7%"}
]

def load_to_m82():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()

    now = datetime.datetime.now().isoformat()
    inserted = 0

    for item in headlines_refinitiv:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["text"], now))
        if c.rowcount > 0:
            inserted += 1

    conn.commit()
    conn.close()
    print(f"✅ Ingesta de M82 Wire Completada: {inserted} nuevos titulares encolados en M82.")

if __name__ == "__main__":
    load_to_m82()
