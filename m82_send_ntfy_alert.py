#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // DYNAMIC ALERT DISPATCHER (NTFY + TELEGRAM)
================================================================================
 Envia el ultimo evento registrado en macro_dosier a ntfy.sh y Telegram
"""

import os
import sqlite3
import requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
NTFY_TOPIC = "MM82"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1004335849125")

def get_latest_event():
    """Consulta el último evento insertado en la base de datos."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute("""
            SELECT category, headline, risk_score, source 
            FROM macro_dosier 
            ORDER BY id DESC LIMIT 1
        """)
        row = c.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"[!] Error leyendo BD: {e}")
        return None

def send_telegram_fallback(title, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"*{title}*\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("  ✓ Alerta entregada con éxito a Telegram.")
            return True
        else:
            print(f"  ❌ Error Telegram: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"  ❌ Fallo en Telegram: {e}")
        return False

def dispatch():
    event = get_latest_event()
    if not event:
        print("[i] No hay registros en macro_dosier para enviar.")
        return

    category, headline, risk_score, source = event
    
    title = f"🚨 #M82 BREAKING [{category}]"
    message = f"📌 {headline}\n\n⚡ Risk Score: {risk_score}/10 | Fuente: {source}"

    print(f"[*] Despachando noticia real: {headline[:50]}...")

    # Intentar ntfy.sh
    headers = {
        "Title": title.encode('utf-8'),
        "Priority": "high",
        "Tags": "zap,bar_chart"
    }
    
    try:
        r = requests.post(NTFY_URL, data=message.encode('utf-8'), headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"  ✓ Alerta enviada a ntfy.sh/{NTFY_TOPIC}")
        elif r.status_code == 429:
            print("  ⚠️ Límite de ntfy.sh (429). Redireccionando a Telegram...")
            send_telegram_fallback(title, message)
        else:
            send_telegram_fallback(title, message)
    except Exception as e:
        print(f"  ❌ Error ntfy.sh ({e}). Redireccionando a Telegram...")
        send_telegram_fallback(title, message)

if __name__ == "__main__":
    dispatch()
