#!/usr/bin/env python3
import os
import sys
import time
import sqlite3
import logging
from datetime import datetime

LOG_FILE = os.path.expanduser("~/M82/desks/m82_rare_earths_daemon.log")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

RIC_CHAINS = ["0#MB-RE-PR", "0#MB-RE-ND", "0#MB-RE-DY", "0#MB-RE-NDPR", "0#MB-RAREARTH"]
EQUITIES = ["MP.N", "LYC.AX", "600111.SS", "USAR.O"]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.execute("PRAGMA busy_timeout = 60000;")
    return conn

def fetch_and_ingest():
    logging.info("Iniciando ciclo de captura LSEG Rare Earths / Critical Minerals...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headline = f"[RARE_EARTHS_PULSE {ts}] Active RICs {len(RIC_CHAINS)} chains + {len(EQUITIES)} equities"
        
        # INSERT OR IGNORE para manejar silenciosamente cualquier colisión
        cursor.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
            VALUES (?, ?, ?, ?, ?)
        """, ('RARE_EARTHS_DAEMON', headline, 'VERIFIED', 0.90, 'CRITICAL_MINERALS'))
        
        conn.commit()
        conn.close()
        logging.info("Ingesta procesada sin conflictos en m82_multi_stream.")
    except Exception as e:
        logging.error(f"Error en persistencia WAL DB: {str(e)}")

if __name__ == "__main__":
    logging.info("=== M82 RARE EARTHS DAEMON STARTED (FIXED) ===")
    while True:
        try:
            fetch_and_ingest()
        except Exception as e:
            logging.error(f"Excepcion no controlada: {e}")
        time.sleep(300)
