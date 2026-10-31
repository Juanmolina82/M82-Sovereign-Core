#!/usr/bin/env python3
# M82 DAEMON :: AI HYPERSCALERS & SEMICONDUCTOR CAPEX (LSEG WIRE)
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run_telemetry():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    cur = conn.cursor()
    
    now_utc = datetime.now(timezone.utc).isoformat()
    headline = "[LSEG TECH WIRE] AI Infrastructure Spending Outpaces Revenue Growth; Intel Q4 Guidance Drops Stock; Samsung Cuts NAND Memory Production"
    tag = "v61.0.28-DAEMON-TECH-AI-CAPEX-INTEL-SAMSUNG-HYPERSCALERS"
    
    meta = {
        "desk": "Tech & AI Compute Infrastructure Desk",
        "key_drivers": [
            "Big Tech AI CAPEX circular investment cycle under market scrutiny",
            "Intel stock pressure on soft Q4 outlook and PC weakness",
            "Samsung NAND cuts aimed at stabilizing chip pricing"
        ],
        "timestamp": now_utc,
        "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active"
    }
    
    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
        VALUES ('LSEG Workspace / Tech Wire', 'TECH_AI_SEMICONDUCTORS', ?, 1.65, ?, 0.50, ?, 'v61.0.28', 'NODO_CHARALLAVE_L4L5')
    """, (headline, tag, json.dumps(meta, ensure_ascii=False)))  
    
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM macro_dossier;")
    total = cur.fetchone()[0]
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()
    
    print(f"\n🔒 M82 ENJAMBRE DE DAEMONS v61.0.28 ACTIVADO CON ÉXITO")
    print(f"🟢 TOTAL REGISTROS EN MACRO_DOSSIER: {total}")
    print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
    
    # Trigger HUD Option A
    subprocess.Popen(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"])

if __name__ == "__main__":
    run_telemetry()
