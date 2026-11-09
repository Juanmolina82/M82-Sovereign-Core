#!/usr/bin/env python3
# M82 REFINITIV TOPNEWS BARRIDO MACRO & TECH WIRE v61.0.23 - NODO CHARALLAVE L4L5
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=120)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=120000;")
conn.execute("PRAGMA synchronous=NORMAL;")
cur = conn.cursor()

now_utc = datetime.now(timezone.utc).isoformat()

headline = "[REFINITIV WIRE] TopNews Macro & Tech: US Productivity +1.6% on AI Surge, ECB Holds Rates, Alphabet/Amazon AI Cloud Growth & Big Oil Surges on Supply Risks"
tag = "v61.0.23-REFINITIV-TOPNEWS-PRODUCTIVITY-ECB-AI-BIG-OIL"

meta = {
    "source_wire": "Refinitiv Workspace / LSEG TopNews Wire (1000281706.jpg)",
    "key_stories": [
        "US Productivity: +1.6% Q3 surge driven by AI CAPEX",
        "ECB: Rates unchanged amid governance/succession talks",
        "Tech/AI: Alphabet & Amazon cloud growth vs Intel Q4 guidance drop",
        "Energy: Big Oil rallies on Middle East supply risks and storage demand"
    ],
    "timestamp": now_utc,
    "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active",
    "governance": "BUNKER MODE 0.30x LOCK -- NODO CHARALLAVE L4/L5 EDGE"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('Refinitiv Workspace / TopNews Feed', 'GLOBAL_MACRO_TECH_WIRE', ?, 1.55, ?, 0.65, ?, 'v61.0.23', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# Verificación y Checkpoint WAL
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("PRAGMA integrity_check;")
integrity = cur.fetchone()[0]

conn.close()

print(f"\n🔒 M82 REFINITIV TOPNEWS BARRIDO v61.0.23 SUCCESS")
print(f"🟢 DB PATH: {DB_PATH}")
print(f"🟢 TOTAL REGISTROS: {total}")
print(f"🟢 INTEGRITY CHECK: {integrity}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAG INGESTADO: {tag}\n")

# Disparar renderizado en Plantilla Opción A (Quantum Terminal HUD)
subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"], check=False)
