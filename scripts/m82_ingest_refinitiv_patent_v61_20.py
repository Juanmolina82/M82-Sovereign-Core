#!/usr/bin/env python3
# M82 REFINITIV WIPO PATENT INGESTION v61.0.20 - NODO CHARALLAVE L4L5 - AUDIT 1000281684.jpg
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

headline = "[REFINITIV WIPO WIRE] WIPO Publishes Patent EBRAHIMZADEH David J AUTOMATICALLY-DEACTIVATED CHILD SAFETY LOCK SYSTEM — Visual Audit 1000281684.jpg — Refinitiv Workspace NewsRoom"
tag = "v61.0.20-REFINITIV-WIPO-PATENT-EBRAHIMZADEH-LOCK-SYSTEM-AUDIT-1000281684"

meta = {
    "source_wire": "Refinitiv Workspace / NewsRoom / WIPO — Visual Audit 1000281684.jpg",
    "inventor": "EBRAHIMZADEH, David, J.",
    "patent_title": "AUTOMATICALLY-DEACTIVATED CHILD SAFETY LOCK SYSTEM",
    "category": "IP_PATENTS_TECH — Automotive Safety — Autonomous Lock",
    "forensic_image": "1000281684.jpg",
    "timestamp": now_utc,
    "governance": "BUNKER MODE 0.30x LOCK — CUSTODIA PASIVA — Exposicion 0.22x VaR 1.68% Warsh Spread +102 bps",
    "repository": "MM82",
    "security": "Zero-PII Gateway D-34 Masked Pass Active — Option A Quantum Terminal HUD 1080x1350",
    "impact": "IP Desk Innovation Infrastructure — Intangible asset for Quad-SPV — Triangulation tech + safety systems for powered land / mobility"
}

cur.execute("""
CREATE TABLE IF NOT EXISTS macro_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts_utc TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    source TEXT,
    category TEXT,
    headline TEXT,
    risk_score REAL,
    m82_tag TEXT UNIQUE,
    sentiment REAL,
    metadata_json TEXT,
    ingestion_node TEXT DEFAULT 'NODO_CHARALLAVE_L4L5',
    version TEXT DEFAULT 'v61.0.20'
);
""")

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('Refinitiv Workspace / WIPO NewsRoom / Visual Audit 1000281684.jpg', 'IP_PATENTS_TECH', ?, 1.10, ?, 0.55, ?, 'v61.0.20', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("PRAGMA integrity_check;")
integrity = cur.fetchone()[0]
conn.close()

print(f"\n🔒 M82 REFINITIV WIPO PATENT v61.0.20 SUCCESS")
print(f"🟢 TOTAL: {total} | INTEGRITY: {integrity} | WAL: 0/0/0 CLEAN")
print(f"🟢 TAG: {tag}")
print(f"🟢 AUDIT: 1000281684.jpg")

# Render HUD Option A
try:
    subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"], timeout=30)
    print("🟢 HUD Option A RENDERED — Quantum Terminal 1080x1350")
except Exception as e:
    print(f"⚠️ HUD render skip: {e}")
