#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // TRUMP-XI PRISONERS DIPLOMACY INGESTION
================================================================================
"""

import os
import sqlite3
import json
import subprocess

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
NTFY_SCRIPT = os.path.expanduser("~/M82/m82_send_ntfy_alert.py")

CABLE = {
    "category": "GEOPOLITICS",
    "source": "REUTERS_M82_MACRO",
    "headline": "Trump says he discussed release of political prisoners (Jimmy Lai, Min Zin) with Xi Jinping",
    "risk_score": 8.9,
    "metadata": {
        "actors": ["Donald Trump", "Xi Jinping"],
        "cases": ["Jimmy Lai", "Min Zin"],
        "topics": ["Political Prisoners", "US-China Diplomacy"]
    }
}

def run_ingestion():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    c = conn.cursor()
    
    try:
        c.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass

    c.execute("""
        INSERT INTO macro_dosier (source, category, headline, risk_score, metadata_json)
        VALUES (?, ?, ?, ?, ?)
    """, (
        CABLE["source"],
        CABLE["category"],
        CABLE["headline"],
        CABLE["risk_score"],
        json.dumps(CABLE["metadata"])
    ))
    
    conn.commit()
    conn.close()
    print(f"  ✓ Cable geopolítico registrado en macro_dosier (Risk Score: {CABLE['risk_score']}).")

    if os.path.exists(NTFY_SCRIPT):
        print(" 🚀 Disparando dispatcher de alertas...")
        subprocess.run(["python3", NTFY_SCRIPT], check=False)

if __name__ == "__main__":
    print("================================================================================")
    print(" 🚀 INGESTANDO CABLE M82_WIRE TRUMP-XI EN NODO CHARALLAVE")
    print("================================================================================")
    run_ingestion()
    print("================================================================================")
