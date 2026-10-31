import urllib.request
import json

# Configuración NTFY
NTFY_TOPICS = ["M82-Molina-Alerts-v2", "molina82_alerts"]

# Configuración Telegram Bot (Si usas un Bot Token y Chat ID, ponlos aquí)
TELEGRAM_BOT_TOKEN = ""  # Ejemplo: "123456789:ABCdefGHI..."
TELEGRAM_CHAT_ID = ""    # Ejemplo: "-100123456789" o "123456789"

def send_ntfy(title, text):
    clean_title = title.replace("\n", " ").strip()
    payload = text.encode('utf-8')
    for topic in NTFY_TOPICS:
        try:
            url = f"https://ntfy.sh/{topic}"
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Title": clean_title,
                    "Priority": "high",
                    "Tags": "chart_with_upwards_trend"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                print(f"✅ [NTFY] {topic}: OK ({resp.status})")
        except Exception as e:
            print(f"❌ [NTFY] {topic}: {e}")

def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"✅ [TELEGRAM] OK ({resp.status})")
    except Exception as e:
        print(f"❌ [TELEGRAM] {e}")

def broadcast_alert(title, text):
    full_message = f"*{title}*\n\n{text}"
    send_ntfy(title, text)
    send_telegram(full_message)

if __name__ == "__main__":
    broadcast_alert("PRUEBA M82", "Respuesta de prueba directa enviada correctamente.")
