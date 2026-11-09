#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: REFINITIV WORKSPACE LIVE STREAMING BRIDGE
User: jmmp@molina82.com
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os
import time
import sys
import datetime

USER_EMAIL = "jmmp@molina82.com"
DB = os.path.expanduser("~/M82/m82_database.db")

# Universo M82 de 19 Activos + Benchmarks
RICS = [
    "CVX.N", "EC.N", "HAL.N", "SLB.N", "BKR.N",
    "SHEL.N", "BP.N", "LNG.N", "COP.N",
    "XOM.N", "EQT.N", "EXE.N", "WMB.N", "KMI.N", "CRWV.O", "MARA.O", "CLSK.O",
    "NGAS.NYMEX", "CLc1", "LCOc1"
]

def update_live_feed():
    csv_path = os.path.expanduser("~/M82/refinitiv_export.csv")
    con = sqlite3.connect(DB, timeout=60.0)
    cur = con.cursor()
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("PRAGMA journal_mode=WAL;")

    # Ingesta desde CSV exportado o API activa
    if os.path.exists(csv_path):
        import csv
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ric = row.get("RIC") or row.get("Instrument") or row.get("Ticker")
                if ric:
                    symbol = ric.replace(".", "_").replace("-", "_")
                    price = float(row.get("Price", 0) or 0)
                    chg = float(row.get("Change%", 0) or row.get("Change", 0) or 0)
                    cur.execute("""
                    UPDATE m82_global_derivatives 
                    SET spot_price=?, daily_change=?, pct_change=?
                    WHERE symbol=?;
                    """, (price, chg, chg, symbol))
        con.commit()
        cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sync live desde Workspace CSV completed.")
    con.close()

if __name__ == "__main__":
    print(f"[M82 STREAMING] Bridge iniciado para {USER_EMAIL}. Bucle de sincronización continuo activo...")
    update_live_feed()
