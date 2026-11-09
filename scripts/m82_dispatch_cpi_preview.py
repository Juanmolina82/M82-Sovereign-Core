import requests
import json

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def send_cpi_preview_alert():
    msg = (
        "🚨 #M82 BREAKING STREAM :: CPI PREVIEW & HASSETT INTERVIEW\n\n"
        "📊 ESTIMACIONES CPI SECTORIAL (MAÑANA 8:30 AM ET):\n"
        "• MoM Consensus: +0.6% (HOT Acceleration)\n"
        "• YoY Consensus: +3.6%\n"
        "• Core Annualized: 2.0% - 2.5% (Aceleración MoM)\n\n"
        "🎙 NARRATIVA HASSETT (NEC WHITE HOUSE):\n"
        "• 3M Core Anualizado: 0.1% (Equivalente a 1% anual)\n"
        "• 3M Headline Anualizado: 2.0%\n"
        "• Labor Market: Initial Jobless Claims en mínimos desde la Segunda Guerra Mundial\n"
        "• Bloomberg Consensus: 80/80 economistas fallaron lecturas previas\n\n"
        "🏠 IMPACTO MACRO & HOUSING DESK (DESK 7):\n"
        "• Renta Fija (10Y Yield): Cayó de 5.3% ➔ 5.1%\n"
        "• Hipotecas (30Y Freddie Mac): 7.4% (Ventas de viviendas congeladas)\n"
        "• Cruce con JPM: Confirma paralización del sector inmobiliario por tasas sostenidas\n\n"
        "🏛 @MolinaHoldings | AGI Quantum Node\n"
        "🔒 BUNKER MODE 0.30x LOCK (RD ONLY)"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    
    if res.status_code == 200:
        print("[✓] Tarjeta #M82 CPI PREVIEW STREAM despachada a Telegram.")
    else:
        print(f"[!] Error en emisión: {res.text}")

if __name__ == "__main__":
    send_cpi_preview_alert()
