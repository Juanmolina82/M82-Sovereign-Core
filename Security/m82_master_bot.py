import requests, time, os, random

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def send_m82(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"🏛️ *M82 INTELLIGENCE*\n{text}", "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=10)
    except: pass

def get_whale_movements():
    # Simulación de Big Data de Dark Pools & Futures
    # En producción esto conectaría con APIs de flujo de órdenes
    assets = ["CL (Oil)", "NQ (Nasdaq)", "PHO (Water)", "DBA (Agri)"]
    status = ["Acumulación Institucional", "Distribución (Venta)", "Hold", "Entrada de Ballenas"]
    report = "\n".join([f"🐋 *{a}:* {random.choice(status)}" for a in assets])
    return report

if __name__ == "__main__":
    send_m82("🛡️ *MODO CENTINELA ACTIVADO.*\nIniciando reportes de flujo institucional cada 30 min.")
    while True:
        intel = get_whale_movements()
        send_m82(f"📊 *WHALE TRACKER UPDATE:*\n{intel}\n\n*STATUS:* Escenario 120/20 monitoreado.")
        time.sleep(1800) # 30 minutos
