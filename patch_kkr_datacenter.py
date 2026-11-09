import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}

patch = {
    "wire": "M82 WIRE: KKR Co-CEO Scott Nuttall - 7 Data Center Platforms = 6% Infra AUM | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "LSEG Workspace - KKR Co-CEO Scott Nuttall Wire",
    "kkr_datacenter": {
        "co_ceo": "Scott Nuttall",
        "platforms": 7,
        "pct_infra_aum": "6%",
        "reading": "Exposicion conservadora - Confirma sobre-reaccion sectorial AI",
        "context": "KKR profit record Q3 - Accion +1% - Portafolio diversificado"
    },
    "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones - Esperando CPI Martes"
}

payload.update(patch)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[KKR OK] Nuttall 6% sellado en CORE.")
