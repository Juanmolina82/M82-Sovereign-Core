import requests

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def amber_alert():
    msg = (
        "🦅 **AMBER ENERGY / ELLIOTT TAKEOVER ACTIVE**\n"
        "💰 **INVERSIÓN:** $11,000M USD (Corpus Christi Expansion)\n"
        "🛡️ **LICENSE:** OFAC Protects until June 19.\n"
        "🏛️ **JUDGE:** Delaware Sale Order Execution Pending.\n\n"
        "⚡ **Molina Holdings: Intelligence Alignment V6.6**"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    amber_alert()
