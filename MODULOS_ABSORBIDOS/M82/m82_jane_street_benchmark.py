import json

# Comparativa de ingresos de Market Makers - FY 2025/2026
trading_benchmarks = {
    "leader": {
        "firm": "Jane Street",
        "net_revenue": "39.6B",
        "drivers": ["Volatility Capture", "AI Stakes (Anthropic)", "ETFs/Bonds"]
    },
    "rivals": [
        {"firm": "Citadel Securities", "revenue": "12.2B"},
        {"firm": "Hudson River Trading", "revenue": "12.3B"},
        {"firm": "JPMorgan (Trading Unit)", "revenue": "35.8B"}
    ],
    "m82_insight": "Jane Street ha demostrado que la agilidad técnica + exposición a IA privada es la fórmula ganadora. Superar a JPMorgan con solo 3,500 empleados es la definición de eficiencia escalar."
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(trading_benchmarks) + "\n")

print("\033[92m[BENCHMARK COMPLETADO]\033[0m")
print("Jane Street establecida como el nuevo estándar de rentabilidad para el Macro Dossier.")
