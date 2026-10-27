#!/usr/bin/env python3
import asyncio, sqlite3, json, os, logging, time
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
LOG_PATH = os.path.join(BASE_DIR, "lite_runner.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=5000;")
    c.execute("""
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
    """)
    conn.commit()
    conn.close()

async def macro_engine_loop():
    init_db()
    logging.info("🟢 M82 MACRO 200 ENGINE - NODO CHARALLAVE OPERATIVO (CARACAS HQ MASTER)")
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"HEARTBEAT M82: Processing active daemons at {timestamp}")
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Error en engine loop: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(macro_engine_loop())
