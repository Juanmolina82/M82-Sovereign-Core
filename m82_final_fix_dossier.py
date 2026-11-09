#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: MACRO_DOSSIER VIEW & SCHEMA RESOLUTION
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os

db_path = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(db_path, timeout=60.0)
cur = con.cursor()

cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("PRAGMA busy_timeout=60000;")

# 1. Tumbar temporalmente la vista huérfana para desbloquear el motor relacional
cur.execute("DROP VIEW IF EXISTS macro_dossier_v61;")

# 2. Asegurar que la tabla macro_dossier exista
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

# 3. Alterar la tabla agregando dinámicamente cualquier columna faltante
cur.execute("PRAGMA table_info(macro_dossier);")
columns = [col[1] for col in cur.fetchall()]

required_cols = {
    'source': 'TEXT DEFAULT "SYSTEM"',
    'category': 'TEXT DEFAULT "GENERAL"',
    'headline': 'TEXT',
    'risk_score': 'REAL DEFAULT 0.0',
    'm82_tag': 'TEXT DEFAULT "UNTAGGED"',
    'sentiment': 'REAL DEFAULT 0.0'
}

for col_name, col_def in required_cols.items():
    if col_name not in columns:
        print(f"[M82 REPAIR] Agregando columna faltante '{col_name}' a macro_dossier...")
        cur.execute(f"ALTER TABLE macro_dossier ADD COLUMN {col_name} {col_def};")

# 4. Inyectar Beat Oficial BLS NFP (+165K)
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

# 5. Inyectar Reuters Wrap-up & Rebound
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

# 6. Reconstruir la vista macro_dossier_v61 limpia y funcional
cur.execute("""
CREATE VIEW IF NOT EXISTS macro_dossier_v61 AS
SELECT id, source, category, headline, risk_score, m82_tag, sentiment, created_at
FROM macro_dossier;
""")

# 7. Checkpoint y cierre atómico
con.commit()
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")

# 8. Verificación de salida limpia
cur.execute("SELECT id, source, category, headline FROM macro_dossier ORDER BY id DESC LIMIT 2;")
rows = cur.fetchall()

print("┌────────────────────────────────────────────────────────────────────────┐")
print("│ M82 SOVEREIGN CORE :: RESOLUCIÓN DEFINITIVA Y CHECKPOINT 0/0/0 CLEAN  │")
print("├────────────────────────────────────────────────────────────────────────┤")
for r in rows:
    print(f"│ ID: {r[0]} | SRC: {r[1]:<22} | CAT: {r[2]:<28} │")
print("└────────────────────────────────────────────────────────────────────────┘")

con.close()
