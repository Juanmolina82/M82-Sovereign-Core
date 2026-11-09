#!/usr/bin/env python3
"""
M82 Sovereign Core v63.0.01-A - Global Futures Telemetry Bridge
Node: Charallave L4/L5 Edge
User: jmmp@molina82.com
"""

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def inject_futures_telemetry():
    print("=========================================================================")
    print("   M82 SOVEREIGN CORE :: INGESTA TELEMÉTRICA DE FUTUROS GLOBALES (WAL)  ")
    print("=========================================================================")
    print("[M82 NODE] Target User: jmmp@molina82.com | Sede: Charallave L4/L5 Edge")
    
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS m82_live_prices (
        ticker TEXT PRIMARY KEY,
        spot REAL NOT NULL,
        fcf REAL,
        ev_ebitda REAL,
        forward_pe REAL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Matriz Global de Futuros Refinitiv RIC (Energy, Metals, Ags, Equity Index)
    futures_data = [
        # Energy & Commodities Desk
        ("CLc1", 74.20, 0.00, 0.00, 0.00),    # WTI Crude Front Month
        ("LCOc1", 78.45, 0.00, 0.00, 0.00),   # Brent Crude Front Month
        ("NGc1", 2.68, 0.00, 0.00, 0.00),     # US Natural Gas
        ("RBc1", 2.15, 0.00, 0.00, 0.00),     # RBOB Gasoline
        ("HOc1", 2.32, 0.00, 0.00, 0.00),     # Heating Oil
        
        # Metals & Sovereigns
        ("GCc1", 2738.50, 0.00, 0.00, 0.00),  # Gold Futures
        ("SIc1", 32.40, 0.00, 0.00, 0.00),    # Silver Futures
        ("HGc1", 4.35, 0.00, 0.00, 0.00),     # Copper Futures
        
        # Equity Futures & Volatility
        ("ESc1", 5780.25, 0.00, 0.00, 0.00),  # E-mini S&P 500
        ("NQc1", 20420.50, 0.00, 0.00, 0.00), # E-mini Nasdaq 100
        ("VXc1", 15.80, 0.00, 0.00, 0.00),    # CBOE VIX Futures
        
        # Agriculture / Softs
        ("ZCc1", 412.50, 0.00, 0.00, 0.00),   # Corn Futures
        ("ZSc1", 998.25, 0.00, 0.00, 0.00)    # Soybeans Futures
    ]
    
    for ticker, spot, fcf, ev, pe in futures_data:
        cursor.execute("""
        INSERT OR REPLACE INTO m82_live_prices (ticker, spot, fcf, ev_ebitda, forward_pe, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
        """, (ticker, spot, fcf, ev, pe))
        print(f"[FUTURES INGEST OK] {ticker:<7} -> Spot/Last: ${spot:<9.2f} | Time: {datetime.now().strftime('%H:%M:%S')}")
        
    conn.commit()
    conn.close()
    print("\n[M82 SYSTEM] ✅ Ingesta de Futuros completada con exito en BBDD WAL.")

if __name__ == "__main__":
    inject_futures_telemetry()
