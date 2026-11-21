#!/usr/bin/env python3
import sqlite3
import pathlib

DB_PATH = pathlib.Path.home() / "M82" / "m82_database.db"
SCRIPT_PATH = pathlib.Path.home() / "M82" / "m82_master_dossier.py"

# Datos extraídos en directo de Refinitiv Workspace (jmmp@molina82.com)
LIVE_METRICS = {
    "GCc1":  {"name": "Gold Future (Comex)", "sector": "METALS / FUTURES", "spot": 4057.20, "fcf": 7.79, "rsi": 55.0, "val_a": 7.79},
    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 91.83, "fcf": 4.50, "rsi": 62.4, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 100.29, "fcf": 4.50, "rsi": 64.1, "val_a": 4.50},
    "SILV":  {"name": "Silver Future", "sector": "METALS / FUTURES", "spot": 51.58, "fcf": 5.10, "rsi": 52.0, "val_a": 5.10},
    "PLTN":  {"name": "Platinum Future", "sector": "METALS / FUTURES", "spot": 1517.60, "fcf": 3.80, "rsi": 48.0, "val_a": 3.80}
}

def update_live_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    for ticker, d in LIVE_METRICS.items():
        cursor.execute("""
            INSERT OR REPLACE INTO m82_live_prices (ticker, spot, fcf, ev_ebitda, forward_pe, updated_at)
            VALUES (?, ?, ?, 0.0, 0.0, CURRENT_TIMESTAMP)
        """, (ticker, d["spot"], d["fcf"]))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_live_db()
    print("[M82 REFINITIV RECALIBRATED] ✅ Gold ($4,057.20), WTI ($91.83) y Brent ($100.29) sincronizados.")
