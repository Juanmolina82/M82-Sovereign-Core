#!/usr/bin/env python3
import os, json, sqlite3
from datetime import datetime
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH, timeout=120)
conn.execute("PRAGMA journal_mode=WAL;")
cur = conn.cursor()

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
    version TEXT DEFAULT 'v61.0.18'
);
""")

now = datetime.utcnow().isoformat()+"Z"
headline = "[GEOPOL URGENT] US military senior officer Middle East briefs Trump White House Iran options — WSJ via LSEG Reuters Oct 29 — Iran crisis Trump meeting"
tag = "v61.0.18-GEOPOL-IRAN-OPTIONS-BRIEFING-TRUMP-WSJ-LSEG-29OCT2026"

meta = {
 "event": "IRAN_CRISIS_TRUMP_MEETING",
 "source": "LSEG Workspace Reuters — WSJ report — US military senior officer overseeing Middle East met Trump White House Thursday outline military options Iran — citing US officials",
 "verification": "Reuters could not independently verify — URGENT tag",
 "date": "2026-10-29",
 "id": "urn:newsml:newswire.refinitiv.com:20261029:nF4N46F3AD:1",
 "oil_impact": "Brent risk premium up — Venezuela as stable supply alternative — validates foco estabilidad mejor centro inversion aliados v61.0.17",
 "alignment_mcm": "MCM doctrine USA principal aliado largo plazo restituir soberania mm2 santuario criminal — same doctrine applied to Iran — negotiation with guarantees vs military options",
 "capital_pitch": "Iran escalation = need reliable long term ally with investment security — Venezuela trust NY arbitraje NY narrative reinforcement for GE Vernova $25B Mastercard $9.8B Quad-SPV",
 "timestamp": now
}

cur.execute("INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version) VALUES ('LSEG Workspace / Reuters / WSJ — IRAN-CRISIS/TRUMP-MEETING URGENT / Charallave L4L5', 'GEOPOL_OIL_RISK', ?, 0.90, ?, -0.20, ?, 'v61.0.18')", (headline, tag, json.dumps(meta)))

conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
print(f"IRAN BRIEFING SELLADO — TOTAL {cur.fetchone()[0]} — {tag}")
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()
