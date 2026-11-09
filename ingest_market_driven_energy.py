#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Vector de Inteligencia: Financiamiento Autónomo por Fuerzas de Mercado en Energía Sostenible para IA
source = "SUSTAINABLE_ENERGY_CAPEX"
headline = "Market Forces Autonomously Fund Nuclear Fusion Fission And Storage Innovation For AI Superintelligence Infrastructure"

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

# 2. Registrar en la matriz de inteligencia y en la cola multi-stream
now = datetime.datetime.now().isoformat()
c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score)
    VALUES (?, 'MARKET_DRIVEN_ENERGY_INNOVATION', ?, 89.1, -0.02, 0.95, 9.5)
""", (source, headline))

c.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'PROCESSED', ?)
""", (source, headline, now))

conn.commit()

# 3. Generar la tarjeta HD Serif estandarizada
card_path = generate_hud_card(headline, source)
print(f"✅ Vector inyectado correctamente en macro_dosier y m82_multi_stream.")
print(f"📸 Tarjeta HUD generada e indexada en: {card_path}")

conn.close()
