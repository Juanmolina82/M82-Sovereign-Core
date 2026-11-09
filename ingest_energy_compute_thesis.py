#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Tesis fundamental: Acoplamiento de Cómputo e Infraestructura de Energía
source = "AI_INFRA_DESK"
headline = "Energy Is The Core Bottleneck Scaling Superintelligence Computing Power Required For AI Growth"

conn = get_db()
c = conn.cursor()

# 1. Asegurar la tabla de dosier macro
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
    VALUES (?, 'COMPUTE_POWER_GRID', ?, 82.5, 0.05, 1.85, 9.2)
""", (source, headline))

c.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'PROCESSED', ?)
""", (source, headline, now))

conn.commit()

# 3. Generar la tarjeta HD con la plantilla Serif en el formato exacto
card_path = generate_hud_card(headline, source)
print(f"✅ Inyectado en Macro Dosier M82.")
print(f"📸 Tarjeta HUD generada en: {card_path}")

conn.close()
