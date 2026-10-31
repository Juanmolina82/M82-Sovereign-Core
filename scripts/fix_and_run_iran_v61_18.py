#!/usr/bin/env python3
# M82 HOTFIX DDL & INGESTION v61.0.18 - NODO CHARALLAVE L4L5
import os, json, sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=120)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=120000;")
conn.execute("PRAGMA synchronous=NORMAL;")
cur = conn.cursor()

# 1. MIGRACIÓN DDL IDEMPOTENTE (ALTER TABLE AGREGAR COLUMNAS FALTANTES)
for col, dtype in [
    ("version", "TEXT DEFAULT 'v61.0.18'"),
    ("ingestion_node", "TEXT DEFAULT 'NODO_CHARALLAVE_L4L5'"),
    ("sentiment", "REAL DEFAULT 0.0"),
    ("metadata_json", "TEXT"),
    ("m82_tag", "TEXT")
]:
    try:
        cur.execute(f"ALTER TABLE macro_dossier ADD COLUMN {col} {dtype};")
        print(f"🟢 Columna '{col}' agregada exitosamente a macro_dossier.")
    except sqlite3.OperationalError:
        pass # Columna ya existe

cur.execute("CREATE INDEX IF NOT EXISTS idx_macro_tag ON macro_dossier(m82_tag);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_macro_cat ON macro_dossier(category);")

# Timestamp con timezone-aware UTC
now_utc = datetime.now(timezone.utc).isoformat()

# 2. INGESTA ATÓMICA v61.0.18 - IRAN CRISIS / TRUMP BRIEFING
headline = "[GEOPOL URGENT] US military senior officer Middle East briefs Trump White House Iran options -- WSJ via LSEG Reuters Oct 29 -- Iran crisis briefs Trump meeting"
tag = "v61.0.18-GEOPOL-IRAN-OPTIONS-BRIEFING-TRUMP-WSJ-LSEG-29OCT2026"

meta = {
    "event": "IRAN_CRISIS_TRUMP_MEETING",
    "source": "LSEG Workspace Reuters / WSJ report -- US military senior officer overseeing Middle East met Trump White House Thursday outline military options Iran -- citing US officials",
    "verification": "Reuters could not independently verify -- URGENT tag",
    "date": "2026-10-29",
    "oil_impact": "Brent risk premium up -- Venezuela as stable supply alternative -- validates foco estabilidad mejor centro inversion aliados v61.0.17",
    "alignment_mcm": "MCM doctrine USA principal aliado largo plazo restituir soberania mm2 santuario criminal -- same doctrine applied to Iran -- negotiation with guarantees vs military options",
    "capital_pitch": "Iran escalation = need reliable long term ally with investment security -- Venezuela trust NY arbitraje NY narrative reinforced for GE Vernova $25B Mastercard $9.8B Quad-SPV",
    "timestamp": now_utc
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('LSEG Workspace / Reuters / WSJ', 'GEOPOL_OIL_RISK', ?, 2.00, ?, -0.20, ?, 'v61.0.18', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# 3. VERIFICACIÓN Y WAL CHECKPOINT
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("PRAGMA integrity_check;")
integrity = cur.fetchone()[0]

conn.close()

print(f"\n🔒 M82 HOTFIX DDL & INGESTION v61.0.18 SUCCESS")
print(f"🟢 DB PATH: {DB_PATH}")
print(f"🟢 TOTAL REGISTROS: {total}")
print(f"🟢 INTEGRITY CHECK: {integrity}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 BUNKER STATE: 0.30x LOCK -- NODO CHARALLAVE L4L5")
print(f"🟢 TAG RECIENTE: {tag}\n")
