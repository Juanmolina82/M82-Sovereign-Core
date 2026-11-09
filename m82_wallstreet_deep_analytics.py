#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: UNIVERSAL WALL STREET DEEP ANALYTICS ENGINE
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
Feeder Account: Refinitiv Workspace / LSEG API (jmmp@molina82.com)
Scope: Full NYSE/NASDAQ/AMEX Spectrum (+4,000 Tickers) under DELL Model
"""

import sqlite3
import pathlib

DB_PATH = pathlib.Path.home() / "M82" / "m82_database.db"

def upgrade_schema_dell_style():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    
    # Reestructuración atómica del esquema m82_global_equities
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_global_equities_deep (
            ticker TEXT PRIMARY KEY,
            company_name TEXT,
            exchange TEXT,
            sector TEXT,
            industry TEXT,
            spot_price REAL,
            market_cap_b REAL,
            fcf_yield_fy1 REAL,
            fcf_yield_fy2 REAL,
            fcf_yield_fy3 REAL,
            forward_pe REAL,
            ev_ebitda REAL,
            net_debt_ebitda REAL,
            roe REAL,
            roic REAL,
            target_price_mean REAL,
            target_price_high REAL,
            target_price_low REAL,
            consensus_rating TEXT,
            esg_combined_score REAL,
            quant_alpha_score REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("[M82 DEEP MODEL OK] ✅ Esquema extendido estilo DELL desplegado en SQLite3 WAL Mode.")

if __name__ == "__main__":
    upgrade_schema_dell_style()
