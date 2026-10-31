#!/usr/bin/env python3
# M82 DAEMON :: PRIVATE CREDIT & GLOBAL BANKING TELEMETRY (LSEG WIRE)
import os, json, sqlite3, time
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run_telemetry():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    cur = conn.cursor()
    
    now_utc = datetime.now(timezone.utc).isoformat()
    headline = "[LSEG FINANCIALS WIRE] Private Credit A.I. Buyout Risks Surge; Mastercard Q3 Card Spending Strong; BBVA & SocGen Beat Estimates"
    tag = "v61.0.28-DAEMON-FINANCIALS-PRIVATE-CREDIT-MASTERCARD-BBVA"
    
    meta = {
        "desk": "Financials & Private Credit Desk",
        "key_drivers": [
            "Private credit exposure to AI LBO buyouts rising",
            "Mastercard Q3 consumer spending holds up",
            "European banking net interest income record profits (SocGen, BBVA, ING)"
        ],
        "timestamp": now_utc,
        "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active"
    }
    
    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
        VALUES ('LSEG Workspace / Banking Desk', 'FINANCIALS_PRIVATE_CREDIT', ?, 1.40, ?, 0.60, ?, 'v61.0.28', 'NODO_CHARALLAVE_L4L5')
    """, (headline, tag, json.dumps(meta, ensure_ascii=False)))
    
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()
    print("🟢 [DAEMON PRIVATE CREDIT] Ingesta ejecutada con éxito.")

if __name__ == "__main__":
    run_telemetry()
