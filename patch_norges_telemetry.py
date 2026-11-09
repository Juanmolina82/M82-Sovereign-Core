import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Lectura defensiva (Parche 1000288287)
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

# 2. Patch MERGE - Preserva todas las capas previas
patch = {
    "wire": "M82 WIRE: Refinitiv Norges Bank Investment Mgmt Ingested (6:30 PM) — Sovereign Wealth Stream",
    "norges_bank_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "entity": "NORGES BANK INVESTMENT MANAGEMENT (GPFG)",
        "wire_source": "REFINITIV_WORKSPACE_NORGES_STREAM",
        "key_allocations": ["Renewable Infrastructure Co-investments", "Prologis Logistics Partnership", "ESG Governance Voting"],
        "status": "NORGES_BANK_INVESTMENT_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Norges Bank (1000288424) inyectado al Bus sin tocar OBS.")
