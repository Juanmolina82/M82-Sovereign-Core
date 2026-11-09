#!/usr/bin/env python3
import os
import sqlite3
import requests
import json
import time

# Configuración de Canales (Reemplaza con tus llaves/canales si difieren)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "TU_TELEGRAM_CHAT_ID")
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "m82_alerts") # Tema público/privado de ntfy.sh

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_vlcc_vs_crude_chart.png")

def send_ntfy(message, title="🚨 M82 MACRO ALERT", image_path=None):
    try:
        url = f"https://ntfy.sh/{NTFY_TOPIC}"
        headers = {"Title": title, "Priority": "high", "Tags": "chart_with_upwards_trend,warning"}
        
        # Enviar texto
        requests.post(url, data=message.encode('utf-8'), headers=headers, timeout=10)
        
        # Enviar imagen si existe
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                requests.put(url, data=f, headers={"Filename": "m82_chart.png"}, timeout=15)
        print("📲 [NTFY] Alerta enviada con éxito.")
    except Exception as e:
        print(f"⚠️ Error enviando a NTFY: {e}")

def send_telegram(message, image_path=None):
    if TELEGRAM_BOT_TOKEN == "TU_TELEGRAM_BOT_TOKEN":
        print("⚠️ Token de Telegram no configurado en entorno (TELEGRAM_BOT_TOKEN). Omitiendo Telegram.")
        return
    try:
        # Enviar Imagen
        if image_path and os.path.exists(image_path):
            url_photo = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(image_path, 'rb') as photo:
                requests.post(url_photo, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': message[:1024]}, files={'photo': photo}, timeout=15)
        else:
            url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url_msg, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message}, timeout=10)
        print("💬 [TELEGRAM] Mensaje enviado con éxito.")
    except Exception as e:
        print(f"⚠️ Error enviando a Telegram: {e}")

def dispatch_pending_signals():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Obtener señales pendientes
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 5;")
    rows = c.fetchall()
    
    if not rows and not os.path.exists(IMG_PATH):
        print("ℹ️ No hay señales pendientes ni tarjetas para emitir.")
        conn.close()
        return

    print(f"🚀 Procesando {len(rows)} eventos pendientes para Telegram y Ntfy...")
    
    for row in rows:
        rec_id, source, headline = row
        msg = f"[{source}]\n{headline}"
        
        send_ntfy(msg, title=f"M82 Signal: {source}", image_path=IMG_PATH)
        send_telegram(msg, image_path=IMG_PATH)
        
        # Marcar como PROCESSED
        c.execute("UPDATE m82_multi_stream SET status = 'PROCESSED' WHERE id = ?;", (rec_id,))
        conn.commit()

    # Si no hay rows en PENDING pero queremos forzar la emisión del HUD actual:
    if not rows and os.path.exists(IMG_PATH):
        hud_msg = "📊 [M82 HUD REPORT] Actualización de Tarjeta Gráfica y Squeeze Físico"
        send_ntfy(hud_msg, title="M82 HUD UPDATE", image_path=IMG_PATH)
        send_telegram(hud_msg, image_path=IMG_PATH)

    conn.close()

if __name__ == "__main__":
    dispatch_pending_signals()
