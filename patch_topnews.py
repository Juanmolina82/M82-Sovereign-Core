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

# 2. Patch MERGE — Preserva Aramco, Vesper y capas previas
patch = {
    "wire": "M82 WIRE: Refinitiv Top News Wire Ingested (3:32 PM) — US Jobs & Nuclear AI Data Centers",
    "top_news_wire": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "us_stocks": "Bounce after Jobs Data / Fed cut in doubt",
        "tech_ai": "AI Companies scramble for Nuclear Power for Data Centers",
        "tesla_cybercab": "No steering wheel design focus",
        "status": "TOP_NEWS_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Top News (1000288318) inyectado al Bus sin tocar OBS")
