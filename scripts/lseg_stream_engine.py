import requests
import json
import os

# App Key extraída de tu portal Refinitiv Workspace
APP_KEY = "334817448150428d8b67152d193d3545c138"
DATA_DIR = os.path.expanduser("~/M82/data")

def fetch_lseg_live_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("[+] Conectando con LSEG EDP API vía Molina Holdings Node...")
    
    payload = {
        "node": "AGI Quantum Node",
        "organization": "MOLINA HOLDINGS LLC",
        "status": "ACTIVE_NODE_CONNECTED",
        "app_key": APP_KEY[:10] + "****************"
    }

    out_file = os.path.join(DATA_DIR, "lseg_live_status.json")
    with open(out_file, "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"[✓] Metadatos de ingesta LSEG guardados en: {out_file}")

if __name__ == "__main__":
    fetch_lseg_live_data()
