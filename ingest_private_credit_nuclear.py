#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Vector de Inteligencia: Estructuración de Crédito Privado para Energía Nuclear e IA
source = "PRIVATE_CREDIT_DESK"
headline = "Private Credit Structures Multibillion PPA Backed Debt For Nuclear Power And AI Compute Infrastructure"

conn = get_db()
c = conn.cursor()

# 1. Asegurar esquema de la tabla macro_dosier
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

# 2. Registrar en la base de datos
now = datetime.datetime.now().isoformat()
c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score)
    VALUES (?, 'PRIVATE_CREDIT_NUCLEAR', ?, 94.1, 0.02, 0.85, 9.7)
""", (source, headline))

c.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'PROCESSED', ?)
""", (source, headline, now))

conn.commit()

# 3. Generar la tarjeta HUD Serif
card_path = generate_hud_card(headline, source)
print(f"✅ Tesis inyectada en macro_dosier y m82_multi_stream.")
print(f"📸 Tarjeta HUD generada en: {card_path}")

conn.close()
