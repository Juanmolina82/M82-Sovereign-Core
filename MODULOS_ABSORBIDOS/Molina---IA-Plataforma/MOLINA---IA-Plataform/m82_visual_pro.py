import requests

def send_strategic_analysis():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Parámetros de Análisis Estratégico
    brent_spot = 124.00
    target_escalation = 130.00
    target_critical = 135.00
    
    # Construcción Visual de Alta Densidad
    header = "🏛️ *M82 | STRATEGIC INTELLIGENCE*"
    divider = "━━━━━━━━━━━━━━━━━━━━━━━━"
    
    prices = (
        f"📊 *PRICE TARGETS*\n"
        f"  ├─ SPOT: `${brent_spot:.2f}`\n"
        f"  ├─ TARGET I: `${target_escalation:.2f}` (Escalada)\n"
        f"  └─ TARGET II: `${target_critical:.2f}` (Bloqueo)\n"
    )
    
    analysis = (
        f"🛰️ *ANÁLISIS DE ESTRUCTURA*\n"
        f"  ● *Riesgo:* Inminente - Bloqueo de Puertos IRN\n"
        f"  ● *Acción:* Protección de Flujo de Caja\n"
        f"  ● *Sentimiento:* Hawkish / Alerta Máxima\n"
    )
    
    footer = "⚖️ *ESTADO: FIRME Y ALINEADO*"
    
    mensaje = f"{header}\n{divider}\n{prices}\n{analysis}\n{divider}\n{footer}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": CHAT_ID, 
            "text": mensaje, 
            "parse_mode": "Markdown"
        })
        if r.status_code == 200:
            print("✅ Reporte Visual enviado con éxito.")
        else:
            print(f"❌ Error visual: {r.text}")
    except Exception as e:
        print(f"🛑 Error de conexión: {e}")

if __name__ == "__main__":
    send_strategic_analysis()
