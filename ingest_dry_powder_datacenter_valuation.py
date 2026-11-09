#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Vector de Inteligencia: Impacto de Dry Powder en Valoraciones de Data Centers y Cap Rates
source = "PE_INFRA_DESK"
headline = "Record Infrastructure Dry Powder Drives Data Center EBITDA Multiples To 20x 30x Via AI Power Grid Premium"

conn = get_db()
c = conn.cursor()

# 1. Asegurar esquema de tabla macro_dosier
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

# 2. Inyectar señal al dosier macro y a la cola multi-stream
now = datetime.datetime.now().isoformat()
c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score)
    VALUES (?, 'PE_DATACENTER_VALUATION', ?, 92.4, 0.04, 1.10, 9.6)
""", (source, headline))

c.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'PROCESSED', ?)
""", (source, headline, now))

conn.commit()

# 3. Generar la tarjeta HD Serif oficial
card_path = generate_hud_card(headline, source)
print(f"✅ Tesis inyectada correctamente en macro_dosier y m82_multi_stream.")
print(f"📸 Tarjeta HUD generada en: {card_path}")

conn.close()
