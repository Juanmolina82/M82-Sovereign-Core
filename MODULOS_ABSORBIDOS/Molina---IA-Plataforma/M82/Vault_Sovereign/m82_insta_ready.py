import sys
try:
    from instagrapi import Client
    print("\033[1;32m[SYSTEM] Motor Instagrapi verificado.\033[0m")
except ImportError:
    print("\033[1;31m[ERROR] Librería no encontrada. Ejecuta: pip install instagrapi\033[0m")
    sys.exit()

def lanzar_dossier():
    # --- CONFIGURACIÓN MOLINA HOLDINGS ---
    USER = "tu_usuario"
    PASS = "tu_password"
    
    cl = Client()
    try:
        print("[SYSTEM] Accediendo al nodo Instagram...")
        cl.login(USER, PASS)
        
        caption = """
[M82 EXECUTIVE AUDIT]
Institutional Flow: Nashville-Caracas Corridor.
Asset Base: $45B PDI | Anchor: $107.97.
MOLINA HOLDINGS LLC.
"""
        # Asegúrate de que el archivo 'm82_fleet.jpg' exista en la carpeta
        cl.photo_upload("m82_fleet.jpg", caption)
        print("\033[1;32m[SUCCESS] Despliegue en Instagram completado.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[FAILED] Error en el disparo: {e}\033[0m")

if __name__ == "__main__":
    lanzar_dossier()
