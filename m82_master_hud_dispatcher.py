#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, re
from PIL import Image, ImageDraw, ImageFont

HOME_DIR = os.path.expanduser("~")
M82_DIR = os.path.join(HOME_DIR, "M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
CARDS_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")
if not os.path.exists(CARDS_DIR):
    CARDS_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")
os.makedirs(CARDS_DIR, exist_ok=True)

TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

def dispatch_loop():
    print("🚀 Despachador M82 Anti-Duplicados Iniciado...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=60.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=60000;")
            cur = conn.cursor()

            # SOLO buscar registros con status estrictamente en 'PENDING'
            cur.execute("""
                SELECT id, daemon_source, headline, asset_impact 
                FROM m82_multi_stream 
                WHERE status = 'PENDING'
                ORDER BY id ASC LIMIT 1
            """)
            row = cur.fetchone()

            if row:
                evt_id, source, headline, impact = row
                
                # MARCAR DE INMEDIATO COMO PROCESANDO/DISPATCHED PARA EVITAR REPETICION
                cur.execute("UPDATE m82_multi_stream SET status = 'DISPATCHED' WHERE id = ?", (evt_id,))
                conn.commit()
                print(f"✅ ID #{evt_id} procesado y bloqueado contra repetición.")

            conn.close()
        except Exception as e:
            print(f"[!] Dispatch Error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    dispatch_loop()
