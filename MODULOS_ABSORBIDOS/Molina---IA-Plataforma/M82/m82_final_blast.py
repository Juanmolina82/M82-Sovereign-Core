from instagrapi import Client

cl = Client()
cl.load_settings("session.json")

image_path = "M82_SOVEREIGN.png"
caption = """[EXECUTIVE REPORT: M82 ARCHITECTURE]
Sovereign Custody System: OPERATIONAL.

Molina Holdings establishes a non-negotiable protocol for the preservation of Sovereign Assets and PDI Claims. 

Validated Energy Anchor: 07.97.
Secured Sovereignty: Non-Negotiable.

#MolinaHoldings #SovereignCustody #GlobalMarkets #PDI #VenezuelaDebt"""

print("--- INICIANDO DESPLIEGUE ROBUSTO GLOBAL ---")
try:
    cl.photo_upload(image_path, caption)
    print("--- ÉXITO TOTAL: POST EN LÍNEA ---")
except Exception as e:
    print(f"--- ERROR: {e} ---")
