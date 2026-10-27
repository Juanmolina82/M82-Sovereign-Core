#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

signals = [
    ("M82_WIRE_APAC_AI", "Chinese factory activity expands in September amid AI boom"),
    ("M82_WIRE_LATAM_FX", "LatAm assets mixed as rising dollar yields offset metals support"),
    ("M82_WIRE_ENERGY_LNG", "Trump set to tout Korean investment in Alaska LNG projects"),
    ("M82_WIRE_CHINA_DEBT", "China's next big export could be $1.5 trillion of debt")
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
        print(f"✅ Inyectado y Tarjeta Creada: [{source}] -> {card_path}")
    except sqlite3.IntegrityError:
        print(f"ℹ️ Ya indexado previamente: {headline[:40]}...")

conn.close()
