from instagrapi import Client
import sys

def dispatch_via_bridge():
    # --- CREDENCIALES UNIFICADAS ---
    USER = "juanmiguelworld"
    PASS = "Trading2026****////"
    
    cl = Client()
    # Ajustamos el User Agent para que parezca un dispositivo móvil confiable
    cl.set_user_agent("Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

    print("[SYSTEM] Intentando cruce por el puente de Facebook...")
    
    try:
        # Intentamos el login directo (instagrapi maneja el bridge internamente si detecta la vinculación)
        cl.login(USER, PASS)
        
        caption = """
[M82 EXECUTIVE DOSSIER]
Institutional Flow: Nashville-Caracas Corridor.
Asset Base: $45B PDI | Anchor: $107.97.
Operational Status: SYNCHRONIZED.

MOLINA HOLDINGS LLC.
#MolinaHoldings #Energy #Logistics #VLCC #Nashville #Caracas
"""
        
        # Usamos la imagen que ya tenemos en el búnker
        print("[SYSTEM] Subiendo Dossier Visual...")
        cl.photo_upload("m82_fleet.jpg", caption)
        print("\033[1;32m[SUCCESS] Post is LIVE via Meta Bridge.\033[0m")
        
    except Exception as e:
        print(f"\033[1;31m[ERROR] Bloqueo persistente: {e}\033[0m")
        print("[ADVICE] Chairman, active el MODO AVIÓN 10 segundos y reintente para cambiar la IP.")

if __name__ == "__main__":
    dispatch_via_bridge()
