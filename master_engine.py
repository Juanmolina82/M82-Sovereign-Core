import requests
import time

# Credenciales V3.2 Actualizadas
TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "7410312683"

def report(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
        print(f"Estado de envío: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    report("🏛️ **M82 CHAIRMAN BOT: ONLINE**\n\n✅ Enlace con GitHub CORE-V6 establecido.\n🛡️ Monitoreo de MP Materials y POET activo.\n⚖️ Sistema Unificado.")
