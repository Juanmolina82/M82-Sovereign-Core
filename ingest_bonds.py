#!/usr/bin/env python3
import sqlite3, os, json
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
VAULT_PATH = os.path.expanduser("~/M82/vault/protected/vault.json")

# 1. Cargar credencial validada LSEG
user_lseg = "jmmp@molina82.com"
if os.path.exists(VAULT_PATH):
    try:
        with open(VAULT_PATH, "r") as f:
            vdata = json.load(f)
            user_lseg = vdata.get("LSEG_USER", user_lseg)
    except Exception:
        pass

# 2. Vector de Precios OCR Workspace (Refinitiv / BGN)
bonds = [
    ("VENZ_13.625_2018A", 58.278, 59.537, 58.908),
    ("VENZ_13.625_2018B", 57.832, 59.234, 58.533),
    ("VENZ_7.000_2018", 44.172, 44.947, 44.560),
    ("VENZ_7.750_2019", 48.719, 49.552, 49.136),
    ("VENZ_6.000_2020", 42.775, 43.628, 43.201),
    ("VENZ_12.750_2022", 57.528, 58.440, 57.984),
    ("VENZ_9.000_2023", 49.719, 50.595, 50.157),
    ("VENZ_8.250_2024", 49.064, 49.980, 49.522),
    ("VENZ_7.650_2025", 48.254, 49.135, 48.695),
    ("VENZ_11.750_2026", 56.744, 57.722, 57.233),
    ("VENZ_9.250_2027", 51.577, 52.329, 51.953),
    ("VENZ_9.250_2028", 51.315, 52.077, 51.696),
    ("VENZ_11.950_2031", 56.343, 57.172, 56.776),
    ("VENZ_9.375_2034", 51.291, 52.023, 51.657),
    ("VENZ_7.000_2038", 44.560, 45.317, 44.939),
    ("PDVSA_8.500_2020", 114.944, 115.686, 115.315),
    ("PDVSA_9.000_2021", 45.900, 46.689, 46.295),
    ("PDVSA_6.000_2022", 37.613, 38.414, 38.014),
    ("PDVSA_12.750_2022", 51.868, 52.706, 52.287),
    ("PDVSA_6.000_2024", 39.374, 39.984, 39.679),
    ("PDVSA_6.000_2026", 39.339, 40.044, 39.692),
    ("PDVSA_5.375_2027", 38.093, 38.889, 38.491),
    ("PDVSA_9.750_2035", 47.413, 48.267, 47.840),
    ("PDVSA_5.500_2037", 38.242, 38.997, 38.620)
]

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

# Ingesta price_ticks
for asset, bid, ask, last in bonds:
    cur.execute("""
        INSERT OR REPLACE INTO price_ticks (asset, bid, ask, last_price, updated_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (asset, bid, ask, last))

# Registración en el Stream Multicanal
headline = f"[LSEG WORKSPACE | {user_lseg}] Extracción OCR exitosa: 24 Bonos Sovereign/PDVSA (PDVSA20 @ $115.31, VENZ26 @ $57.23, PDVSA26 @ $39.69)"
cur.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
    VALUES ('REFINITIV_OCR_DESK', ?, 'PROCESSED', 0.95, 'SOVEREIGN_DEBT_CURVE', 'LSEG_WORKSPACE_BOND_INGEST')
""", (headline,))

conn.commit()
conn.close()
print(f"✅ [M82 LSEG INGEST] 24 Bonos asimilados en price_ticks bajo usuario {user_lseg}.")
