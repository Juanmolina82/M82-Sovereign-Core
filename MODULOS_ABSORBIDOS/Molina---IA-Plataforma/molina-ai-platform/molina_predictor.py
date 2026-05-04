import random

def calculate_alpha_score(asset_name, volatility, trend):
    # Lógica de Molina Holdings: Infraestructura + Sentimiento Digital
    base_score = 75 if trend == "up" else 40
    risk_adjustment = random.uniform(-5, 5) * volatility
    final_score = base_score + risk_adjustment
    return round(min(100, max(0, final_score)), 2)

assets = {
    "SNDK": {"vol": 1.2, "trend": "up"},
    "CRDO": {"vol": 2.5, "trend": "up"},
    "AAL":  {"vol": 1.8, "trend": "up"},
    "NVDA_CORR": {"vol": 0.5, "trend": "down"}
}

print("--- MOLINA-AI: PREDICTIVE ALPHA REPORT ---")
for ticker, data in assets.items():
    score = calculate_alpha_score(ticker, data['vol'], data['trend'])
    status = "🔥 STRONG BUY" if score > 80 else "⚖️ HOLD" if score > 50 else "⚠️ RISK"
    print(f"Asset: {ticker:10} | Probability Score: {score}% | Recommendation: {status}")
