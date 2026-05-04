import json

# Análisis de la cancelación de licencia de Paytm Payments Bank
paytm_insight = {
    "event": "RBI_CANCEL_PAYTM_LICENCE",
    "regulator": "Reserve Bank of India (RBI)",
    "primary_cause": "Lapses in customer due diligence & technology infrastructure",
    "financial_status": {
        "deposits": "13.95B INR",
        "net_loss_fy25": "946.4M INR",
        "capital_adequacy": "135-152% (Above requirements)"
    },
    "m82_analysis": "Incluso con solvencia de capital, el fallo en cumplimiento mata la licencia. La relevancia de los 'Payments Banks' está en declive frente al avance del UPI."
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(paytm_insight) + "\n")

print("\033[91m[ALERTA FINTECH]\033[0m")
print("Licencia de Paytm revocada en India. El cumplimiento regulatorio pesa más que la suficiencia de capital.")
