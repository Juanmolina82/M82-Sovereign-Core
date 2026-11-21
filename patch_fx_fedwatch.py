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

# 2. Patch MERGE - Macro FX & FedWatch Telemetry
patch = {
    "wire": "M82 WIRE: Global FX & FedWatch Telemetry Ingested (9 Nov) — USD Index 102.20 | Dec Fed Hike Odds 79%",
    "global_fx_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "usd_index": {"level": 102.20, "change_friday_pct": 0.7, "status": "STABLE_HIGH"},
        "fedwatch_dec_hike_prob": 79.0,
        "g10_crosses": {
            "eur_usd": 1.11485,
            "aud_usd": 0.6875,
            "usd_jpy": 158.185,
            "gbp_usd": 1.3360,
            "usd_cad": 1.4119,
            "nzd_usd": 0.5557
        },
        "macro_catalysts": [
            "US Payrolls surprise to upside",
            "Hawkish Fed speakers (Williams, Musalem, Daly)",
            "NZ Election results pending final count (27 Nov)"
        ],
        "status": "GLOBAL_FX_FEDWATCH_SYNCED"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atómico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector Global FX & FedWatch (Tokyo Nov 9) inyectado al Bus sin tocar OBS.")
