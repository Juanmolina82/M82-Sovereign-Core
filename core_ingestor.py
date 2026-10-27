#!/usr/bin/env python3
import os, sys, sqlite3, json

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signal_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            category TEXT,
            asset_class TEXT,
            risk_score REAL,
            headline TEXT UNIQUE,
            payload_json TEXT,
            status TEXT DEFAULT 'PROCESSED',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def ingest_signal(source, category, asset_class, risk_score, headline, payload_dict):
    init_db()
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO signal_events (source, category, asset_class, risk_score, headline, payload_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (source, category, asset_class, risk_score, headline, json.dumps(payload_dict)))
        conn.commit()
        print(f"✅ [INGEST SUCCESS] Evento guardado: {headline[:60]}... (Risk: {risk_score})")
        conn.close()
    except sqlite3.IntegrityError:
        print(f"⚠️ [INGEST SKIP] Duplicado detectado: {headline[:40]}...")
    except Exception as e:
        print(f"❌ [INGEST ERROR] {e}")

if __name__ == "__main__":
    init_db()
    print("Core Ingestor M82 operacional.")
