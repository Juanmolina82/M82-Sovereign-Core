#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: COLOMBIA OIL TELEMETRY INGESTION (SCHEMA ALIGNED)
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os

db_path = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(db_path, timeout=60.0)
cur = con.cursor()

cur.execute("PRAGMA busy_timeout=60000;")
cur.execute("PRAGMA journal_mode=WAL;")

# 1. Ingesta en macro_dossier
cur.execute("""
INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment)
VALUES (
    'REUTERS_COLOMBIA_OIL_20261106',
    'LATAM_ENERGY_COLOMBIA',
    'Colombia ANH Sep: Oil 729.5K bpd +2.9% YoY — Gas 705 mpcd -13.39% YoY — Imports 40% gas — De La Espriella reactivates exploration — 19.9M ha',
    1.70,
    'M82_COLOMBIA_OIL',
    -0.30
);
""")

# 2. Ingesta alineada a exactamente 8 campos en m82_global_derivatives
vals = [
    ('CO_OIL_SEP', 'Colombia Oil Production bpd', 'ENERGY', 729593.0, -2.92, 0.0, 48.0, 0.98),
    ('CO_GAS_SEP', 'Colombia Gas Production mpcd', 'ENERGY', 705.0, -13.39, 0.0, 35.0, 0.98),
    ('CO_GAS_IMPORT', 'Colombia Gas Import Share %', 'ENERGY', 40.0, 0.0, 0.0, 65.0, 0.98),
    ('CO_EXPLORATION_HA', 'Colombia New Exploration Hectares', 'ENERGY', 19900000.0, 0.0, 0.0, 50.0, 0.98),
]

for v in vals:
    cur.execute("""
    INSERT OR REPLACE INTO m82_global_derivatives (symbol, contract_name, asset_class, spot_price, daily_change, pct_change, rsi_14d, val_alpha)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, v)

# 3. Checkpoint WAL TRUNCATE
con.commit()
checkpoint = cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone()
print(f"[M82 COLOMBIA OK] ✅ Oil 729.5K | Gas -13.39% sellado. WAL Checkpoint: {checkpoint}")

con.close()
