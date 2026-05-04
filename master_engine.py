import requests
import os

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def send_intel(subject, body):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg = f"🏛️ **M82 GLOBAL INTELLIGENCE - MANDO GERENCIAL**\n\n📌 **ASUNTO:** {subject}\n\n{body}\n\n⚖️ *Estatus: Operación Unificada V3.2*"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    # Primer reporte de mando AGI
    reporte = (
        "✅ **CORE UNIFICADO:** Sincronización Termux/GitHub exitosa.\n"
        "📈 **MERCADOS:** Procesando Block Buys en CHRW (111K) y Movimiento en INTT.\n"
        "🛰️ **SATÉLITE:** GitHub Actions en guardia 24/7.\n"
        "🤖 **AGI READY:** Sistema listo para recibir órdenes de alta prioridad."
    )
    send_intel("DESPLIEGUE ESTRATÉGICO", reporte)
