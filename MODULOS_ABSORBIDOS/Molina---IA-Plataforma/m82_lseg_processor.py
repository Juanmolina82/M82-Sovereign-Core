"""
M82 - PROCESADOR DE INTELIGENCIA LSEG
PROPIEDAD DE MOLINA HOLDINGS LLC
LICENCIA: USO EXCLUSIVO CHAIRMAN
"""

intel_apple = {
    "ticket": "AAPL",
    "last_price": 268.64,
    "change": "-1.0%",
    "iphone_revenue": 56.99e9,
    "target_miss": 0.22e9,
    "margin": "49.27%",
    "sentiment": "CAUTIOUS"
}

def evaluar_riesgo():
    print("--- M82 ANALYTICS: INFORME AAPL ---")
    print(f"Estado: {intel_apple['sentiment']}")
    print(f"Margen Bruto: {intel_apple['margin']} (SUPERIOR A ESTIMADOS)")
    print(f"Déficit en iPhone: ${intel_apple['target_miss']:,.0f}")
    print("-----------------------------------")
    print("ESTRATEGIA M82: Vigilar flujo hacia Brent $110.72")

if __name__ == "__main__":
    evaluar_riesgo()
