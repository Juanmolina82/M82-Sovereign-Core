#!/usr/bin/env python3
import sqlite3, json, os, hashlib
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

LATAM_FEED = [
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "DIPLOMATIC_RISK",
        "headline": "US halts consular services in Brazil ahead of election amid rising tensions",
        "risk_score": 9.6,
        "sentiment": -0.75,
        "entities": "[\"US_STATE_DEPT\", \"BRAZIL\", \"US_BRL\"]",
        "m82_tag": "DIPLOMATIC_TENSIONS"
    },
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "FX_OUTLOOK",
        "headline": "Brazil Real spurt does not reflect a shift in recent bearish macro outlook",
        "risk_score": 8.4,
        "sentiment": -0.40,
        "entities": "[\"USDBRL\", \"BCB\"]",
        "m82_tag": "LATAM_FX"
    },
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "LATAM_TRADE",
        "headline": "Chinese auto show debuts in Argentina as sales surge amid shift in Mercosur trade",
        "risk_score": 8.1,
        "sentiment": 0.20,
        "entities": "[\"CHINA\", \"ARGENTINA\", \"MERCOSUR\"]",
        "m82_tag": "CHINA_LATAM"
    }
]

def process_and_ingest():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    
    ingested_count = 0
    for item in LATAM_FEED:
        headline_hash = hashlib.sha256(item['headline'].encode('utf-8')).hexdigest()[:16]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = {"hash": headline_hash, "desk": "BRAZIL_CONSULAR_M82_MACROURITY", "latency_ms": 115}
        
        try:
            c.execute("""
                INSERT INTO macro_dosier 
                (timestamp, source, category, headline, risk_score, metadata_json, m82_tag, sentiment, entities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, item['source'], item['category'], item['headline'],
                item['risk_score'], json.dumps(metadata), item['m82_tag'],
                item['sentiment'], item['entities']
            ))
            ingested_count += 1
        except Exception:
            pass

    conn.commit()
    conn.close()
    print(f"✅ Ingesta LATAM/Diplomatic finalizada: {ingested_count} titulares agregados.")

if __name__ == "__main__":
    process_and_ingest()
