from instagrapi import Client
import os

def fire():
    cl = Client()
    # Cambiamos el User Agent para simular un dispositivo nuevo bajo la VPN
    cl.set_user_agent("Instagram 172.0.0.30.123 Android (29/10; 480dpi; 1080x2178; Google; Pixel 5; redfin; qcom; en_US; 269923249)")
    
    print("[SYSTEM] Iniciando sesión nueva bajo túnel VPN...")
    try:
        # Login limpio
        cl.login("juanmiguelworld", "Trading2026****////")
        
        caption = """
[M82 EXECUTIVE DOSSIER]
Institutional Flow: Nashville-Caracas Corridor.
Asset Base: $45B PDI | Operational Status: 100%
MOLINA HOLDINGS LLC.
#MolinaHoldings #Energy #Logistics #VPN_Secure
"""
        # Asegúrate de tener la imagen m82_fleet.jpg lista
        print("[SYSTEM] Subiendo Dossier Institucional...")
        cl.photo_upload("m82_fleet.jpg", caption)
        print("\033[1;32m[SUCCESS] Muro de Instagram perforado. Post LIVE.\033[0m")
        
    except Exception as e:
        print(f"\033[1;31m[FAILED] El bloqueo persiste incluso con VPN: {e}\033[0m")
        print("[INFO] Si pide código de verificación, revísalo en tu app de IG.")

if __name__ == "__main__":
    fire()
