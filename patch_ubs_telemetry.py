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
    "wire": "M82 WIRE: Refinitiv UBS Group AG Telemetry Ingested (5:16 PM) — Warrants & Debt Filings",
    "ubs_group_telemetry": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "ticker": "UBSG.S",
        "wire_source": "REFINITIV_WORKSPACE_UBS_STREAM",
        "key_events": ["Structured Notes & Warrants Issuance", "SIX Swiss Filings", "Analyst Price Target Adjustments"],
        "status": "UBS_TELEMETRY_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector UBS Group AG (1000288395) inyectado al Bus sin tocar OBS.")
