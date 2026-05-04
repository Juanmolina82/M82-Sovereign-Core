import requests

def send_overwatch_report():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Data Core
    brent_spot = 124.00
    
    # Bloques Visuales
    header = "🏛️ *M82 | STRATEGIC INTELLIGENCE*"
    divider = "━━━━━━━━━━━━━━━━━━━━━━━━"
    
    prices = (
        f"📊 *PRICE TARGETS*\n"
        f"  ├─ SPOT: `${brent_spot:.2f}`\n"
        f"  ├─ TARGET I: `$130.00` (Escalada)\n"
        f"  └─ TARGET II: `$135.00` (Bloqueo)\n"
    )
    
    analysis = (
        f"🛰️ *ANÁLISIS DE ESTRUCTURA*\n"
        f"  ● *Riesgo:* Inminente - Bloqueo IRN\n"
        f"  ● *Acción:* Protección de Flujo\n"
        f"  ● *Sentimiento:* Alerta Máxima\n"
    )
    
    # Nuevo Cintillo Inferior Alineado
    footer = "⚖️ *ESTADO: FIRME Y ALINEADO*"
    security_tag = "🔒 `SECURE_LINK: M82-SOVEREIGN-ACTUAL`"
    
    mensaje = f"{header}\n{divider}\n{prices}\n{analysis}\n{divider}\n{footer}\n{security_tag}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    print("✅ Arquitectura con doble cintillo desplegada.")

if __name__ == "__main__":
    send_overwatch_report()
