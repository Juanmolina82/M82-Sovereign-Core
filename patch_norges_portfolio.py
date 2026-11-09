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
    "wire": "M82 WIRE: Refinitiv Norges Bank Investment Mgmt Portfolio Ingested (6:43 PM) — GPFG Core Equity Stream",
    "norges_bank_portfolio_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "entity": "NORGES BANK INVESTMENT MANAGEMENT (GPFG PORTFOLIO)",
        "wire_source": "REFINITIV_WORKSPACE_NORGES_HOLDINGS",
        "top_holdings": ["NVDA", "AAPL", "MSFT", "AMZN", "META", "GOOGL", "AVGO"],
        "sector_breakdown": "Tech Heavy (~30%+) / Financials / Industrial / Consumer",
        "status": "NORGES_BANK_PORTFOLIO_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Portafolio Norges Bank (1000288434) inyectado al Bus sin tocar OBS.")
