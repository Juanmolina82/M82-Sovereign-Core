import requests

def send_to_bot(ebitda, debt, rate_increase_bps):
    # Credenciales Blindadas
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Lógica de Estrés M82
    additional_interest = debt * (rate_increase_bps / 10000)
    reduction_factor = 0.88 # -12% por shock energético LSEG
    new_ebitda = ebitda * reduction_factor
    fcf = new_ebitda - additional_interest
    
    status = "🚨 ALERTA ROJA: RIESGO DE LIQUIDEZ" if fcf < (ebitda * 0.5) else "✅ ESTADO: RESILIENTE"
    
    msg = (
        f"🏛️ *M82 | STRESS TEST REPORT*\n\n"
        f"📊 *Escenario:* +{rate_increase_bps} bps (Shock Petróleo)\n"
        f"📉 *EBITDA Ajustado:* ${new_ebitda:,.2f}\n"
        f"💸 *Costo Adicional Deuda:* ${additional_interest:,.2f}\n"
        f"💰 *FCF Estimado:* ${fcf:,.2f}\n\n"
        f"🛡️ *VERDICTO:* {status}\n"
        f"_Protocolo Louisiana-Flow activo._"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# Ejecución de prueba con valores de base
send_to_bot(ebitda=5000000, debt=15000000, rate_increase_bps=50)
