import requests
import os

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def alert_threshold(asset, type, detail):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg = (
        f"🚨 **ALERTA DE UMBRAL CRÍTICO - M82 CORE**\n\n"
        f"🎯 **ACTIVO:** {asset}\n"
        f"⚠️ **EVENTO:** {type}\n"
        f"📊 **DETALLE:** {detail}\n\n"
        f"⚖️ *Acción Sugerida: Vigilar Volumen en Moomoo*"
    )
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    # Configurando umbrales para Semiconductores (ON, INTT)
    # Estos se dispararán cuando los webhooks detecten el cruce
    alert_threshold(
        "SEMICONDUCTORES (ON/INTT)", 
        "Prioridad Alta", 
        "Cruce de volumen detectado tras Block Buy. Umbrales de AGI configurados."
    )
