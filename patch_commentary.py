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

# 2. Patch MERGE - Sin pisar capas previas
patch = {
    "wire": "M82 WIRE: Refinitiv Breakingviews Commentary Ingested (3:35 PM) — Anthropic IPO & Tech Leverage",
    "breakingviews_analysis": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "anthropic_ipo_wager": "Tech leverage rise targeting Anthropic IPO",
        "uk_housing_rates": "Bank rate freeze commentary on UK real estate",
        "ai_data_centers": "Music industry AI infrastructure offloading",
        "status": "BREAKINGVIEWS_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Breakingviews (1000288320) inyectado al Bus sin tocar OBS")
