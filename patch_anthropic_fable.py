import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}
payload.update({
    "wire": "M82 WIRE: Anthropic releases Claude Fable 5.2 + Mythos 5.2 - Mythos access limited - AI discipline",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "anthropic": {
        "models": ["Claude Fable 5.2", "Claude Mythos 5.2"],
        "focus": "Complex coding / technical work",
        "mythos_access": "LIMITED",
        "reading": "AI discipline - No free compute - Converge con KKR 6% + Banks tightening AI debt"
    },
    "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones - Esperando CPI Martes"
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[ANTHROPIC OK] Fable 5.2 / Mythos 5.2 sellado.")
