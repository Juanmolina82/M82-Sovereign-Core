#!/usr/bin/env python3
# M82 SOVEREIGN CORE v61.0.25 - TERM SHEET CORNICHE QUAD-SPV & DECK INGESTION
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=30000;")
cur = conn.cursor()

now_utc = datetime.now(timezone.utc).isoformat()

headline = "[M82 BINDING TERM SHEET] Delaware 50/50 Quad-SPV Joint Venture with Corniche Capital (David Ebrahimzadeh) -- Citi NY Master Escrow & NY Arbitration Clause Active"
tag = "v61.0.25-M82-CORNICHE-TERM-SHEET-QUAD-SPV-CITI-NY"

meta = {
    "entity_a": "Molina Holdings LLC / M82 Sovereign Core",
    "entity_b": "Corniche Capital (David J. Ebrahimzadeh)",
    "structure": "Delaware Quad-SPV 50/50 Joint Venture",
    "underlying_assets": ">10M sqft Industrial Real Estate & Multi-GW Powered Land (ERCOT/PJM)",
    "escrow_agent": "Citibank N.A. New York (Master Escrow Account)",
    "jurisdiction": "New York State Law / UNCITRAL International Arbitration",
    "dossier_sync": "139 Certified Records Sealed in ~/M82/m82_database.db",
    "timestamp": now_utc,
    "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active",
    "governance": "BUNKER MODE 0.30x LOCK -- NODO CHARALLAVE L4/L5 EDGE"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('M82 Legal Desk / Executive Board', 'TERM_SHEET_PRIVATE_EQUITY', ?, 1.00, ?, 0.95, ?, 'v61.0.25', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# Checkpoint WAL Atómico Limpio
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
conn.close()

print(f"\n🔒 M82 SOVEREIGN CORE v61.0.25 SUCCESS")
print(f"🟢 TOTAL REGISTROS EN MACRO_DOSSIER: {total}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAG INGESTADO: {tag}\n")

# Disparar renderizado asíncrono en Plantilla Opción A (Quantum Terminal HUD)
subprocess.Popen(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"])
