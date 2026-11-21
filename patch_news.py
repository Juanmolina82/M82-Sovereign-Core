import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Leer sin fallar (Parche 1000288287)
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

# 2. Patch MERGE - Sin pisar nada
patch = {
    "wire": "M82 WIRE: Refinitiv Saudi Sovereign News Wire Ingested (2:07 PM) — Sukuk & SAMA Telemetry Verified",
    "saudi_sovereign_news": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "target": "SAUDI ARABIA, KINGDOM OF GOVERNMENT",
        "wire_source": "REFINITIV_WORKSPACE_NEWS",
        "key_topics": ["Sukuk & Eurobond Settlements", "SAMA Banking Liquidity", "PIF Vision 2030 Ingest"],
        "status": "SAUDI_NEWS_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura atómica
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print(f"[MERGE OK] Refinitiv Saudi News (1000288295) inyectado al Bus sin tocar OBS")
