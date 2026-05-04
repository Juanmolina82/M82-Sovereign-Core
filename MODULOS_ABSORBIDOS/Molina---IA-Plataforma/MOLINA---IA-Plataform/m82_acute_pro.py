import requests

# Configuración Soberana Molina Holdings
TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

# Niveles Críticos M82
BRENT_LIMIT = 135.0
JPY_LIMIT = 162.0
UST10Y_LIMIT = 4.65  # Punto de ruptura para el mercado inmobiliario/corporativo

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def run_pro_scan():
    # Datos actuales basados en LSEG Workspace (30/04/2026)
    brent = 125.0
    jpy = 160.5
    ust10y = 4.43
    
    risk_level = "CRÍTICO" if brent > 120 or ust10y > 4.40 else "ALTO"
    
    report = (
        "🏛️ *M82 ACUTE PRO: VIGILANCIA DE BONOS*\n\n"
        f"🛢️ *BRENT:* ${brent} (Foco: Ormuz)\n"
        f"💹 *YEN:* {jpy} (Zona de Intervención)\n"
        f"📉 *UST 10Y:* {ust10y}% (Presión Hawk Fed)\n\n"
        f"⚠️ *ESTADO DE RIESGO:* {risk_level}\n"
        "_Recomendación: Maximizar liquidez en USD._"
    )
    
    send_alert(report)
    print("✅ Reporte de Crisis enviado al Chairman.")

if __name__ == "__main__":
    run_pro_scan()
