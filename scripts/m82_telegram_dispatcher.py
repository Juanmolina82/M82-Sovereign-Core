import requests
import sys

BOT_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

def send_telegram_message(text: str, parse_mode: str = "Markdown"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        if res_data.get("ok"):
            print("[M82 DISPATCHER] Mensaje enviado exitosamente a Telegram.")
            return True
        else:
            print(f"[M82 DISPATCHER] Error en la API de Telegram: {res_data}")
            return False
    except Exception as e:
        print(f"[M82 DISPATCHER] Excepción al enviar mensaje: {e}")
        return False

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "🏛️ *M82 TELEGRAM SYSTEM*: Notificación de prueba."
    send_telegram_message(msg)
