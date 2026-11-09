#!/usr/bin/env python3
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

wires = [
    (
        "REFINITIV_LSEG_WIRE",
        "[REFINITIV | BRENT_HORMUZ] Brent $112-$114 risk premium sustained on Middle East shipping threat -> Off-Hormuz Merey 16 $93.92 ITM vector locked",
        "PROCESSED",
        0.95,
        "MEREY16_OFF_HORMUZ_HEDGE",
        "LSEG_HORMUZ_STRIKE_FEED"
    ),
    (
        "REFINITIV_LSEG_WIRE",
        "[REFINITIV | FED_RATES] Fed rate path caution amid sticky PPI energy inflation -> UST10Y spread monitoring",
        "BUNKER_HOLD_030X",
        0.85,
        "UST10Y_CREDIT_SPREAD",
        "FED_POLICY_MONITOR"
    ),
    (
        "REFINITIV_LSEG_WIRE",
        "[REFINITIV | ASIA_SEMIS] Asian tech & memory chip volatility (.KS11 KOSPI) -> AI CapEx financing stress validation",
        "BUNKER_HOLD_030X",
        0.82,
        "ASIA_TECH_INFRA",
        "KOSPI_CHIP_FEED"
    )
]

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

# 1. Inserción en m82_multi_stream
for src, hl, status, alpha, asset, trigger in wires:
    cur.execute("""
        INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (src, hl, status, alpha, asset, trigger))

# 2. Asentamiento en macro_dossier
cur.execute("""
    INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score)
    VALUES (
        'REFINITIV_WORKSPACE_WIRE_24OCT',
        'GLOBAL_MACRO_ENERGY_INGEST',
        'Refinitiv Workspace 16:04 VET Feed: Brent $112-$114 Hormuz Risk Premium + Off-Hormuz Merey 16 $93.92 ITM + Fed Rate Caution',
        1.68,
        'BUNKER_HOLD_030X',
        0.95
    )
""")

conn.commit()
conn.close()
print("✅ [M82 LSEG INGEST] Feed de cables de Refinitiv asimilado atómicamente en SQLite3 WAL.")
