#!/usr/bin/env python3
import sqlite3, os, datetime
from m82_engine_master import generate_hud_card, get_db

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Vector de Inteligencia: Riesgo Crediticio en SMR para Infraestructura AI
source = "SMR_CREDIT_RISK_DESK"
headline = "Private Debt Markets Demand 1.5x DSCR Coverage And FOAK Contingency Reserves For SMR Nuclear Projects"

conn = get_db()
c = conn.cursor()

now = datetime.datetime.now().isoformat()

# 1. Registrar en la matriz macro_dosier
c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score)
    VALUES (?, 'SMR_CREDIT_RISK', ?, 95.8, 0.05, 0.70, 9.8)
""", (source, headline))

# 2. Registrar en la cola m82_multi_stream
c.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'PROCESSED', ?)
""", (source, headline, now))

conn.commit()

# 3. Generar la tarjeta HUD Serif
card_path = generate_hud_card(headline, source)
print(f"✅ Análisis de Riesgo SMR registrado en m82_database.db.")
print(f"📸 Tarjeta HUD disponible en: {card_path}")

conn.close()
