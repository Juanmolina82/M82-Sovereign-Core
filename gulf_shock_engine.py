import requests

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def tsunami_shock_alert():
    report = (
        "🌊 **ALERTA TSUNAMI: BRENT $112.66**\n\n"
        "🚨 **EVENTO:** Ataque con drones UAE/HMM.\n"
        "📉 **FED:** Riesgo de 'No Cuts' por inflación.\n"
        "⚔️ **M82:** Ejecutando cobertura agresiva.\n\n"
        "⚖️ © 2024 MOLINA HOLDINGS - EO 14373 Active"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': report, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    tsunami_shock_alert()
