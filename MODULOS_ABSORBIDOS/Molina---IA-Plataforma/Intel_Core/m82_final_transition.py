import json
from datetime import datetime

# Cierre del dossier de riesgo legal Powell-DOJ
final_report = {
    "status": "PROBE_CLOSED",
    "prosecutor": "Jeanine Pirro",
    "key_outcome": "Warsh confirmation path cleared",
    "impact_metrics": {
        "market_uncertainty": "DECREASING",
        "fed_independence_score": "STABILIZED",
        "next_catalyst": "Senate Banking Committee Vote (Warsh)"
    },
    "strategy": "Long Tech / Neutral Bonds until Warsh inaugural speech"
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(final_report) + "\n")

print("\033[92m[SISTEMA] Dossier Macro actualizado: Riesgo Criminal Powell ELIMINADO.\033[0m")
print("\033[94m[M82] Alerta: Monitoreando ahora la confirmación de Kevin Warsh en el Senado.\033[0m")
