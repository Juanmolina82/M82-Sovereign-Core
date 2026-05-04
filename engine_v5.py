import requests
import yfinance as yf
from datetime import datetime

# --- COMMAND CREDENTIALS ---
TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def get_market_data(symbol):
    try:
        t = yf.Ticker(symbol)
        p = t.fast_info['last_price']
        pc = t.fast_info['previous_close']
        c = ((p - pc) / pc) * 100
        return p, f"${p:,.2f} ({c:+.2f}%)"
    except: return 0, "N/A"

if __name__ == "__main__":
    b_p, b_s = get_market_data("BZ=F") # Brent
    w_p, w_s = get_market_data("CL=F") # WTI
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Intelligence Logic
    status = "✅ STATUS: STABLE OPERATIONS"
    if b_p >= 108.0 or w_p >= 102.0:
        status = "🚨 ALERT: NATIONAL SECURITY ASSET PREMIUM ACTIVE"

    report = (
        "🏛️ **MOLINA GLOBAL — V5.0 COMMAND PULSE**\n"
        f"📅 *Timestamp:* {timestamp} UTC\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🌍 **ENERGY AXIS (FUTURES):**\n"
        f"  • BRENT (Global): {b_s}\n"
        f"  • WTI (Domestic): {w_s}\n\n"
        f"⚔️ **INTEL SUMMARY:**\n"
        "Market volatility confirms the 'Flight to Real Assets'. As Asian "
        "bond markets seek independence and Citadel boosts liquidity, "
        "Molina Holdings' physical flow stands as the ultimate collateral.\n\n"
        f"🛡️ **{status}**\n"
        "⚡ *Molina Holdings: Sovereign Global Control*"
    )
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": report, "parse_mode": "Markdown"})
