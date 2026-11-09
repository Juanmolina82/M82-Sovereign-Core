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

# 2. Patch MERGE - NVIDIA Quantitative & Multi-Exchange Telemetry
patch = {
    "wire": "M82 WIRE: Refinitiv NVDA.O Ingested (10:30 PM) — Momentum 93/100 | Value 43/100 | Multi-Exchange Synced",
    "nvda_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "ticker": "NVDA.O",
        "entity": "NVIDIA CORPORATION",
        "source": "REFINITIV_WORKSPACE_NVDA_STREAM",
        "starmine_scores": {
            "value": 43,
            "momentum": 93
        },
        "peer_positioning": "Top Quantile Profitability vs Industry (AVGO, AMD, QCOM)",
        "multi_exchange": "NASDAQ / XETRA / LSE / Tradegate Synced",
        "status": "NVDA_QUANT_TELEMETRY_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector NVIDIA Quant (1000288467-468) inyectado al Bus sin tocar OBS.")
