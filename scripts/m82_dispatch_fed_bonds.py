import requests
import json

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def send_fed_bonds_alert():
    msg = (
        "🚨 #M82 BREAKING STREAM :: FED vs BONDS & WARSH ERA\n\n"
        "📈 DISLOCACIÓN DE TASA CORTA & SPREAD:\n"
        "• 2Y US Treasury: 4.77%\n"
        "• Fed Funds Range: 3.00% - 3.75%\n"
        "• Spread (2Y over FF): +102bps ➔ Market leading, not Fed lagging\n\n"
        "🏛 WARSH FACTOR & STRATEGY (Hassett Analysis):\n"
        "• Fed Chair Profile: Inflation Hawk / Growth-oriented\n"
        "• Policy Stance: Data-driven PAUSE (Sin necesidad de destruir la economía)\n"
        "• Inflation Trend: 3M-4M annualized core en desaceleración (1.0% - 2.0% rate)\n\n"
        "🏠 CROSS-ASSET IMPACT (DESK 3 / DESK 6 / DESK 7):\n"
        "• Housing Desk: Freddie Mac 30Y Mortgage en 7.4% ➔ Sector Inmobiliario Congelado\n"
        "• Banking Desk: NIM expandido beneficia a GS / MS / JPM\n"
        "• Sovereign Bonds: Presión persistente sobre TLT\n\n"
        "🏛 @MolinaHoldings | AGI Quantum Node\n"
        "🔒 BUNKER MODE 0.30x LOCK (RD ONLY)"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    
    if res.status_code == 200:
        print("[✓] Tarjeta #M82 FED vs BONDS STREAM despachada a Telegram.")
    else:
        print(f"[!] Error en emisión: {res.text}")

if __name__ == "__main__":
    send_fed_bonds_alert()
