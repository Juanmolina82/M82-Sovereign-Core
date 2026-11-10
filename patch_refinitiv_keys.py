import os, json

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

payload.update({
    "refinitiv_config": {
        "primary_app_key": "f63c02203524456391dff6e36d5b0eeef78f",
        "trading_app_key": "31beeb5b955743b18beea91410403ca12ab4",
        "edp_app_key": "cc48724d2ff3439b8244cccd0ffcae8c85f4",
        "account_user": "jmmp@molina82.com",
        "company": "Molina Holdings LLC",
        "status": "BOUND_AND_ACTIVE"
    }
})

tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Refinitiv AppKeys inyectados en data.json.")
