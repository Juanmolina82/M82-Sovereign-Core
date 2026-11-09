#!/usr/bin/env python3
"""
================================================================================
 M82 CRON DISPATCHER // VENEZUELA_DESK AUTO-CARD & TELEGRAM PUSH
================================================================================
"""
import os
import sqlite3
import requests
import subprocess
from m82_hud_card_generator_daemon import generate_stream_card

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARD_PATH = os.path.join(BASE_DIR, "m82_breaking_stream_card.png")

# Configuración Telegram (Reemplazar con credenciales reales si aplica)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def check_and_dispatch():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Buscar el último evento no procesado o con risk_score >= 9.5
    c.execute("""
        SELECT id, headline, category, risk_score 
        FROM macro_dosier 
        WHERE risk_score >= 9.5 
        ORDER BY id DESC LIMIT 1
    """)
    row = c.fetchone()
    conn.close()

    if row:
        event_id, headline, category, risk = row
        print(f"[CRON] Breaking Event Detectado ID {event_id}: [{category}] {headline}")
        
        # Generar Tarjeta HUD Headless en PNG
        generate_stream_card(headline, f"#M82 {category}")
        
        # Envío a Telegram si las credenciales están presentes
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            caption = f"🚨 *#M82 BREAKING STREAM*\n\n📌 *{category}*\n{headline}\n\n[AGI QUANTUM VERIFIED]"
            with open(CARD_PATH, 'rb') as photo:
                requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'photo': photo})
            print("  ✓ Tarjeta y alerta despachadas exitosamente a Telegram.")
        else:
            print("  ✓ Tarjeta renderizada en ~/M82/m82_breaking_stream_card.png (Modo Local/PWA).")

if __name__ == "__main__":
    check_and_dispatch()
