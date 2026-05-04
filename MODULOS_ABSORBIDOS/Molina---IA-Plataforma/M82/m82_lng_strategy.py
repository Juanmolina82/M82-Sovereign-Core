import json

# Análisis del mercado de GNL - Relevo de Qatar por EE.UU.
lng_insight = {
    "us_export_record": "32.15M Metric Tons (Jan-Apr 2026)",
    "growth_yoy": "+28%",
    "qatar_gap_filled": True,
    "key_facility_performance": "Plaquemines LNG (+240%)",
    "market_risk": "US Hurricane season & maintenance downtime",
    "m82_inference": "La dependencia de Europa del GNL de EE.UU. (72%) crea una oportunidad histórica para el gas del Caribe/Venezuela como 'back-up' estratégico ante fallos logísticos en el Golfo."
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(lng_insight) + "\n")

print("\033[96m[M82 ENERGY SCAN]\033[0m")
print("EE.UU. domina el flujo de GNL ante la crisis de Qatar. El factor clima es ahora el principal riesgo.")
