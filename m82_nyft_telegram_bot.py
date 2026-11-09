#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // NYFT CONNECTOR & TELEGRAM DISPATCHER BOT
================================================================================
 Integration: M82 Wire (NYFT Feed) + SQLite Database + HUD Card Generator + Telegram Bot
"""

import os
import sys
import json
import sqlite3
import datetime
import requests
import subprocess

# Directorios y Rutas
BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARD_PATH = os.path.join(BASE_DIR, "m82_breaking_stream_card.png")
CARD_SCRIPT = os.path.join(BASE_DIR, "m82_hud_card_generator_daemon.py")

# Credenciales de Telegram (Leídas desde Entorno)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def verify_environment():
    """Verifica que el entorno de base de datos y scripts esté disponible."""
    if not os.path.exists(DB_PATH):
        print(f"[!] Error: Base de datos no encontrada en {DB_PATH}")
        sys.exit(1)
    if not os.path.exists(CARD_SCRIPT):
        print(f"[!] Warning: Script renderizador {CARD_SCRIPT} no localizado.")

def get_latest_high_risk_event(min_risk_score=9.5):
    """Consulta en SQLite el último cable breaking registrado por NYFT con Risk Score alto."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, source, category, headline, risk_score, gprk_index, metadata_json
            FROM macro_dosier
            WHERE risk_score >= ?
            ORDER BY id DESC LIMIT 1
        """, (min_risk_score,))
        row = c.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"[!] Error consultando SQLite: {e}")
        return None

def trigger_hud_card_generation(headline, category):
    """Ejecuta el demonio de tarjetas para renderizar la imagen m82_breaking_stream_card.png."""
    print(f"[*] Generando Tarjeta HUD para: [{category}] {headline[:40]}...")
    try:
        # Importar dinámicamente o ejecutar mediante subprocess
        cmd = ["python3", CARD_SCRIPT]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("  ✓ Tarjeta HUD renderizada exitosamente.")
        return True
    except Exception as e:
        print(f"[!] Error al generar tarjeta HUD: {e}")
        return False

def send_telegram_breaking(category, headline, risk_score, gprk_index):
    """Envía la tarjeta HUD de la imagen junto con el resumen explicativo por Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[i] Telegram Token/Chat_ID no configurados. Omitiendo envío remoto.")
        print(f"  └─> Noticia procesada localmente: [{category}] {headline}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    caption = (
        f"🚨 *#M82 BREAKING STREAM*\n\n"
        f"📌 *DESK:* `{category}`\n"
        f"⚡ *RISK SCORE:* `{risk_score}/10` | *GPRK:* `{gprk_index}`\n\n"
        f"📝 *HEADLINE:*\n_{headline}_\n\n"
        f"🌐 [AGI QUANTUM VERIFIED - NYFT FEED]"
    )

    try:
        with open(CARD_PATH, 'rb') as photo:
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            }
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files, timeout=15)
            
            if response.status_code == 200:
                print("  ✓ Mensaje y tarjeta despachados con éxito a Telegram.")
                return True
            else:
                print(f"[!] Error API Telegram ({response.status_code}): {response.text}")
                return False
    except Exception as e:
        print(f"[!] Excepción enviando a Telegram: {e}")
        return False

def main():
    print("================================================================================")
    print(" 🤖 M82 NYFT BOT & DISPATCHER CORE")
    print("================================================================================")
    verify_environment()
    
    event = get_latest_high_risk_event(min_risk_score=9.5)
    if not event:
        print("[i] No hay eventos recientes con Risk Score >= 9.5.")
        return

    event_id, source, category, headline, risk_score, gprk_index, metadata_json = event
    print(f" [+] Evento Crítico Detectado [ID {event_id}]:")
    print(f"  ├─ Origen: {source}")
    print(f"  ├─ Mesa: {category}")
    print(f"  ├─ Risk Score: {risk_score}")
    print(f"  └─ Titular: {headline}")

    # 1. Generar la imagen visual
    generated = trigger_hud_card_generation(headline, f"#M82 {category}")
    
    # 2. Despachar a Telegram si la tarjeta existe
    if generated and os.path.exists(CARD_PATH):
        send_telegram_breaking(category, headline, risk_score, gprk_index)

    print("================================================================================")

if __name__ == "__main__":
    main()
