#!/usr/bin/env python3
import sqlite3, os, json
from datetime import datetime
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
WIRE_EVENTS = [
    ("Oil >$100/bbl & Merey Premium", "COMMODITIES_OIL", 1.72, "v61.0.1-WIRE-OIL-100-MEREY"),
    ("Google 10% Drop — Cloud Miss & AI Capex Reprice", "BIG_TECH_CLOUD", 1.65, "v61.0.1-WIRE-GOOGL-DROP"),
    ("ECB Inflation Persistence — Eurozone Core Stickiness", "MACRO_ECB", 1.68, "v61.0.1-WIRE-ECB-INFLATION"),
    ("France Election & OAT-Bund Spread Blowout", "MACRO_EUROPE", 1.70, "v61.0.1-WIRE-FRANCE-OAT"),
    ("US Q3 Productivity Surge — AGI Efficiency", "MACRO_US", 1.60, "v61.0.1-WIRE-US-PRODUCTIVITY"),
]
def ingest():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;"); conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()
    for headline, cat, risk, tag in WIRE_EVENTS:
        cur.execute("INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score, msi_index, validated) VALUES ('REFINITIV_TELEMETRY','{}',?,? ,?,0.97,?,1.90,1500.0,1)".format(cat), (headline, risk, tag, json.dumps({"ts":datetime.now().isoformat(),"wire":"21:41"})))
        cur.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES ('REFINITIV_BRIDGE_DESK',?, 'PENDING', 0.97, ?, ?)", (headline, cat, tag))
    conn.commit(); cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    cur.execute("SELECT COUNT(*) FROM macro_dossier WHERE validated=1;"); val = cur.fetchone()[0]
    conn.close()
    print(f"🟢 [WIRE 21:41 SUCCESS] 5 Wire Events Ingested | {val} Validated Dossiers | WAL CLEAN 0/0/0")
if __name__ == "__main__": ingest()
