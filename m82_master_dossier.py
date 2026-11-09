#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN EXECUTION CORE :: FULL EQUITIES & DERIVATIVES DOSSIER
Caracas HQ Central (Core Mainframe) ⊗ Charallave Edge L4/L5 (Execution Node)
Firmware Tag: M82_DOSSIER_ROBUSTO — HQ CARACAS — Edge Charallave
Gobernanza: BUNKER MODE / 0.30x LOCK (Custodia Pasiva)
"""

import sys
import sqlite3
import pathlib

HOME_DIR = pathlib.Path.home()
M82_DIR = HOME_DIR / "M82"
DB_PATH = M82_DIR / "m82_database.db"

PRESETS = {
    # Equities Basket (10 Activos)
    "DELL.N": {"name": "Dell Technologies Inc.", "sector": "TECHNOLOGY", "spot": 118.50, "fcf": 6.49, "rsi": 42.1, "val_a": 4.75},
    "NVDA":   {"name": "NVIDIA Corporation", "sector": "SEMICONDUCTORS", "spot": 125.40, "fcf": 2.10, "rsi": 61.2, "val_a": 2.10},
    "AAPL":   {"name": "Apple Inc.", "sector": "TECHNOLOGY", "spot": 224.30, "fcf": 3.80, "rsi": 52.4, "val_a": 3.80},
    "MSFT":   {"name": "Microsoft Corporation", "sector": "TECHNOLOGY", "spot": 428.10, "fcf": 3.10, "rsi": 49.8, "val_a": 3.10},
    "GOOGL":  {"name": "Alphabet Inc.", "sector": "COMMUNICATIONS", "spot": 165.20, "fcf": 4.20, "rsi": 45.3, "val_a": 4.20},
    "AMZN":   {"name": "Amazon.com Inc.", "sector": "CONSUMER DISCRETIONARY", "spot": 186.50, "fcf": 3.90, "rsi": 54.1, "val_a": 3.90},
    "META":   {"name": "Meta Platforms Inc.", "sector": "COMMUNICATIONS", "spot": 585.00, "fcf": 4.10, "rsi": 58.7, "val_a": 4.10},
    "AVGO":   {"name": "Broadcom Inc.", "sector": "SEMICONDUCTORS", "spot": 172.80, "fcf": 3.40, "rsi": 51.0, "val_a": 3.40},
    "TSM":    {"name": "Taiwan Semiconductor", "sector": "SEMICONDUCTORS", "spot": 190.50, "fcf": 3.85, "rsi": 56.2, "val_a": 3.85},
    "AMD":    {"name": "Advanced Micro Devices", "sector": "SEMICONDUCTORS", "spot": 155.40, "fcf": 2.50, "rsi": 44.0, "val_a": 2.50},
    
    # Futuros & Derivados
    "CLc1":   {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 91.83, "fcf": 4.50, "rsi": 48.0, "val_a": 4.50},
    "LCOc1":  {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 100.29, "fcf": 4.50, "rsi": 48.0, "val_a": 4.50},
    "GCc1":   {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 4057.20, "fcf": 7.79, "rsi": 55.0, "val_a": 7.79},
    "ESc1":   {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "rsi": 50.0, "val_a": 3.50},
    "NQc1":   {"name": "Nasdaq 100 Future", "sector": "INDEX / FUTURES", "spot": 20420.50, "fcf": 3.80, "rsi": 53.0, "val_a": 3.80},
    "VXc1":   {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "rsi": 35.0, "val_a": 2.00}
}

def sync_to_db():
    M82_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_live_prices (
            ticker TEXT PRIMARY KEY,
            spot REAL,
            fcf REAL,
            ev_ebitda REAL,
            forward_pe REAL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    for ticker, d in PRESETS.items():
        cursor.execute("""
            INSERT OR REPLACE INTO m82_live_prices (ticker, spot, fcf, ev_ebitda, forward_pe, updated_at)
            VALUES (?, ?, ?, 0.0, 0.0, CURRENT_TIMESTAMP)
        """, (ticker, d["spot"], d["fcf"]))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    sync_to_db()
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'DELL.N'
    d = PRESETS.get(ticker)
    if d:
        line = '┌' + '─'*58 + '┐'
        head = '│ M82 DOSSIER TELEMETRY :: ' + f'{ticker:<31}' + '│'
        sep  = '├' + '─'*58 + '┤'
        n_str = '│ Asset Name : ' + f'{d.get("name", "N/A"):<43}' + '│'
        s_str = '│ Sector     : ' + f'{d.get("sector", "N/A"):<43}' + '│'
        p_str = '│ Spot Price : $' + f'{d.get("spot", 0.0):<42.2f}' + '│'
        f_str = '│ FCF Yield  : ' + f'{d.get("fcf", 0.0):<41.2f}' + '% │'
        r_str = '│ RSI (14D)  : ' + f'{d.get("rsi", 0.0):<43.1f}' + '│'
        v_str = '│ Val Alpha  : ' + f'{d.get("val_a", 0.0):<43.2f}' + '│'
        bot  = '└' + '─'*58 + '┘'
        print('\n' + '\n'.join([line, head, sep, n_str, s_str, p_str, f_str, r_str, v_str, bot]) + '\n')
    else:
        print('[M82] Ticker no encontrado: ' + str(ticker))
    sys.exit(0)

def show_quant_doctrine():
    import sqlite3, pathlib
    db = pathlib.Path.home() / 'M82' / 'm82_database.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT principle_name, m82_implementation FROM m82_quant_doctrine;')
    rows = c.fetchall()
    print('┌────────────────────────────────────────────────────────────────────────┐')
    print('│ M82 SOVEREIGN CORE :: DOCTRINA CUANTITATIVA ANONIMIZADA               │')
    print('├────────────────────────────────────────────────────────────────────────┤')
    for r in rows:
        print(f'│ • {r[0]:<25} : {r[1]:<43} │')
    print('└────────────────────────────────────────────────────────────────────────┘')
    conn.close()
