#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: EIA VENEZUELA CRUDE IMPORTS TO US (PADD 3) INGESTION
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os

db_path = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(db_path, timeout=60.0)
cur = con.cursor()

cur.execute("PRAGMA busy_timeout=60000;")
cur.execute("PRAGMA journal_mode=WAL;")

# 1. Ingesta macro en tabla macro_dossier
cur.execute("""
INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment)
VALUES (
    'EIA_PETROLEUM_MONTHLY_20261106',
    'ENERGY_GEOPO_VENEZUELA',
    'US EIA: US crude imports from Venezuela reached 701K b/d in July 2026 (highest since May 2017) and 655K b/d in Aug — China exports dropped to 0 b/d — US largest single destination PADD 3',
    1.35,
    'M82_EIA_VE_US_701K',
    0.45
);
""")

# 2. Ingesta de indicadores energéticos en m82_global_derivatives (Estructura exacta: 8 columnas)
vals = [
    ('VE_US_EXPORTS_JUL', 'Venezuela Crude to US July b/d', 'ENERGY', 701000.0, 250.5, 0.0, 72.0, 0.98),
    ('VE_US_EXPORTS_AUG', 'Venezuela Crude to US Aug b/d', 'ENERGY', 655000.0, -6.56, 0.0, 68.0, 0.98),
    ('VE_CHINA_EXPORTS', 'Venezuela Crude to China 2026', 'ENERGY', 0.0, -100.0, 0.0, 10.0, 0.98),
    ('PADD3_HEAVY_SOUR', 'PADD 3 Heavy Sour Refining Demand Index', 'ENERGY', 98.4, 1.2, 0.0, 64.0, 0.95),
]

for v in vals:
    cur.execute("""
    INSERT OR REPLACE INTO m82_global_derivatives (symbol, contract_name, asset_class, spot_price, daily_change, pct_change, rsi_14d, val_alpha)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, v)

# 3. Checkpoint WAL TRUNCATE
con.commit()
checkpoint = cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone()
print(f"[M82 EIA VE OK] ✅ Imports a EE. UU. 701K b/d (Jul) / 655K b/d (Ago) sellados. China: 0 b/d. WAL Checkpoint: {checkpoint}")

con.close()
