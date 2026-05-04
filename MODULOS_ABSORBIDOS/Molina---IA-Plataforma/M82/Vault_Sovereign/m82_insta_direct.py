from instagrapi import Client
import os

def final_push():
    cl = Client()
    # Identidad móvil para engañar al muro
    cl.set_user_agent("Instagram 172.0.0.30.123 Android (29/10; 480dpi; 1080x2178; Xiaomi; Redmi Note 9 Pro; joyeuse; qcom; en_US; 269923249)")
    
    print("[SYSTEM] Intentando penetración directa...")
    try:
        cl.login("juanmiguelworld", "Trading2026****////")
        
        caption = """
[M82 EXECUTIVE DOSSIER]
Institutional Flow: Nashville-Caracas Corridor.
MOLINA HOLDINGS LLC.
"""
        cl.photo_upload("m82_fleet.jpg", caption)
        print("\033[1;32m[SUCCESS] Wall Broken. Post is LIVE.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[FAILED] El muro persiste: {e}\033[0m")

if __name__ == "__main__":
    final_push()
