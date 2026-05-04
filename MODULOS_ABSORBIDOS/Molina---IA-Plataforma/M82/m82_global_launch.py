from instagrapi import Client
import os

cl = Client()
# Cargamos la sesión segura que ya validaste
cl.load_settings("session.json")

# La imagen de autoridad: Infraestructura Tangible
image_path = "1000127314.jpg" 

# El Mensaje Robusto (Inglés para mercados globales)
caption = """[OFFICIAL COMMUNIQUÉ]
Sovereign Custody System: OPERATIONAL.

Molina Holdings has finalized the M82 Architecture Executive Report. Our framework establishes a non-negotiable protocol for the preservation of Sovereign Assets and PDI Claims within the Caribbean corridor.

We ensure that asset integrity and creditor rights remain uncompromised. 
Secured Sovereignty: Non-Negotiable.

#MolinaHoldings #SovereignCustody #EnergyInfrastructure #GlobalMarkets #PDI #Venezuela"""

print("--- INICIANDO DESPLIEGUE GLOBAL (INSTAGRAM & LINKEDIN) ---")
try:
    cl.photo_upload(image_path, caption)
    print("--- ÉXITO: POST EN LÍNEA. SOBERANÍA PROYECTADA ---")
except Exception as e:
    print(f"--- ERROR EN EL LANZAMIENTO: {e} ---")
