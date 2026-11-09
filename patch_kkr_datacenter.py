import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}
payload.update({
    "wire": "M82 WIRE: KKR Co-CEO Scott Nuttall - 7 Data Center Platforms = 6% Infra AUM | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "kkr_datacenter": {
        "co_ceo": "Scott Nuttall",
        "platforms": 7,
        "pct_infra_aum": "6%",
        "reading": "Exposicion baja - Refuerza tesis sobre-reaccion AI - Morgan Stanley / UBS",
        "context": "KKR profit record Q3 - KKR +1% hoy - No all-in AI"
    },
    "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - Sin cambio postura hasta CPI Martes"
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[KKR OK] Nuttall 6% sellado en CORE.")
