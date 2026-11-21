import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

social_patch = {
    "wire": "M82 SOCIAL BROADCAST: Post Energético publicado en X (#Brent $94.32 / WTI $87.71) | BUNKER 0.30x LOCK",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "x_post_active": {
        "text": "#Brent $94.32 (-4.07%) WTI $87.71 | No perseguimos spikes. Custodia pasiva. 100% Dry Powder. 0 ejecuciones. #M82 #BUNKER #HedgeFund #Oil #OOTT #Crude #C02",
        "length_chars": 158,
        "status": "DISPATCHED_TO_X"
    }
}

payload.update(social_patch)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[SOCIAL OK] Post de X registrado en data.json.")
