#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: MACRO_DOSSIER SCHEMA REPAIR & INGESTION RECOVER
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os

db_path = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(db_path, timeout=60.0)
cur = con.cursor()

cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("PRAGMA busy_timeout=60000;")

# 1. Asegurar la creación o alteración limpia de la tabla macro_dossier
cur.execute("""
CREATE TABLE IF NOT EXISTS macro_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    category TEXT,
    headline TEXT,
    risk_score REAL,
    m82_tag TEXT,
    sentiment REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# 2. Verificar y agregar columna 'source' si la tabla existía con esquema previo
cur.execute("PRAGMA table_info(macro_dossier);")
columns = [column[1] for column in cur.fetchall()]

if 'source' not in columns:
    print("[M82 REPAIR] Modificando esquema: Agregando columna 'source' a macro_dossier...")
    cur.execute("ALTER TABLE macro_dossier ADD COLUMN source TEXT;")

# 3. Re-inyección atómica del Beat Oficial BLS NFP (+165K)
cur.execute("""
INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment)
VALUES (
    'BLS_NFP_20261106_ACTUAL',
    'US_LABOR_MARKET_NFP',
    'BLS Actual 06-Nov: NFP Oct +165K vs +65K Est BEAT +100K — Unemployment 4.1% — Wages 3.1% YoY vs 2.9% Est — Revisions Ago +53K Sep +31K — Prof Business +70K Health +42K',
    1.65,
    'M82_MACRO_NFP_BEAT',
    -0.15
);
""")

# 4. Re-inyección atómica del Reuters Wrap-up & Rebound
cur.execute("""
INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment)
VALUES (
    'REUTERS_WRAPUP_20261106',
    'GLOBAL_MARKETS_STABILISATION',
    'Reuters Wrapup: Nasdaq Fut +1.5% bounce after -5.5% -$2.5T — Nikkei -6% KOSPI -6% Taiwan -4.5% close (-12.2% wk) Europe -1.5% — US10Y 4.86% — NVDA +0.4% — Softbank -11% CDS 4y high — Oil to $107 worst wk since 2020',
    1.80,
    'M82_WRAPUP_BOUNCE',
    -0.10
);
""")

# 5. Checkpoint y cierre WAL
con.commit()
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
print("[M82 REPAIR OK] ✅ Esquema corregido, NFP Beat + Reuters Wrap-up inyectados cleanly (0/0/0 CHECKPOINTED).")
con.close()
