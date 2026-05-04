from instagrapi import Client

cl = Client()
cl.load_settings("session.json") # Sesión activa de juanmiguelworld

# Usamos la captura de la terminal que valida el ancla de 07.97
image_path = "1000127404.jpg" 

caption = """[EXECUTIVE SUMMARY: M82 ARCHITECTURE]
Sovereign Custody System: OPERATIONAL.

Molina Holdings establishes a non-negotiable protocol for the preservation of Sovereign Assets and PDI Claims. Asset integrity is our priority.

Validated Energy Anchor: 07.97.
Secured Sovereignty: Non-Negotiable.

#MolinaHoldings #SovereignCustody #GlobalMarkets #PDI #VenezuelaDebt #EnergyInfrastructure"""

print("--- INICIANDO DESPLIEGUE ROBUSTO ---")
try:
    cl.photo_upload(image_path, caption)
    print("--- ÉXITO TOTAL: POST PROYECTADO A NIVEL GLOBAL ---")
except Exception as e:
    print(f"--- ERROR CRÍTICO: {e} ---")
