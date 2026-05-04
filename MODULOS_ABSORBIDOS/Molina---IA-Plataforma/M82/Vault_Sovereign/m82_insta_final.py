from instagrapi import Client
import sys

def dispatch():
    USER = "juanmiguelworld"
    PASS = "Trading2026****////"
    
    cl = Client()
    print("[SYSTEM] Accediendo al nodo Instagram...")
    
    try:
        cl.login(USER, PASS)
        
        caption = """
[M82 EXECUTIVE DOSSIER]
Institutional Flow: Nashville-Caracas Corridor.
Asset Base: $45B PDI | Anchor: $107.97.
Operational Status: SYNCHRONIZED.

MOLINA HOLDINGS LLC.
#MolinaHoldings #Energy #Logistics #VLCC #Nashville #Caracas
"""
        
        print("[SYSTEM] Subiendo Dossier Visual...")
        cl.photo_upload("m82_fleet.jpg", caption)
        print("\033[1;32m[SUCCESS] Post is LIVE on Instagram. Target hit.\033[0m")
        
    except Exception as e:
        print(f"\033[1;31m[ERROR] Fallo en la conexión: {e}\033[0m")

if __name__ == "__main__":
    dispatch()
