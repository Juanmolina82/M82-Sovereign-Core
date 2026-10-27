#!/usr/bin/env python3
import sqlite3
import json
import os
import hashlib
import subprocess
import sys
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
BOT_SCRIPT = os.path.join(BASE_DIR, "m82_telegram_bot.py")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=5000;")
    c.execute('''
        CREATE TABLE IF NOT EXISTS macro_dosier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            headline TEXT NOT NULL,
            risk_score REAL NOT NULL,
            metadata_json TEXT,
            m82_tag TEXT NOT NULL,
            sentiment REAL,
            entities TEXT
        )
    ''')
    conn.commit()
    conn.close()

def publish_energy_infrastructure_dossier():
    init_db()
    
    headline = "BRENT $98 VS VLCC BULLISH: DESCONEXION POR BYPASS ORMUZ 75% Y STS 10.5M BPD"
    source = "EULER/TASS_INTELLIGENCE"
    category = "ENERGY_INFRASTRUCTURE"
    risk_score = 8.8
    sentiment = -0.15
    m82_tag = "ENERGY_MACRO"
    entities = "ORMUZ,SUMED,ADCOP,FUJAIRAH,SIDI_KERIR,VLCC,BRENT"
    desk = "CHARALLAVE_HQ_TRANSITION"

    h = hashlib.sha256(headline.encode()).hexdigest()[:16]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "hash": h,
        "desk": desk,
        "key_capacity_index": "10.6M bpd (75% pre-war)",
        "bypass_routes": {
            "fujairah_uae": "3.7M MT",
            "sumed_egypt": "1.0M MT",
            "yanbu_saudi": "0.3M MT"
        },
        "sts_operations": {
            "total_bpd": "10.5M",
            "uae_offshore": "7.6M bpd",
            "oman_offshore": "2.9M bpd"
        },
        "price_scenarios": {
            "p_100_percent": "$85-$90",
            "p_75_percent_current": "$95-$102",
            "p_under_50_percent": "$120+"
        },
        "trade_positioning": {
            "commodity_crude": "Range sell / defensivo ($90-$105)",
            "freight_tankers": "Bullish VLCCs / Suezmax (STS Friccion)"
        }
    }

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=5000;")
    
    c.execute("SELECT id FROM macro_dosier WHERE metadata_json LIKE ?", (f'%"{h}"%',))
    if c.fetchone():
        print(f"ℹ️ Evento duplicado en Core M82 (Hash: {h}). Omitiendo inserción.")
        conn.close()
        return

    c.execute('''
        INSERT INTO macro_dosier 
        (timestamp, source, category, headline, risk_score, metadata_json, m82_tag, sentiment, entities) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ts, source, category, headline, risk_score, json.dumps(payload), m82_tag, sentiment, entities))
    
    conn.commit()
    conn.close()
    print(f"✅ Dossier [{m82_tag}] (Risk Score: {risk_score}) guardado exitosamente en SQLite (WAL).")

    if risk_score >= 8.0 and os.path.exists(BOT_SCRIPT):
        print("⚡ Risk Score 8.8 >= 8.0. Ejecutando motor de tarjeta e integración Telegram...")
        subprocess.run([sys.executable, BOT_SCRIPT])

if __name__ == "__main__":
    publish_energy_infrastructure_dossier()
