#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // M82_WIRE CENTRAL BANKS INGESTION (LOCK-FREE)
================================================================================
"""

import os
import sqlite3
import json
import time
import subprocess

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
NTFY_SCRIPT = os.path.expanduser("~/M82/m82_send_ntfy_alert.py")

CABLES = [
    {
        "category": "MACRO_DESK",
        "source": "RTRS",
        "headline": "BOJ debated need for more rate hikes at September meeting, summary shows",
        "risk_score": 8.8,
        "metadata": {"central_bank": "BOJ", "policy_bias": "HAWKISH"}
    },
    {
        "category": "MACRO_DESK",
        "source": "RTRS",
        "headline": "Fed seen on pause in October after inflation data",
        "risk_score": 8.5,
        "metadata": {"central_bank": "FED", "policy_bias": "DOVISH_PAUSE"}
    },
    {
        "category": "MACRO_DESK",
        "source": "RTRS",
        "headline": "US inflation does below expectations in August, gives the Fed breathing space",
        "risk_score": 8.2,
        "metadata": {"indicator": "CPI_US", "status": "COOLER"}
    }
]

def run_ingestion():
    # Establecemos un timeout de 30s para esperar si la BD está ocupada
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    c = conn.cursor()
    
    # Activar Journal Mode WAL para prevenir bloqueos futuros
    try:
        c.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass

    count = 0
    for item in CABLES:
        c.execute("""
            INSERT INTO macro_dosier (source, category, headline, risk_score, metadata_json)
            VALUES (?, ?, ?, ?, ?)
        """, (
            item["source"],
            item["category"],
            item["headline"],
            item["risk_score"],
            json.dumps(item["metadata"])
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"  ✓ {count} Entradas de Bancos Centrales registradas exitosamente en macro_dosier.")

    # Invocación de alerta
    if os.path.exists(NTFY_SCRIPT):
        print(" 🚀 Disparando actualización de alerta...")
        subprocess.run(["python3", NTFY_SCRIPT], check=False)

if __name__ == "__main__":
    print("================================================================================")
    print(" 🚀 INGESTANDO METRICAS M82_WIRE CENTRAL BANKS EN NODO CHARALLAVE")
    print("================================================================================")
    run_ingestion()
    print("================================================================================")
