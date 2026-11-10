import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

lseg_8pm_payload = {
    "wire": "M82 WIRE: LSEG 8:08 PM VET - Trump Signals Russia-Ukraine End / EU Energy & Poll Vectors | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "LSEG Workspace Realtime Wire (jmmp@molina82.com) - Captura 1000289119.jpg",
    "wire_vectors_8pm": {
        "trump_ukraine_statement": "Trump indica señales fuertes para finalizar la guerra entre Rusia y Ucrania",
        "eu_coal_shipments": "Compras oportunistas de bajo volumen en envios de carbon a la UE",
        "us_approval_poll": "Encuesta Ipsos muestra aprobacion presidencial de Trump en 52%"
    },
    "ai_audit": {
        "builder": "Fable 5.2 - OK",
        "auditor": "Mythos 5.2 - SELLAR",
        "verdict_status": "SELLADO_EN_CORE"
    },
    "risk": {
        "mode": "BUNKER MODE",
        "lock": "0.30x LOCK",
        "dry_powder": "100%",
        "executions": 0,
        "wait_for": "CPI Martes 8:30 AM ET"
    }
}

payload.update(lseg_8pm_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Wire LSEG 8:08 PM inyectado y sellado en CORE.")
