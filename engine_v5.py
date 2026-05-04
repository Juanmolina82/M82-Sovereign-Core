import requests
import yfinance as yf
from datetime import datetime
import time

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def get_market_data(symbol):
    try:
        t = yf.Ticker(symbol)
        p = t.fast_info['last_price']
        pc = t.fast_info['previous_close']
        c = ((p - pc) / pc) * 100
        return p, f"${p:.2f} ({c:+.2f}%)"
    except:
        return 0, "N/A"

print("⚡ MOTOR DE ALTA FRECUENCIA ACTIVADO (5s)")

while True:
    b_p, b_s = get_market_data("BZ=F")
    w_p, w_s = get_market_data("CL=F")
    timestamp = datetime.now().strftime('%H:%M:%S')

    status = "✅ STATUS: STABLE"
    if b_p >= 108.0 or w_p >= 102.0:
        status = "🛡️ 🚨 ALERT: ASSET PREMIUM ACTIVE"

    report = (
        f"🏛️ **MOLINA GLOBAL V5.0**\n"
        f"🕒 {timestamp}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🛢️ BRENT: {b_s}\n"
        f"🛢️ WTI: {w_s}\n"
        f"{status}"
    )

    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": report, "parse_mode": "Markdown"},
                      timeout=3)
    except:
        pass

    time.sleep(5) 
