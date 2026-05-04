import json

# Ingesta de la IPO de X-Energy y el nexo con IA
energy_insight = {
    "ticker": "X-ENERGY (IPO)",
    "market_valuation": "12B",
    "day_1_surge": 0.30,
    "key_backers": ["Amazon", "Citadel", "Ares", "ARK"],
    "strategic_moat": "5GW commitment from Amazon",
    "m82_inference": "AI demand is now decoupled from traditional grid. Nuclear is the new 'Gold Standard' for data center infra."
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(energy_insight) + "\n")

print("\033[96m[M82 ENERGY LAYER]\033[0m")
print("X-Energy IPO procesada. El Nexo IA-Nuclear es ahora un pilar de valoración.")
