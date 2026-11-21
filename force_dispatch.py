import os, json, requests, time

wire_msg = "⚡ M82 ALERT: Wall Street Rebound (Dow +1.27%, Nasdaq +1.87%). NVDA recortado a -5.6%. CPI Martes en foco (+2.7% YoY). BUNKER 0.30x LOCK."

# Ntfy Direct Push (Sin requerir credenciales complejas)
topic = "m82_sovereign_alerts"
try:
    r = requests.post(
        f"https://ntfy.sh/{topic}",
        data=wire_msg.encode('utf-8'),
        headers={"Title": "⚡ M82 WALL STREET REBOUND", "Priority": "high", "Tags": "chart_with_upwards_trend,rocket"},
        timeout=5
    )
    print(f"[NTFY PUSH] Estado: {r.status_code} - Alerta PUSH emitida a https://ntfy.sh/{topic}")
except Exception as e:
    print(f"[NTFY ERROR] {e}")

# Telegram Bot (Si existen variables exportadas o en script local)
token = os.getenv("TELEGRAM_TOKEN", "")
chat_id = os.getenv("CHAT_ID", "")
if token and chat_id:
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": wire_msg}, timeout=5)
        print(f"[TELEGRAM] Estado: {r.status_code} - Notificación entregada.")
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
else:
    print("[TELEGRAM] Para despertar el Bot de Telegram de forma permanente, exporte TELEGRAM_TOKEN y CHAT_ID en su ~/.bashrc")
