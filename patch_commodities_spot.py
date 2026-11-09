import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Lectura defensiva
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

# 2. Patch MERGE - Commodities Spot & COMEX Telemetry
patch = {
    "wire": "M82 WIRE: Metals Telemetry Ingested (8:01 PM) — XAU $4,106.64 (+1.01%) | XAG $52.92 (+2.03%)",
    "commodities_spot_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "xau_gold_spot": {"price": 4106.64, "change_pct": 1.01, "symbol": "XAU="},
        "xag_silver_spot": {"price": 52.9256, "change_pct": 2.03, "symbol": "XAG="},
        "xpt_platinum_spot": {"price": 1553.87, "change_pct": 1.34, "symbol": "XPT="},
        "xpd_palladium_spot": {"price": 1044.50, "change_pct": 2.03, "symbol": "XPD="},
        "comex_gold_front": {"price": 4064.50, "change_pct": -0.89, "symbol": "GCc1"},
        "comex_gold_next": {"price": 4107.90, "change_pct": 0.81, "symbol": "GCc2"},
        "comex_silver_front": {"price": 51.8030, "change_pct": -0.74, "symbol": "SIc1"},
        "status": "COMMODITIES_METALS_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Commodities Metales (1000288458) inyectado al Bus sin tocar OBS.")
