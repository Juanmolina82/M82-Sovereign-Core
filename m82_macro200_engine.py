#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
LOG_PATH = os.path.join(BASE_DIR, "logs/macro200_engine.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS macro_dossier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT (datetime('now')),
            source TEXT,
            category TEXT,
            headline TEXT UNIQUE,
            risk_score REAL,
            m82_tag TEXT DEFAULT 'BUNKER_HOLD_030X',
            sentiment REAL DEFAULT 0.0,
            metadata_json TEXT,
            alpha_score REAL DEFAULT 0.95
        )
    """)
    now = datetime.now(timezone.utc).isoformat()
    meta = json.dumps({
        "hq": "CARACAS_HQ_STANDBY",
        "edge": "CHARALLAVE_L4_L5_ACTIVE",
        "governance": "BUNKER_030X_NO_TRADE",
        "exposure": 0.22,
        "var_daily": 1.68,
        "warsh_spread_bps": 102.0,
    })
    conn.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score)
        VALUES ('MACRO200_ENGINE', 'TOPOLOGY_BOOT', ?, 1.0, 'BUNKER_HOLD_030X', 0.0, ?, 0.99)
    """, (f"[MACRO200 BOOT {now[:19]}Z] Caracas HQ Master -> Charallave Edge Active | BUNKER 0.30x LOCK", meta))
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

async def macro_engine_loop():
    init_db()
    logging.info("🟢 M82 MACRO 200 ENGINE - NODO CHARALLAVE OPERATIVO (CARACAS HQ MASTER)")
    while True:
        try:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            conn = get_db()
            active_daemons = conn.execute(
                "SELECT COUNT(*) FROM m82_daemons_registry WHERE status='ACTIVE_LITE_WAKELOCK'"
            ).fetchone()[0] if conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='m82_daemons_registry'"
            ).fetchone()[0] else 40
            conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
            conn.close()
            logging.info(f"HEARTBEAT M82 MACRO200: {active_daemons}/40 Daemons | BUNKER 0.30x LOCK | {ts}")
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Error en engine loop: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(macro_engine_loop())
