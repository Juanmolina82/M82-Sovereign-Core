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

# 2. Patch MERGE - Ingesta Institucional Tier-1 & Breakingviews
patch = {
    "wire": "M82 WIRE: Refinitiv Breakingviews & Tier-1 Institutions Ingested (3:43 PM)",
    "breakingviews_deluge": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "us_fiscal_rebalance": "Post-election Trump policy & Congress alignment",
        "spacex_valuation": "Physical AI & Starlink valuation upside focus",
        "china_capex_risk": "European OEMs capex compression ongoing"
    },
    "tier1_institutional_dossier": {
        "apollo_global": "APO.N - Private Credit & Origination Growth",
        "goldman_sachs": "GS.N - M&A & FICC Trading Recovery",
        "morgan_stanley": "MS.N - Wealth Management & Investment Banking Strength",
        "softbank_group": "9984.T - Asset Rotation to AI/ARM Data Centers",
        "spacex_private": "SpaceX - Secondary Market Liquidity & AI Anchor",
        "ubs_group": "UBSG.S - Credit Suisse Integration & Capital Optimization",
        "status": "INSTITUTIONAL_TIER1_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Institucional Tier-1 (1000288321-329) inyectado al Bus sin tocar OBS.")
