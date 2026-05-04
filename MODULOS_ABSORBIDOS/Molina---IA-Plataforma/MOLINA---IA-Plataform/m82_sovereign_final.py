import requests
import sys

def send_emergency_stress():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Datos de la simulación Louisiana
    ebitda, debt, bps = 5000000, 15000000, 50
    interest_extra = debt * (bps / 10000)
    fcf_final = (ebitda * 0.88) - interest_extra
    
    mensaje = (
        "🏛️ *M82 | SISTEMA DE CONTROL SOBERANO*\n\n"
        "✅ *Bot:* @M82Sovereign_bot\n"
        "📡 *Estatus:* Activo Perpetuo\n"
        "💰 *FCF Louisiana:* ${:,.2f}\n"
        "⚠️ *Alerta:* Brent @ $125 - Monitor Activo".format(fcf_final)
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    print("🚀 Intentando ignición de mensaje...")
    try:
        response = requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}, timeout=10)
        if response.status_code == 200:
            print("✅ ¡ÉXITO! Mensaje enviado al Chairman.")
        else:
            print(f"❌ ERROR DEL SERVIDOR TELEGRAM: {response.status_code}")
            print(f"Detalle: {response.text}")
    except Exception as e:
        print(f"🛑 FALLO CRÍTICO DE RED: {e}")

if __name__ == "__main__":
    send_emergency_stress()
