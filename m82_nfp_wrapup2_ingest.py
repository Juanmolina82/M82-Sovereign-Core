#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: NFP WRAPUP 2 (MUTIKANI) & BREAKEVEN RATIO INGESTION
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
    'REUTERS_NFP_WRAPUP2_20261106',
    'US_LABOR_NFP_WRAPUP2',
    'Reuters Wrapup2 Mutikani: NFP +165K vs 65K Est Range 35-125K — Breakeven 40K vs 150K 2024 (immigration crackdown) — GDP Q3 +3.4% — Fed 3.75-4.00% — Economists expect HIKE Dec — CPI Tue — Middle East war month 9',
    1.90,
    'M82_NFP_WRAPUP2_HIKE',
    -0.25
);
""")

# 2. Ingesta de derivados e indicadores tácticos
vals = [
    ('US_BREAKEVEN', 'Breakeven Jobs Monthly', 'MACRO_INDICATOR', 40.0, 0.0, 0.0, 40.0, 0.98),
    ('US_GDP_Q3', 'US GDP Q3 Annualized', 'MACRO_INDICATOR', 3.4, 0.0, 0.0, 65.0, 0.98),
    ('US_FED_RATE', 'Fed Funds Mid', 'MACRO_INDICATOR', 3.875, 0.0, 0.0, 50.0, 0.98),
    ('US_NFP_BREAKEVEN_RATIO', 'NFP / Breakeven Ratio', 'MACRO_INDICATOR', 4.12, 0.0, 0.0, 78.0, 0.98),
]

for v in vals:
    cur.execute("""
    INSERT OR REPLACE INTO m82_global_derivatives (symbol, contract_name, asset_class, spot_price, daily_change, pct_change, rsi_14d, val_alpha)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, v)

# 3. Checkpoint atómico WAL TRUNCATE
con.commit()
checkpoint = cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone()
print(f"[M82 WRAPUP2 OK] ✅ Breakeven 40K | GDP 3.4% | HIKE Dic en mesa. WAL Checkpoint: {checkpoint}")

con.close()
