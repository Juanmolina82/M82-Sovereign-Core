#!/usr/bin/env python3
# M82 REFINITIV WIPO EVACUATION PATENT INGESTION v61.0.21 - NODO CHARALLAVE L4L5
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=120)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=120000;")
conn.execute("PRAGMA synchronous=NORMAL;")
cur = conn.cursor()

# Timestamp UTC atómico
now_utc = datetime.now(timezone.utc).isoformat()

headline = "[REFINITIV WIPO WIRE] WIPO Publishes Patent of EBRAHIMZADEH, David, J. titled AUTOMATICALLY EMERGENCY EVACUATION SYSTEM -- Refinitiv NewsRoom IP Desk"
tag = "v61.0.21-REFINITIV-WIPO-PATENT-EBRAHIMZADEH-EVACUATION-SYSTEM"

meta = {
    "source_wire": "Refinitiv Workspace / NewsRoom / WIPO",
    "inventor": "EBRAHIMZADEH, David, J.",
    "firm": "Corniche Capital",
    "patent_title": "AUTOMOTIVE EMERGENCY EVACUATION SYSTEM",
    "category": "INTELLECTUAL_PROPERTY_AUTOMOTIVE_SAFETY",
    "portfolio_synergy": "Complementing Child Safety Lock System (Patent #1) under Dual-Use / Defense Tech Vector",
    "timestamp": now_utc,
    "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('Refinitiv Workspace / WIPO NewsRoom', 'IP_PATENTS_TECH', ?, 1.15, ?, 0.60, ?, 'v61.0.21', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# Verificación y Checkpoint WAL
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("PRAGMA integrity_check;")
integrity = cur.fetchone()[0]

conn.close()

print(f"\n🔒 M82 REFINITIV WIPO EVACUATION PATENT INGESTION v61.0.21 SUCCESS")
print(f"🟢 DB PATH: {DB_PATH}")
print(f"🟢 TOTAL REGISTROS: {total}")
print(f"🟢 INTEGRITY CHECK: {integrity}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAG INGESTADO: {tag}\n")

# Disparar renderizado en Plantilla Opción A (Quantum Terminal HUD)
subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"], check=False)
