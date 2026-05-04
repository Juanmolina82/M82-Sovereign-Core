import yfinance as yf
import requests
import time
from datetime import datetime

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"
SYMBOLS = {"🛢️ BRENT": "BZ=F", "🛢️ WTI": "CL=F", "🥇 ORO": "GC=F", "₿ BTC": "BTC-USD", "📊 S&P500": "^GSPC"}

def get_data():
    report = f"🏛️ **MOLINA SOVEREIGN CORE V6-AI**\n🕒 {datetime.now().strftime('%H:%M:%S')}\n"
    report += "━━━━━━━━━━━━━━━━━━\n"
    for name, sym in SYMBOLS.items():
        try:
            t = yf.Ticker(sym)
            hist = t.history(period="1d", interval="1m")
            price = hist['Close'].iloc[-1]
            change = ((price - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
            trend = "📈" if change > 0 else "📉"
            report += f"{name}: ${price:.2f} ({change:+.2f}%) {trend}\n"
        except:
            continue
    return report

while True:
    try:
        msg = get_data()
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass
    time.sleep(10) # 10s para procesar más datos sin errores
