import os
import requests
import yfinance as yf
from pyfinviz.news import News
from datetime import datetime

def get_yfinance_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        price = info['last_price']
        prev_close = info['previous_close']
        change = ((price - prev_close) / prev_close) * 100
        return f"${price:,.2f} ({change:+.2f}%)"
    except:
        return "N/A"

def get_finviz_intel():
    try:
        news_client = News()
        headlines = news_client.news_df.head(5)['Headline'].tolist()
        keywords = ["CRASH", "BREAKING", "EMERGENCY", "HALT", "COLLAPSE"]
        alerts = [f"🚨 **{h}**" for h in headlines if any(w in h.upper() for w in keywords)]
        normal_news = [f"• {h}" for h in headlines if not any(w in h.upper() for w in keywords)]
        return alerts, normal_news[:5]
    except:
        return [], ["⚠️ News Feed: Standby."]

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Extracción de Datos
    spy = get_yfinance_data("SPY")
    qqq = get_yfinance_data("QQQ")
    dia = get_yfinance_data("DIA")
    tlt = get_yfinance_data("TLT")
    gold = get_yfinance_data("GLD")
    oil = get_yfinance_data("USO")
    
    try:
        t10y_raw = yf.Ticker("^TNX").fast_info['last_price']
        t10y = f"{t10y_raw:.2f}%"
    except:
        t10y = "N/A"

    alerts, news = get_finviz_intel()
    
    header = "🔴 **M82 EMERGENCY ALERT**\n\n" if alerts else "🏛️ **M82 ASSET MATRIX**\n\n"
    alert_block = "\n".join(alerts) + "\n\n" if alerts else ""
    
    report = (
        f"{header}"
        f"{alert_block}"
        "📈 **Equities & Indices (M82 Platform):**\n"
        f"  • SPY: {spy} | QQQ: {qqq} | DIA: {dia}\n\n"
        "🏦 **Fixed Income:**\n"
        f"  • US 10Y Yield: {t10y} | TLT: {tlt}\n\n"
        "🛡️ **Strategic ETFs:**\n"
        f"  • Gold: {gold} | Crude: {oil}\n\n"
        "📊 **M82 Order Flow Analysis:**\n"
        "  • Status: Active Tracking (Patente de Licencia General)\n"
        "  • Flow Sentiment: Institutional Monitoring ON\n\n"
        "📰 **Market Pulse:**\n"
        f"{'\n'.join(news)}\n\n"
        "⚡ *Molina Holdings: M82 Intellectual Property*"
    )
    send_intel(report)
