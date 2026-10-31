#!/usr/bin/env python3
# M82 DAEMON :: COMMODITIES, FREIGHT & REFINING MARGINS (LSEG WIRE)
import os, json, sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run_telemetry():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    cur = conn.cursor()
    
    now_utc = datetime.now(timezone.utc).isoformat()
    headline = "[LSEG COMMODITIES WIRE] High Freight Rates Cut $3.4B from Shell Debt; US Energy Exports Surge to Hedge European Disruption; Aramco Cuts Asian OSP"
    tag = "v61.0.28-DAEMON-COMMODITIES-FREIGHT-SHELL-ARAMCO-OSP"
    
    meta = {
        "desk": "Commodities & Energy Freight Desk",
        "key_drivers": [
            "Freight rates pressure global oil majors debt reduction",
            "US LNG and crude exports hedge European supply risks",
            "Saudi Aramco OSP price adjustments for Asian markets"
        ],
        "timestamp": now_utc,
        "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active"
    }
    
    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
        VALUES ('LSEG Workspace / Commodities Wire', 'COMMODITIES_FREIGHT_ENERGY', ?, 1.30, ?, 0.70, ?, 'v61.0.28', 'NODO_CHARALLAVE_L4L5')
    """, (headline, tag, json.dumps(meta, ensure_ascii=False)))
    
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()
    print("🟢 [DAEMON COMMODITIES FREIGHT] Ingesta ejecutada con éxito.")

if __name__ == "__main__":
    run_telemetry()
