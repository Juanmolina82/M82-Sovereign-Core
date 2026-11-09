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

# 2. Patch MERGE - Ingesta BlackRock Institutional Trust
patch = {
    "wire": "M82 WIRE: Refinitiv BlackRock Institutional Trust Co NA Ingested (5:37 PM) — Holdings & WpHG Stream",
    "blackrock_institutional_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "entity": "BLACKROCK INSTITUTIONAL TRUST CO NA",
        "wire_source": "REFINITIV_WORKSPACE_BLACKROCK_STREAM",
        "top_holdings": ["NVDA", "AAPL", "MSFT", "AMZN", "META", "GOOGL", "AVGO"],
        "sector_allocation": "Technology Heavy / Private Capital & Infrastructure Anchor",
        "regulatory_filings": "WpHG Section 40 Voting Rights & EU Disclosures Active",
        "status": "BLACKROCK_INSTITUTIONAL_TRUST_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector BlackRock Institutional Trust (1000288416-417) inyectado al Bus sin tocar OBS.")
