#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: WALL STREET FULL EQUITY INGESTION DAEMON
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
Data Source: Refinitiv Workspace / LSEG API (jmmp@molina82.com)
"""

import sqlite3
import pathlib
import sys
import time

HOME_DIR = pathlib.Path.home()
DB_PATH = HOME_DIR / "M82" / "m82_database.db"

def init_extended_schema():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    
    # Tabla Extendida de Fundamentales NYSE/NASDAQ (Modelo DELL)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_equity_fundamentals (
            ticker TEXT PRIMARY KEY,
            company_name TEXT,
            exchange TEXT,
            sector TEXT,
            spot_price REAL,
            fcf_yield_fy1 REAL,
            fcf_yield_fy2 REAL,
            fcf_yield_fy3 REAL,
            pe_forward_fy1 REAL,
            ev_ebitda_fy1 REAL,
            net_debt_ebitda REAL,
            roe REAL,
            target_price_mean REAL,
            consensus_rating TEXT,
            esg_combined_score REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("[M82 SCHEMA OK] ✅ Tabla m82_equity_fundamentals preparada en SQLite3 WAL Mode.")

if __name__ == "__main__":
    init_extended_schema()
