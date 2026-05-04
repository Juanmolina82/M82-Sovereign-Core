import json

# Análisis de la oferta de Amber Energy por Citgo
citgo_insight = {
    "entity": "AMBER ENERGY (Elliott Investment Management)",
    "target": "Citgo Petroleum",
    "investment_promised": "11B USD",
    "purchase_price_pdv_holding": "5.9B USD",
    "key_projects": [
        "+125k bpd en Corpus Christi (1B USD)",
        "Expansión de coquización en Lemont (500M USD)",
        "Gasolina premium en Lake Charles (250M USD)"
    ],
    "regulatory_hurdle": "OFAC Approval (US Treasury)",
    "m82_analysis": "La entrada de Elliott marca el fin del control venezolano y la integración total de Citgo al mercado de capitales de EE.UU. Es un movimiento de consolidación energética masiva."
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(citgo_insight) + "\n")

print("\033[93m[ALERTA ENERGÉTICA - CITGO]\033[0m")
print("Amber Energy promete $11.000M en inversión. Recalibrando exposición a refinados.")
