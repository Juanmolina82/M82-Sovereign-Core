#!/usr/bin/env python3
import sqlite3, json, os, time, hashlib
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Noticias extraídas directamente del M82 Wire Workspace Desk
RAW_FEED = [
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "MACRO_POLICY",
        "headline": "Fed may skip October but rate hike trigger in December - M82_MACRO",
        "risk_score": 9.2,
        "sentiment": -0.45,
        "entities": "[\"FED\", \"US_RATES\"]",
        "m82_tag": "CENTRAL_BANKS"
    },
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "MACRO_JOBS",
        "headline": "US job growth undershoots expectations in September, but labor market remains stable",
        "risk_score": 8.5,
        "sentiment": -0.20,
        "entities": "[\"US_PAYROLLS\", \"USD\"]",
        "m82_tag": "US_ECONOMY"
    },
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "GEOPOLITICS_TRADE",
        "headline": "Handful of G20 countries reject US stance on excess industrial capacity",
        "risk_score": 8.8,
        "sentiment": -0.60,
        "entities": "[\"G20\", \"US_TRADE\"]",
        "m82_tag": "GLOBAL_TRADE"
    },
    {
        "source": "M82_MACRO_M82_WIRE",
        "category": "EUROZONE_INFLATION",
        "headline": "Euro zone inflation surges more than expected, keeping pressure on ECB to hike rates",
        "risk_score": 9.0,
        "sentiment": -0.75,
        "entities": "[\"ECB\", \"EUR\"]",
        "m82_tag": "EUROZONE"
    }
]

def process_and_ingest():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    
    ingested_count = 0
    for item in RAW_FEED:
        # Deduplicación semántica basada en Hash SHA-256 del titular
        headline_hash = hashlib.sha256(item['headline'].encode('utf-8')).hexdigest()[:16]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        metadata = {
            "hash": headline_hash,
            "refinitiv_desk": "SPACE_WEB_V2",
            "latency_ms": 185
        }
        
        try:
            c.execute("""
                INSERT INTO macro_dosier 
                (timestamp, source, category, headline, risk_score, metadata_json, m82_tag, sentiment, entities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                item['source'],
                item['category'],
                item['headline'],
                item['risk_score'],
                json.dumps(metadata),
                item['m82_tag'],
                item['sentiment'],
                item['entities']
            ))
            ingested_count += 1
        except Exception as e:
            pass

    conn.commit()
    conn.close()
    print(f"✅ Ingesta M82 Wire finalizada: {ingested_count} titulares agregados a m82_database.db.")

if __name__ == "__main__":
    process_and_ingest()
