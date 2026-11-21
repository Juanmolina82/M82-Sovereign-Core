#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Titulares extraídos directamente de la pantalla M82 Wire Workspace
headlines = [
    ("M82_WIRE_AI_GEOPOLITICS", "China's AI agents can lie and scheme — just like their US rivals"),
    ("M82_WIRE_APAC_RISK", "North Korea calls DMZ mine blast a farce as UN Command says armistice breach occurred"),
    ("M82_WIRE_MACRO_INFLATION", "Australia inflation unexpectedly high in August, dampening rate cut hopes"),
    ("M82_WIRE_ENERGY_LNG", "Trump set to tout Korean investment in Alaska LNG, other projects, sources say")
]

conn = get_db()
c = conn.cursor()

now = datetime.datetime.now().isoformat()
for source, headline in headlines:
    try:
        c.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PROCESSED', ?)
        """, (source, headline, now))
        conn.commit()
        
        # Generar la tarjeta HD inmediata para la señal principal
        card_path = generate_hud_card(headline, source)
        print(f"✅ Inyectado y Tarjeta Generada: [{source}] -> {card_path}")
    except sqlite3.IntegrityError:
        print(f"ℹ️ Titular ya registrado: {headline[:40]}...")

conn.close()
