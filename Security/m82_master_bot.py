import requests
import time

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def send_m82(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"🏛️ *M82 SOVEREIGN CORE*\n{text}", "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

if __name__ == "__main__":
    send_m82("🚀 *SISTEMA DESPLEGADO.* Monitoreo de Big Data y Cuántica activo.")
    print("Bot lanzado. Revisa tu Telegram.")
    while True:
        # Aquí irá la lógica de escaneo de mercados que definimos
        time.sleep(60)
