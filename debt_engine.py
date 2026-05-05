import requests

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def debt_alert():
    msg = (
        "🚨 **DEBT RESTRUCTURING ALERT - CORE V6.3**\n\n"
        "🏛️ **ASESOR:** Houlihan Lokey (VCC)\n"
        "📊 **DEUDA:** $170B USD (Est.)\n"
        "🛡️ **STATUS:** Preparación de Licencias OFAC post-Maduro.\n\n"
        "⚡ **Molina Holdings: Financial Intelligence Layer Active**"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    debt_alert()
