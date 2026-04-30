import requests

def send_alert(text):
    # --- CREDENCIALES SOBERANAS VERIFICADAS ---
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "6192750379" # Este es su ID detectado
    # ------------------------------------------
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ SISTEMA ONLINE: Mensaje enviado a M82Sovereign_bot")
        else:
            print(f"❌ ERROR {response.status_code}: Revise la conexión.")
    except Exception as e:
        print(f"⚠️ FALLO DE RED: {e}")

msg = "🏛️ *M82 | SOBERANÍA TOTAL CONFIRMADA*\n\n*Chairman:* Juan Molina\n*Status:* Enlace Termux-Telegram ACTIVO\n*Intelligence:* LSEG Monitor Ready\n\n_El búnker está oficialmente en línea._"
send_alert(msg)
