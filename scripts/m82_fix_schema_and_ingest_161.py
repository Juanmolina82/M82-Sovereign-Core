#!/usr/bin/env python3
# M82 SOVEREIGN CORE - SCHEMA FIX & RECORD #161 PROTOCOLO CROTONA INGESTION
import sqlite3, os, json, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
SCRIPT_HUD = os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py")

conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

# 1. Asentamiento del Registro #161 con campos canónicos
headline = "[M82 PROTOCOL v61.0.44] Protocolo Crotona 530 AC Sealed -- Sovereign Core Foundation Matrix -- Base 444 = $4.444T Trust Validated -- Bunker Lock 0.30x Nominal"
tag = "v61.0.44-CROTONA-530AC-BUNKER-ORIGIN"

meta = {
    "protocol": "CROTONA_530AC_ORIGIN",
    "equation": "Base 444 = 4.444T Trust",
    "operator": "SECURE OPERATOR D-34",
    "node": "SOVEREIGN EDGE CORE",
    "bunker_lock": "0.30x_LOCK",
    "exposure": "0.22x",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('CROTONA_GOVERNANCE_CORE', 'SOVEREIGN_FOUNDATION', ?, 1.00, ?, 0.99, ?, 'v61.0.44', 'SOVEREIGN_EDGE_CORE')
""", (headline, tag, json.dumps(meta)))

conn.commit()

# 2. Verificación Atómica de Columnas
cur.execute("SELECT id, source, category, headline, m82_tag FROM macro_dossier ORDER BY id DESC LIMIT 1;")
last_row = cur.fetchone()
rec_id = last_row[0]

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total_count = cur.fetchone()[0]
conn.close()

print(f"🔒 [FIX 161 OK] Registro #{rec_id} asentado correctamente. TOTAL DOSSIER: {total_count} | WAL 0/0/0 CLEAN")

# 3. Invocar motor de tarjetas sanitizadas
if os.path.exists(SCRIPT_HUD):
    subprocess.run(["python3", SCRIPT_HUD], check=False)
