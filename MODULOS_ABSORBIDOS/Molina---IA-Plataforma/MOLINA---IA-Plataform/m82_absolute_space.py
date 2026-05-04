import requests

def send_absolute_report():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Configuración de Tendencia
    up_green = "🟢 🔼"
    down_red = "🔴 🔽"
    
    # Cabezal y Separador Único
    header = "⬜ *M82 | STRATEGIC INTELLIGENCE*"
    divider = "━━━━━━━━━━━━━━━━━━━━"
    
    # Bloque 1: Inteligencia de Precios
    prices = (
        f"🟦 *PRICE TARGETS*\n\n"
        f"  SPOT: `$124.00` {up_green}\n"
        f"  TARGET I: `$130.00` 🚩\n"
        f"  TARGET II: `$135.00` 🚫"
    )
    
    # Bloque 2: Análisis Estructural
    analysis = (
        f"🟥 *ANÁLISIS DE ESTRUCTURA*\n\n"
        f"  ● *Riesgo:* Inminente {up_green}\n"
        f"  ● *Acción:* Protección {down_red}\n"
        f"  ● *Sentimiento:* Alerta Máxima"
    )
    
    # Construcción final sin pie de página
    mensaje = f"{header}\n{divider}\n\n{prices}\n\n{analysis}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    print("✅ Reporte de Arquitectura Absoluta desplegado.")

if __name__ == "__main__":
    send_absolute_report()
