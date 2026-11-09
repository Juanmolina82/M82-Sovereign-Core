import requests
import json
import os
import time

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def send_stream_to_telegram():
    json_path = os.path.expanduser("~/M82/data/m82_bank_bot_stream.json")
    if not os.path.exists(json_path):
        print("[!] No se encontró el archivo de feeds. Ejecutando m82_bank_stream primero...")
        os.system("python $HOME/M82/scripts/m82_bank_stream.py")

    with open(json_path, "r") as f:
        payload = json.load(f)

    print(f"[+] Iniciando despacho de {len(payload.get('streams', []))} alertas al canal {CHAT_ID}...")

    for b in payload.get("streams", []):
        msg = (
            f"🚨 #M82 BREAKING STREAM {b['ticker']}_EARNINGS_DESK\n\n"
            f"🏦 {b['name']} Q3 2026 EARNINGS\n"
            f"• Revenue: {b['revenue']} ({b['revenue_yoy']} YoY) {b['rev_status']}\n"
            f"• Net Income: {b['net_income']} ({b['net_income_yoy']} YoY) {b['net_status']}\n"
            f"• EPS: {b['eps']} ({b['eps_yoy']} YoY vs {b['eps_prev']} 2025)\n"
            f"• ROE: {b['roe']} (vs {b['roe_prev']} 2025)\n"
            f"• Pre-Market: {b['premarket']} ({b['premarket_change']})\n\n"
            f"📌 CEO: '{b['ceo_quote']}'\n\n"
            f"🏛 @MolinaHoldings | AGI Quantum Node\n"
            f"🔒 BUNKER MODE 0.30x LOCK"
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        
        if response.status_code == 200:
            print(f"[✓] Alerta de {b['ticker']} despachada con éxito.")
        else:
            print(f"[!] Error al enviar {b['ticker']}: {response.text}")
        
        time.sleep(1) # Delay anti-rate-limit

    print("\n[✓] TRANSMISIÓN M82 COMPLETADA EN TELEGRAM.")

if __name__ == "__main__":
    send_stream_to_telegram()
