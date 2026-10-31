import requests
import json
import os

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def send_dimon_paradox_alert():
    msg = (
        "🚨 #M82 BREAKING STREAM :: FORENSE_DESK_3_6_BANKING\n\n"
        "🏛 DIMON PARADOX — DOOM TALK vs OPTIMISTIC BOOKS\n"
        "• JPM Consumer Provision: +$50M (-91.3% YoY vs +$575M prior year)\n"
        "• JPM Corporate Reserves: +$500M ➔ $11.5B en 3M\n"
        "• WFC: Provisiones ralentizadas | Citi: +$207M (Único contrarián prudente)\n\n"
        "📉 REAL ECONOMY & HOUSING STRESS:\n"
        "• Mortgage Rates: 7.4% vs 6.3% YoY\n"
        "• IB Fees Momentum Q/Q: Citi -13%, JPM -8%, WFC -3% (Deal pipeline enfriándose)\n"
        "• Disconnect Main St vs Wall St: Complacencia en consumo vs Cobertura corporativa\n\n"
        "📊 REAJUSTE DE PESOS EN DESKS M82 V50:\n"
        "• m82_jpmorgan_chase_daemon.py: Alpha 0.91 (Señal de Topping en consumo)\n"
        "• m82_citigroup_daemon.py: Overweight relativo vs JPM/WFC por reservas realistas\n"
        "• IB Desks (GS / MS): Presión esperada en Q4 por desaceleración Q/Q\n\n"
        "🏛 @MolinaHoldings | AGI Quantum Node\n"
        "🔒 BUNKER MODE 0.30x LOCK (RD ONLY)"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    
    if res.status_code == 200:
        print("[✓] Alerta Forense Dimon Paradox despachada a Telegram.")
    else:
        print(f"[!] Error en emisión: {res.text}")

if __name__ == "__main__":
    send_dimon_paradox_alert()
