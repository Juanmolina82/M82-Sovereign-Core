import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}
payload.update({
    "wire": "M82 MAIN: Fable 5.2 (Builder) + Mythos 5.2 (Auditor Limited) integrados a arquitectura M82 V63.0.01-A",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "ai_architecture": {
        "fable_5_2": "BUILDER - orch.py / patch / PWA / OBS / Tarjetas HD",
        "mythos_5_2": "AUDITOR LIMITED - Audita LSEG / Tesis / CPI / KKR 6% - Veredicto SELLAR/ESPERAR",
        "routing_file": "m82_ai_routing.py",
        "rule": "Fable construye, Mythos audita, check.py verifica, Chairman decide"
    },
    "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones"
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[AI INTEGRATION OK] Fable + Mythos sellados en CORE.")
