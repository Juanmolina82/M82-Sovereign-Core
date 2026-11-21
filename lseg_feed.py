import json, os
from pathlib import Path

BASE = Path.home() / "M82"
VAULT = BASE / "vault.json"

def fetch_m82_macro_data():
    if not VAULT.exists():
        print("[ERR] vault.json no encontrado.")
        return None
        
    with open(VAULT, 'r') as f:
        vault = json.load(f)
        
    app_key = vault.get("M82_MACRO_APP_KEY")
    user = vault.get("M82_MACRO_USERNAME")
    password = vault.get("M82_MACRO_PASSWORD")
    
    if not app_key or "TU_APP_KEY" in app_key:
        print("[WARN] M82_MACRO_APP_KEY no configurada. Utilizando metrics.json en fallback.")
        return None

    # Inicialización del SDK refinitiv-data / m82_macro-data
    try:
        import refinitiv.data as rd
        rd.open_platform_session(
            app_key=app_key,
            grant=rd.session.platform.GrantPassword(username=user, password=password)
        )
        print("[OK] Sesión M82_MACRO Workspace autenticada correctamente.")
        
        # Ejemplo de extracción para el .NDX
        df = rd.get_data(['.NDX'], ['CF_LAST', 'PCTCHNG'])
        rd.close_session()
        return df
    except Exception as e:
        print(f"[ERR] Fallo en conexión M82_MACRO: {e}")
        return None

if __name__ == "__main__":
    fetch_m82_macro_data()
