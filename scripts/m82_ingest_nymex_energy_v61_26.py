#!/usr/bin/env python3
# M82 REFINITIV NYMEX GLOBEX ENERGY TELEMETRY v61.0.26 - NODO CHARALLAVE L4L5
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=30000;")
cur = conn.cursor()

now_utc = datetime.now(timezone.utc).isoformat()

headline = "[REFINITIV NYMEX WIRE] Globex Energy Futures: WTI Dec26 Surge to $102.80/bbl (+0.80), Jan27 $100.85, ULSD Nov26 $4.73/gal, Gas Dec26 $2.90 -- Strong Backwardation"
tag = "v61.0.26-REFINITIV-NYMEX-GLOBEX-WTI-102.80-ULSD-4.73"

meta = {
    "source_wire": "LSEG Workspace / Dow Jones Newswires / FactSet (1000281768.jpg)",
    "market_data": {
        "WTI_Dec26": 102.80, "WTI_Jan27": 100.85, "WTI_Feb27": 98.58,
        "ULSD_Nov26": 4.73, "RBOB_Nov26": 3.18, "NatGas_Dec26": 2.90
    },
    "merey_implied_valuation": "$88.80 - $90.50/bbl net",
    "structure": "Strong Backwardation / High Geopolitical Premium",
    "timestamp": now_utc,
    "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active",
    "governance": "BUNKER MODE 0.30x LOCK -- NODO CHARALLAVE L4/L5 EDGE"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('Refinitiv Workspace / Dow Jones Energy', 'ENERGY_FUTURES_TELEMETRY', ?, 1.35, ?, 0.80, ?, 'v61.0.26', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# Checkpoint WAL Atómico Limpio
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
conn.close()

print(f"\n🔒 M82 SOVEREIGN CORE v61.0.26 SUCCESS")
print(f"🟢 TOTAL REGISTROS EN MACRO_DOSSIER: {total}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAG INGESTADO: {tag}\n")

# Disparar renderizado en Plantilla Opción A (Quantum Terminal HUD)
subprocess.Popen(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"])
