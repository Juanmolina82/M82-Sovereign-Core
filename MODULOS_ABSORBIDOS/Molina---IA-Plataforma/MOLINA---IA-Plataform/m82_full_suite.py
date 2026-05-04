import requests

def send_professional_suite():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Configuración de Tendencia (American Standard)
    up = "🟢 🔼"
    down = "🔴 🔽"
    
    header = "⬜ *M82 | STRATEGIC INTELLIGENCE*"
    license_tag = "📜 `Licensed under Apache-2.0`"
    divider = "━━━━━━━━━━━━━━━━━━━━"
    
    # Bloque 1: Mercado
    prices = (
        f"🟦 *PRICE TARGETS*\n\n"
        f"  SPOT: `$124.00` {up}\n"
        f"  T1 (Escalada): `$130.00` 🚩\n"
        f"  T2 (Bloqueo): `$135.00` 🚫"
    )
    
    # Bloque 2: Herramientas de Estructura
    tools = (
        f"🛠️ *TOOLS & ANALYSIS*\n\n"
        f"  ● *Volatility:* High (+2.74%) {up}\n"
        f"  ● *Spread Monitor:* Calibrated\n"
        f"  ● *Geo-Risk:* Active (Strait of Hormuz)"
    )
    
    # Bloque 3: Análisis de Riesgo
    analysis = (
        f"🟥 *ANÁLISIS DE ESTRUCTURA*\n\n"
        f"  ● *Riesgo:* Inminente {up}\n"
        f"  ● *Acción:* Protección {down}"
    )
    
    mensaje = f"{header}\n{license_tag}\n{divider}\n\n{prices}\n\n{tools}\n\n{analysis}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    print("✅ Suite con Licencia Apache y Herramientas desplegada.")

if __name__ == "__main__":
    send_professional_suite()
