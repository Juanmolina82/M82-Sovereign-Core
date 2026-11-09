#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")

signals = [
    ("LATAM_DEBT_DESK", "Vale mulls raising over $500 million in debut panda bond sale"),
    ("GLOBAL_BONDS_DESK", "Bonds set for bruising September but stocks little fazed"),
    ("EMERGING_FX_DESK", "Indian central bank likely intervenes to support rupee near 96/USD mark"),
    ("APAC_MACRO_DESK", "Thai August factory output rises 4.44% on year beating forecast")
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
