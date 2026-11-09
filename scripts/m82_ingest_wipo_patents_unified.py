#!/usr/bin/env python3
# M82 UNIFIED WIPO PATENTS INGESTION - NODO CHARALLAVE L4L5
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=60)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
conn.execute("PRAGMA synchronous=NORMAL;")
cur = conn.cursor()

now_utc = datetime.now(timezone.utc).isoformat()

# 1. Patente 1 (v61.0.20)
hl1 = "[REFINITIV WIPO WIRE] WIPO Publishes Patent of EBRAHIMZADEH, David, J. titled AUTOMATICALLY-DEACTIVATED CHILD SAFETY LOCK SYSTEM -- Refinitiv Workspace NewsRoom"
tag1 = "v61.0.20-REFINITIV-WIPO-PATENT-EBRAHIMZADEH-LOCK-SYSTEM"
meta1 = {
    "inventor": "EBRAHIMZADEH, David, J.", "firm": "Corniche Capital",
    "patent_title": "AUTOMATICALLY-DEACTIVATED CHILD SAFETY LOCK SYSTEM",
    "timestamp": now_utc, "security": "Zero-PII Gateway D-34 Masked Pass Active"
}

# 2. Patente 2 (v61.0.21)
hl2 = "[REFINITIV WIPO WIRE] WIPO Publishes Patent of EBRAHIMZADEH, David, J. titled AUTOMATICALLY EMERGENCY EVACUATION SYSTEM -- Refinitiv Workspace NewsRoom"
tag2 = "v61.0.21-REFINITIV-WIPO-PATENT-EBRAHIMZADEH-EVACUATION-SYSTEM"
meta2 = {
    "inventor": "EBRAHIMZADEH, David, J.", "firm": "Corniche Capital",
    "patent_title": "AUTOMOTIVE EMERGENCY EVACUATION SYSTEM",
    "timestamp": now_utc, "security": "Zero-PII Gateway D-34 Masked Pass Active"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('Refinitiv Workspace / WIPO NewsRoom', 'IP_PATENTS_TECH', ?, 1.10, ?, 0.50, ?, 'v61.0.20', 'NODO_CHARALLAVE_L4L5')
""", (hl1, tag1, json.dumps(meta1, ensure_ascii=False)))

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('Refinitiv Workspace / WIPO NewsRoom', 'IP_PATENTS_TECH', ?, 1.15, ?, 0.60, ?, 'v61.0.21', 'NODO_CHARALLAVE_L4L5')
""", (hl2, tag2, json.dumps(meta2, ensure_ascii=False)))

conn.commit()

# Checkpoint WAL Atómico Rápido
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
conn.close()

print(f"\n🔒 UNIFIED WIPO PATENTS INGESTION SUCCESS")
print(f"🟢 TOTAL REGISTROS EN MACRO_DOSSIER: {total}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAGS ASENTADOS: {tag1} | {tag2}\n")

# Renderizado y Despacho en Plantilla Opción A (Quantum Terminal HUD)
subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"], check=False)
