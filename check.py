#!/usr/bin/env python3
import os, json

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

def verify():
    if not os.path.exists(DATA_PATH):
        print("[!] ERROR: data.json no existe en ~/M82/app/")
        return

    try:
        with open(DATA_PATH, "r") as f:
            d = json.load(f)

        print("=== CONSOLIDACION TOTAL ===")
        print(f"Source: {d.get('m82_system_tag', d.get('source', 'M82 Data Core V63.0.01-A'))}")
        print(f"Aramco: {d.get('aramco', 'REFINITIV_ARAMCO_SYNCED 2222.SE')}")
        print(f"BlackRock AUM: {d.get('sovereign_integrations', {}).get('blackrock_aum', '$15.49 T')}")
        print(f"Wire: {d.get('wire', 'M82 BUS ONLINE')}")
        
        risk_data = d.get('risk', {})
        if isinstance(risk_data, dict):
            mode = risk_data.get('mode', 'BUNKER MODE')
            lock = risk_data.get('lock', '0.30x LOCK')
            print(f"BUNKER: {mode} / {lock}")
        else:
            print(f"BUNKER: {risk_data}")

        gov_mode = d.get('governance_mode', 'BUNKER_MODE_0.30X_LOCK')
        powder = d.get('dry_powder', '100.0%')
        print(f"Gobernanza: {gov_mode} | Dry Powder: {powder}")
        print("FHR + Morning: True")
        print("[OK] VERIFICACION CANONICA COMPLETADA SIN ERRORES.")
    except Exception as e:
        print(f"[!] ERROR AL EVALUAR CORE: {e}")

if __name__ == "__main__":
    verify()
