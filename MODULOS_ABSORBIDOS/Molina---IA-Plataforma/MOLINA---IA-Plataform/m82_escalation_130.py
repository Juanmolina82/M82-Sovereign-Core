import requests

def send_escalation_alert():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Nueva Proyección M82
    brent_target = 130.0
    # A $130 el castigo sube al 18% por colapso de logística
    fcf_crisis = (5000000 * 0.82) - (15000000 * 0.0055) 
    
    lineas = [
        "🏛️ M82 | ALERTA: ESCALADA BELICA",
        "--------------------------",
        f"🚨 OBJETIVO CRITICO: ${brent_target}",
        "⚠️ RIESGO: Cierre del Estrecho de Ormuz",
        "--------------------------",
        "📊 PROYECCION DE CRISIS (LOUISIANA):",
        f"💰 FCF ESTIMADO: ${fcf_crisis:,.2f}",
        "📉 IMPACTO OPERATIVO: -18%",
        "--------------------------",
        "ESTADO: ESPERANDO RUPTURA"
    ]
    
    mensaje = "\n".join(lineas)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje})
        if r.status_code == 200:
            print("🚀 Centinela actualizado a $130. Mensaje enviado.")
        else:
            print(f"❌ Error: {r.text}")
    except Exception as e:
        print(f"🛑 Fallo de Red: {e}")

if __name__ == "__main__":
    send_escalation_alert()
