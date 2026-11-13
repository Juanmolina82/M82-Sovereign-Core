#!/usr/bin/env python3
import sqlite3, os, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Credenciales de Producción Proporcionadas por Chairman Molina
TELEGRAM_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TELEGRAM_CHAT_ID = "-1004335849125"
NTFY_TOPIC = "M82-Molina-Alerts-v2"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=8)
        return r.status_code == 200
    except Exception as e:
        return False

def send_ntfy(title, text):
    try:
        r = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=text.encode('utf-8'),
            headers={"Title": title, "Priority": "high", "Tags": "chart_with_upwards_trend,newspaper"},
            timeout=8
        )
        return r.status_code == 200
    except Exception as e:
        return False

def dispatch():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    # Tomar titulares pendientes
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    
    if not rows:
        conn.close()
        return

    for row_id, source, headline in rows:
        msg = f"📡 [M82 STREAM | {source}]\n{headline}"
        
        tg_ok = send_telegram(msg)
        ntfy_ok = send_ntfy(f"M82 {source}", headline)
        
        if tg_ok or ntfy_ok:
            c.execute("UPDATE m82_multi_stream SET status = 'DISPATCHED' WHERE id = ?", (row_id,))
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    dispatch()
