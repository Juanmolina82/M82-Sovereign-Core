import requests

def alert_blockade():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    msg = (
        "🏛️ M82 | PROTOCOLO DE BLOQUEO ACTIVO\n"
        "--------------------------\n"
        "⚠️ EVENTO: Posible bloqueo puertos Iran\n"
        "📈 BRENT FOCUS: $130 - $135\n"
        "📉 ESTRUCTURA: Maxima proteccion de caja\n"
        "--------------------------\n"
        "ESTADO: FIRME Y ALINEADO"
    )
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": msg})

if __name__ == "__main__":
    alert_blockade()
