#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: MACRO_DOSSIER COMPREHENSIVE SCHEMA REBUILD
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os

db_path = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(db_path, timeout=60.0)
cur = con.cursor()

cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("PRAGMA busy_timeout=60000;")

# 1. Crear tabla temporal con el esquema maestro completo
cur.execute("""
CREATE TABLE IF NOT EXISTS macro_dossier_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT DEFAULT 'SYSTEM',
    category TEXT DEFAULT 'GENERAL',
    headline TEXT NOT NULL,
    risk_score REAL DEFAULT 0.0,
    m82_tag TEXT DEFAULT 'UNTAGGED',
    sentiment REAL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# 2. Migrar datos existentes si la tabla antigua macro_dossier existía
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='macro_dossier';")
if cur.fetchone():
    cur.execute("PRAGMA table_info(macro_dossier);")
    old_cols = [col[1] for col in cur.fetchall()]
    
    # Mapear dinámicamente solo las columnas que existían previamente
    select_cols = []
    for col in ['source', 'category', 'headline', 'risk_score', 'm82_tag', 'sentiment', 'created_at']:
        if col in old_cols:
            select_cols.append(col)
        else:
            select_cols.append(f"NULL AS {col}")
            
    query = f"INSERT INTO macro_dossier_new (source, category, headline, risk_score, m82_tag, sentiment, created_at) SELECT {', '.join(select_cols)} FROM macro_dossier;"
    cur.execute(query)
    cur.execute("DROP TABLE macro_dossier;")

# 3. Renombrar la tabla reconstruida a macro_dossier
cur.execute("ALTER TABLE macro_dossier_new RENAME TO macro_dossier;")
print("[M82 REBUILD] ✅ Tabla macro_dossier reconstruida exitosamente con esquema maestro.")

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

# 6. Checkpoint atómico WAL TRUNCATE
con.commit()
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")

# 7. Verificación final de persistencia
cur.execute("SELECT id, source, category, headline FROM macro_dossier ORDER BY id DESC LIMIT 2;")
rows = cur.fetchall()

print("┌────────────────────────────────────────────────────────────────────────┐")
print("│ M82 SOVEREIGN CORE :: VERIFICACIÓN DE INYECCIÓN POST-RECONSTRUCCIÓN   │")
print("├────────────────────────────────────────────────────────────────────────┤")
for r in rows:
    print(f"│ ID: {r[0]} | SRC: {r[1]:<22} | CAT: {r[2]:<28} │")
print("└────────────────────────────────────────────────────────────────────────┘")

con.close()
