import json

# Análisis de la regulación de redes sociales en Noruega
tech_reg_insight = {
    "event": "NORWAY_SOCIAL_MEDIA_BAN_U16",
    "target_sector": "Big Tech / Hyperscalers",
    "impacted_entities": ["META", "GOOGL", "SNAP", "TIKTOK"],
    "regulatory_trend": "ACCELERATING (Australia -> Norway)",
    "m82_analysis": "La regulación del 'tiempo de pantalla' es el nuevo frente de batalla. Esto podría desviar capital de plataformas de consumo hacia infraestructura de IA pura."
}

with open("m82_market_intelligence.json", "a") as f:
    f.write(json.dumps(tech_reg_insight) + "\n")

print("\033[93m[ALERTA REGULATORIA]\033[0m")
print("Noruega propone prohibición de redes sociales para menores de 16 años. Analizando contagio en la UE.")
