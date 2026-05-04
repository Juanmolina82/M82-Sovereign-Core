import json

# Actualización basada en el fallo del Juez Boasberg
legal_insight = {
    "ruling": "Subpoenas Quashed",
    "judge": "James Boasberg",
    "impact_on_fed_independence": "REINFORCED",
    "warsh_path": "CLEAR / ACCELERATED",
    "market_signal": "Buy the Dip in Financials",
    "m82_action": "Confidence Index set to 0.95 for May 15th Transition"
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(legal_insight) + "\n")

print("\033[92m[INTELIGENCIA] Fallo Judicial Procesado.\033[0m")
print("\033[94m[M82] El 'Escudo Boasberg' protege la estabilidad de la transición. Reduciendo prima de riesgo.\033[0m")
