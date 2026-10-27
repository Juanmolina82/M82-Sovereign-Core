#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Vector de Inteligencia: Mix Energético Multidisciplinario y Calibración Térmica Espacial
source = "ADVANCED_ENERGY_DESK"
headline = "Diversified Power Generation Integrates Fusion Nuclear SMRs Solar And Space Heat Systems For Superintelligence Infrastructure"

conn = get_db()
c = conn.cursor()

# 1. Verificar existencia del esquema macro_dosier
c.execute('''
    CREATE TABLE IF NOT EXISTS macro_dosier (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        source TEXT,
        category TEXT,
        headline TEXT,
        gprk_index REAL,
        yield_10y_delta REAL,
        oil_spread_impact REAL,
        risk_score REAL
    )
''')

# 2. Inyectar señal en el dosier macro y en la cola de despacho
now = datetime.datetime.now().isoformat()
c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score)
    VALUES (?, 'DIVERSIFIED_ENERGY_MIX_SPACE_HEAT', ?, 91.3, -0.01, 0.80, 9.6)
""", (source, headline))

c.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'PROCESSED', ?)
""", (source, headline, now))

conn.commit()

# 3. Generar la tarjeta HD Serif en formato oficial
card_path = generate_hud_card(headline, source)
print(f"✅ Vector inyectado correctamente en macro_dosier y m82_multi_stream.")
print(f"📸 Tarjeta HUD generada e indexada en: {card_path}")

conn.close()
