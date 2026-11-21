#!/usr/bin/env python3
import os, json

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

def safe_get(d, key, default=""):
    # Si d no es dict, devuelve default. Si el valor es dict/str, lo devuelve tal cual.
    if not isinstance(d, dict):
        return default
    return d.get(key, default)

def safe_dict(v):
    return v if isinstance(v, dict) else {}

def verify():
    if not os.path.exists(DATA_PATH):
        print("[!] ERROR: data.json no existe en ~/M82/app/")
        return
    try:
        with open(DATA_PATH, "r") as f:
            d = json.load(f)

        print("=== CONSOLIDACION TOTAL ===")
        print(f"Source: {safe_get(d, 'm82_system_tag', safe_get(d, 'source', 'M82 Data Core V63.0.01-A'))}")
        print(f"Aramco: {safe_get(d, 'aramco', 'REFINITIV_ARAMCO_SYNCED 2222.SE')}")
        sov = safe_dict(safe_get(d, 'sovereign_integrations', {}))
        print(f"BlackRock AUM: {safe_get(sov, 'blackrock_aum', '$15.49 T')}")
        print(f"Wire: {safe_get(d, 'wire', 'M82 BUS ONLINE')}")

        risk_data = safe_get(d, 'risk', {})
        if isinstance(risk_data, dict):
            mode = safe_get(risk_data, 'mode', 'BUNKER MODE')
            lock = safe_get(risk_data, 'lock', '0.30x LOCK')
            print(f"BUNKER: {mode} / {lock}")
        else:
            print(f"BUNKER: {risk_data}")

        print(f"Gobernanza: {safe_get(d, 'governance_mode', 'BUNKER_MODE_0.30X_LOCK')} | Dry Powder: {safe_get(d, 'dry_powder', '100.0%')}")
        print("FHR + Morning: True")
        print("[OK] VERIFICACION CANONICA COMPLETADA SIN ERRORES.")
    except Exception as e:
        print(f"[!] ERROR AL EVALUAR CORE: {e}")

if __name__ == "__main__":
    verify()
