import hashlib
import datetime

# Licensed under Apache-2.0
def generate_news_dashboard():
    # Simulador de Keys de Noticias (Reuters/LSEG Data)
    news_feed = [
        {"t": "Russian drones strike Odesa", "r": "HIGH", "i": "Geopolitics"},
        {"t": "Taiwan drone exports exceed 2025", "r": "LOW", "i": "Tech"},
        {"t": "UK fastracks legislation vs antisemitism", "r": "MED", "i": "Social"}
    ]
    
    header = "⬜ M82 | QUANTUM & AGI NEWS HUB\n📜 Apache-2.0 | Q-Protocol Active"
    divider = "━━━━━━━━━━━━━━━━━━━━"
    
    print(f"{header}\n{divider}\n")
    
    for item in news_feed:
        status = "🔴" if item['r'] == "HIGH" else "🟡" if item['r'] == "MED" else "🟢"
        print(f"🛰️ {item['t']}\n  ● Impact: {item['i']}\n  ● Risk: {status} {item['r']}\n")
    
    # Firma Criptográfica
    sig_data = str(news_feed) + str(datetime.datetime.now())
    sig = hashlib.sha256(sig_data.encode()).hexdigest()[:16].upper()
    print(f"{divider}\n🔐 DIGITAL_SIG: {sig}-{datetime.datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    generate_news_dashboard()
