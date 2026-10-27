#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "M82_WIRE_AI", "headline": "Anthropic IPO prospectus shows sweeping AI vision, surging costs"},
    {"source": "M82_WIRE_MARKETS", "headline": "Nvidia sets biggest-ever buyback plan as AI chip competition weighs on stock"},
    {"source": "M82_WIRE_GEO", "headline": "US, Iran separately talk with mediators in latest bid to end war"},
    {"source": "M82_WIRE_TRADE", "headline": "China, US pledge tariff cuts on $60 billion of goods including agriculture, toys"},
    {"source": "M82_WIRE_TECH", "headline": "SpaceX Starship makes orbital debut deploying Starlinks before early landing"},
    {"source": "M82_WIRE_AI_SAFETY", "headline": "OpenAI Scraps Release of New AI Model Over Safety Concerns"},
    {"source": "M82_WIRE_DEFENSE", "headline": "Raytheon Gets $20.7 Billion Contract to Accelerate AMRAAM Missile Production"}
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
    print(f"🤖 [DAEMON WORLD]: Inyectadas {count} nuevas señales.")

if __name__ == "__main__":
    run()
