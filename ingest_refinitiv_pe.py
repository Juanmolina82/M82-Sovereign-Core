#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")

signals = [
    ("PRIVATE_EQUITY_DESK", "Global Private Markets Drive Record Capital Deployment Into Energy And Compute Infrastructure"),
    ("PE_FUNDRAISING_DESK", "Blackstone KKR And Brookfield Lead Mega Fund Closures For AI Energy Grid Assets"),
    ("DRY_POWDER_DESK", "Private Credit And Infrastructure Funds Accumulate Record Liquidity For Strategic M&A")
]

conn = get_db()
c = conn.cursor()

now = datetime.datetime.now().isoformat()
for source, headline in signals:
    try:
        c.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PROCESSED', ?)
        """, (source, headline, now))
        conn.commit()
        
        card_path = generate_hud_card(headline, source)
        print(f"✅ Inyectado en M82: [{source}] -> {card_path}")
    except sqlite3.IntegrityError:
        print(f"ℹ️ Ya existente en la base de datos: {headline[:40]}...")

conn.close()
