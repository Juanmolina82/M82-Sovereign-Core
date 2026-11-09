#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // UNIFIED HUD CARD & ALERT DISPATCHER
================================================================================
 Integration: DB Ingestion -> HUD Card Generator -> Multi-Channel Alert (ntfy/Telegram)
"""

import os
import sqlite3
import json
import requests
import subprocess

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARD_SCRIPT = os.path.join(BASE_DIR, "m82_hud_card_generator_daemon.py")
CARD_IMG = os.path.join(BASE_DIR, "m82_breaking_stream_card.png")

NTFY_TOPIC = "MM82"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1004335849125")

def render_hud_card():
    """Llama al daemon generador de tarjetas HUD para actualizar la imagen PNG."""
    print("[*] Generando tarjeta cibernética M82 BREAKING STREAM...")
    try:
        res = subprocess.run(["python3", CARD_SCRIPT], capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            print("  ✓ Tarjeta HUD renderizada exitosamente.")
            return True
        else:
            print(f"  ❌ Error en generador HUD: {res.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Fallo al ejecutar daemon HUD: {e}")
        return False

def dispatch_telegram_photo(title, caption):
    """Envía la imagen de la tarjeta HUD generada con pie de texto a Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    if os.path.exists(CARD_IMG):
        with open(CARD_IMG, 'rb') as photo:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": f"*{title}*\n\n{caption}",
                "parse_mode": "Markdown"
            }
            files = {"photo": photo}
            try:
                r = requests.post(url, data=payload, files=files, timeout=15)
                if r.status_code == 200:
                    print("  ✓ Tarjeta HUD + Alerta despachada con éxito a Telegram.")
                    return
            except Exception as e:
                print(f"  ❌ Error enviando foto a Telegram: {e}")

    # Fallback a texto si no hay imagen
    text_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"*{title}*\n\n{caption}",
        "parse_mode": "Markdown"
    }
    requests.post(text_url, json=payload, timeout=10)

def dispatch():
    render_hud_card()

    # Obtener el último evento registrado
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT headline, category, risk_score, gprk_index FROM macro_dosier ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
    except Exception as e:
        print(f"[!] Error leyendo BD: {e}")
        return

    if not row:
        print("[i] No hay registros en macro_dosier.")
        return

    headline, category, risk_score, gprk_index = row
    title = f"🚨 #M82 BREAKING STREAM [{category}]"
    message = (
        f"📌 *{headline}*\n\n"
        f"⚡ *Risk Score:* {risk_score}/10 | *GPRK Index:* {gprk_index}\n"
        f"🌐 *Node:* Caracas | *Status:* AGI QUANTUM VERIFIED\n"
        f"🖼️ *HUD Card:* http://127.0.0.1:8080/m82_breaking_stream_card.png"
    )

    print(f"[*] Despachando notificación a ntfy.sh/{NTFY_TOPIC} y Telegram...")
    
    headers = {
        "Title": title.encode('utf-8'),
        "Priority": "high",
        "Tags": "zap,chart_with_upwards_trend,robot"
    }

    try:
        r = requests.post(NTFY_URL, data=message.encode('utf-8'), headers=headers, timeout=10)
        if r.status_code == 200:
            print("  ✓ Alerta push entregada a ntfy.sh")
        else:
            print(f"  ⚠️ Response ntfy ({r.status_code}). Conmutando a Telegram con tarjeta PNG...")
            dispatch_telegram_photo(title, message)
    except Exception as e:
        print(f"  ❌ Error ntfy ({e}). Redirigiendo a Telegram...")
        dispatch_telegram_photo(title, message)

if __name__ == "__main__":
    dispatch()
