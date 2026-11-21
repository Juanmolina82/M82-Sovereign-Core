#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: GLOBAL MULTI-ASSET INGESTION ENGINE
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
Data Account: Refinitiv Workspace / LSEG API (jmmp@molina82.com)
"""

import sqlite3
import pathlib

DB_PATH = pathlib.Path.home() / "M82" / "m82_database.db"

def init_global_schema():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    
    # 1. Tabla de Renta Variable Global (Modelado tipo DELL)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_global_equities (
            ticker TEXT PRIMARY KEY,
            asset_name TEXT,
            exchange TEXT,
            sector TEXT,
            spot_price REAL,
            fcf_yield_fy1 REAL,
            fcf_yield_fy2 REAL,
            fcf_yield_fy3 REAL,
            forward_pe REAL,
            ev_ebitda REAL,
            net_debt_ebitda REAL,
            roe REAL,
            target_price_mean REAL,
            esg_score REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Tabla de Futuros, Commodities y FX
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_global_derivatives (
            symbol TEXT PRIMARY KEY,
            contract_name TEXT,
            asset_class TEXT,
            spot_price REAL,
            daily_change REAL,
            pct_change REAL,
            rsi_14d REAL,
            val_alpha REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 3. Tabla de Tasas y Deuda Soberana
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_global_rates (
            country TEXT,
            tenor TEXT,
            yield_pct REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (country, tenor)
        );
    """)

    conn.commit()
    conn.close()
    print("[M82 GLOBAL SCHEMA OK] ✅ Tablas multiactivo inicializadas en SQLite3 WAL Mode.")

if __name__ == "__main__":
    init_global_schema()
