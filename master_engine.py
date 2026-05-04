import requests
import os

# Intenta leer de GitHub Secrets, si no, usa tus fijos
TOKEN = os.getenv("TELEGRAM_TOKEN", "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1020305418")

def report():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg = "🏛️ **M82 GLOBAL INTELLIGENCE**\n\n✅ Operación Sincronizada: Termux <-> GitHub\n🛡️ Vigilancia Geopolítica V3.2 Activa.\n📊 Status: Sovereign Core Online."
    try:
        r = requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
        print(f"Respuesta: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    report()
