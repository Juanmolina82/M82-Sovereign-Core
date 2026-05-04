import requests
import os

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

# REFERENCIA LEGAL SEGÚN README
LICENSE = "🏛️ Licensed under the Apache License, Version 2.0 (the 'License')"

def alert_threshold(asset, type, detail):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg = (
        f"🚨 **ALERTA DE UMBRAL CRÍTICO - M82 CORE**\n\n"
        f"🎯 **ACTIVO:** {asset}\n"
        f"⚠️ **EVENTO:** {type}\n"
        f"📊 **SITUACIÓN:** {detail}\n\n"
        f"{LICENSE}\n"
        f"⚖️ © 2024 MOLINA HOLDINGS"
    )
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    alert_threshold(
        "SISTEMA UNIFICADO", 
        "Actualización Legal", 
        "Integración de Licencia Apache 2.0 completada exitosamente."
    )
