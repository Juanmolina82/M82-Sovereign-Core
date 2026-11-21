#!/usr/bin/env python3
import sqlite3, json, os, hashlib, subprocess, sys
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
BOT_SCRIPT = os.path.join(BASE_DIR, "m82_telegram_bot.py")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Habilitar Write-Ahead Logging para alto rendimiento concurrente
    c.execute("PRAGMA journal_mode=WAL;")
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

def ingest_event(source, category, headline, risk_score, sentiment, entities, m82_tag, desk="CARACAS_HQ_TRANSITION"):
    init_db()
    h = hashlib.sha256(headline.encode()).hexdigest()[:16]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta = {"hash": h, "desk": desk, "latency_ms": 95}

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # De-duplicación estricta por hash
    c.execute("SELECT id FROM macro_dosier WHERE metadata_json LIKE ?", (f'%"{h}"%',))
    if c.fetchone():
        print(f"ℹ️ Evento duplicado en Core M82 (Hash: {h}). Omitiendo inserción.")
        conn.close()
        return False

    c.execute('''
        INSERT INTO macro_dosier 
        (timestamp, source, category, headline, risk_score, metadata_json, m82_tag, sentiment, entities) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ts, source, category, headline, risk_score, json.dumps(meta), m82_tag, sentiment, entities))
    
    conn.commit()
    conn.close()
    print(f"✅ Registro [{m82_tag}] (Risk Score: {risk_score}) guardado en SQLite.")

    # Disparar renderizado y Telegram solo para alto riesgo (Risk Score >= 8.0)
    if risk_score >= 8.0 and os.path.exists(BOT_SCRIPT):
        print("⚡ Score alto detectado. Ejecutando motor de tarjeta e integración Telegram...")
        subprocess.run([sys.executable, BOT_SCRIPT])
    
    return True

if __name__ == "__main__":
    print("Módulo core_ingestor.py listo para operación autónoma en Charallave.")
