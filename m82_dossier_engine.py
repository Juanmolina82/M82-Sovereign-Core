#!/usr/bin/env python3
import sqlite3
import os
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [M82_ENGINE] - %(levelname)s - %(message)s')
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

class M82DossierEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=60.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=60000;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _initialize_db(self):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS m82_multi_stream (
                stream_id INTEGER PRIMARY KEY AUTOINCREMENT,
                daemon_source TEXT NOT NULL,
                headline TEXT NOT NULL,
                status TEXT DEFAULT 'RAW',
                alpha_score REAL DEFAULT 0.00,
                sentiment REAL DEFAULT 0.00,
                asset_impact TEXT NOT NULL,
                event_trigger TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS macro_dossier (
                dossier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                headline TEXT NOT NULL,
                risk_score REAL DEFAULT 1.68,
                m82_tag TEXT UNIQUE NOT NULL,
                sentiment REAL DEFAULT 0.0,
                validated INTEGER DEFAULT 1,
                metadata_json TEXT NOT NULL,
                ingested_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()
            conn.close()
            logging.info("Database schema validated successfully.")
        except Exception as e:
            logging.error(f"Error initializing DB: {str(e)}")

    def ingest_event(self, source, category, headline, tag, event_trigger, alpha_score, sentiment, asset_impact, metadata):
        start_time = time.time()
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT OR IGNORE INTO m82_multi_stream 
            (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger)
            VALUES (?, ?, 'VERIFIED', ?, ?, ?, ?);
            """, (f"M82_DAEMON_{source.upper()}", headline, alpha_score, sentiment, asset_impact, event_trigger))
            
            metadata_str = json.dumps(metadata)
            cursor.execute("""
            INSERT OR IGNORE INTO macro_dossier
            (source, category, headline, risk_score, m82_tag, sentiment, validated, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?);
            """, (source, category, headline, metadata.get("var", 1.68), tag, sentiment, metadata_str))
            
            # FIX CLAVE: COMMIT PRIMERO
            conn.commit()
            conn.close()
            conn = None
            
            # Checkpoint en conexión LIMPIA y SEPARADA
            conn2 = self._get_connection()
            cur2 = conn2.cursor()
            cur2.execute("PRAGMA wal_checkpoint(TRUNCATE);")
            checkpoint_res = cur2.fetchone()
            conn2.close()
            
            elapsed_ms = (time.time() - start_time) * 1000
            logging.info(f"Ingestion SEALED | Tag: {tag} | Latency: {elapsed_ms:.2f}ms | WAL Status: {checkpoint_res}")
            return True
        except Exception as e:
            logging.error(f"Ingestion FAILED for tag {tag}: {str(e)}")
            if conn:
                try:
                    conn.rollback()
                    conn.close()
                except: pass
            return False

if __name__ == "__main__":
    engine = M82DossierEngine()
    test_meta = {
        "timestamp": "2026-11-05T01:10:00VET",
        "gold": 3940,
        "silver": 50.58,
        "var": 1.68,
        "warsh_spread_bps": 102.0,
        "status": "BUNKER_MODE_030X_LOCK"
    }
    engine.ingest_event(
        source="SYSTEM_ARCHITECT",
        category="INFRASTRUCTURE_DESIGN",
        headline="Robust M82 Macro Dossier Architecture Operational",
        tag="v61.0.51-A-ROBUST-ARCH-20261105",
        event_trigger="M82_ROBUST_ARCH_CHECKPOINT",
        alpha_score=1.00,
        sentiment=0.99,
        asset_impact="SYSTEM_STABILITY",
        metadata=test_meta
    )
