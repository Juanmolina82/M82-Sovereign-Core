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
    "wire": "M82 WIRE: Refinitiv Top News Wire Ingested (3:34 PM) — Geopolitics & M&A Telemetry Verified",
    "top_news_wire_v2": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "toshiba_cvc": "Shares surge on foreign intelligence report",
        "eni_earnings": "Profit doubled in winter / Shares up 9%",
        "geopolitics_iran": "Trump high likelihood of Iran strikes if talks fail",
        "saudi_geopolitics": "Drone event reported near Riyadh financial district",
        "status": "TOP_NEWS_V2_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Top News v2 (1000288319) inyectado al Bus sin tocar OBS.")
