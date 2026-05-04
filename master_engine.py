import requests
import os

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

# REFERENCIA DE PATENTE (Extraída de su README)
PATENT_LICENSE = "⚖️ © 2024 MOLINA HOLDINGS - Patent License: M82-AGI-INTEL-V3.2"

def alert_threshold(asset, type, detail):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # Protocolo de Opacidad: No se menciona la fuente de los datos
    msg = (
        f"🚨 **ALERTA DE UMBRAL CRÍTICO - M82 CORE**\n\n"
        f"🎯 **ACTIVO:** {asset}\n"
        f"⚠️ **EVENTO:** {type}\n"
        f"📊 **SITUACIÓN:** {detail}\n\n"
        f"{PATENT_LICENSE}"
    )
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    # Prueba de transmisión con el nuevo protocolo
    alert_threshold(
        "INTEL ESTRATÉGICA", 
        "Actualización de Sistema", 
        "Protocolo de opacidad de fuentes activo. Licencia de patente integrada."
    )
