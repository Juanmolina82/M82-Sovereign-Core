import requests
import time

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def send_to_bot(ebitda, debt, rate_increase_bps):
    additional_interest = debt * (rate_increase_bps / 10000)
    new_ebitda = ebitda * 0.88 
    fcf = new_ebitda - additional_interest
    status = "🚨 ALERTA ROJA" if fcf < (ebitda * 0.5) else "✅ RESILIENTE"
    
    msg = (
        f"🏛️ *M82 | CÁLCULO DE ESTRÉS REALIZADO*\n\n"
        f"📊 *EBITDA:* ${new_ebitda:,.2f}\n"
        f"💸 *Interés Extra:* ${additional_interest:,.2f}\n"
        f"💰 *FCF Final:* ${fcf:,.2f}\n\n"
        f"🛡️ *VERDICTO:* {status}"
    )
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# --- CICLO DE ACTIVIDAD PERPETUA ---
print("🚀 M82 Sovereign Bot: INICIANDO VIGILANCIA PERPETUA...")
# Enviamos un mensaje de confirmación inicial
send_to_bot(5000000, 15000000, 50)

while True:
    # Aquí el bot se queda en espera. 
    # En una versión avanzada, aquí leería sus mensajes de Telegram.
    time.sleep(60) # Mantiene el proceso vivo cada minuto
