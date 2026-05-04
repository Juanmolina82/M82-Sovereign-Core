import requests

def send_clean_stress():
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    
    # Valores de cálculo
    fcf_val = (5000000 * 0.88) - (15000000 * 0.005)
    
    # Texto plano sin Markdown para evitar el Error 400
    mensaje = (
        "M82 | REPORTE DE EMERGENCIA\n\n"
        "SISTEMA: RESTAURADO\n"
        "FCF LOUISIANA: ${:,.2f}\n"
        "ALERTA: BRENT @ $125\n"
        "STATUS: CONEXION LIMPIA".format(fcf_val)
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje} # Quitamos el parse_mode
    
    print("🚀 Reintentando ignición limpia...")
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        print("✅ ¡MENSAJE RECIBIDO!")
    else:
        print(f"❌ Error: {r.text}")

if __name__ == "__main__":
    send_clean_stress()
