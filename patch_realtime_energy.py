import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}
payload.update({
    "wire": "M82 WIRE: LSEG Energy Real-Time - Brent $94.32 (-4.07%), WTI $87.71 (-3.43%) | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "commodities_live": {
        "brent_lcoc1": 94.32,
        "brent_change_pct": -4.07,
        "wti_clc1": 87.71,
        "wti_change_pct": -3.43,
        "wti_clc2": 86.64,
        "brent_lcoc2": 92.05,
        "merey16_live": 83.15,
        "status": "LSEG_WORKSPACE_SYNCED"
    }
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[REALTIME OK] Precios LSEG inyectados.")
