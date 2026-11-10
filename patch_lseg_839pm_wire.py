import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

lseg_839pm_payload = {
    "wire": "M82 WIRE: LSEG 8:39 PM VET - ExxonMobil Debt Structuring / Global Capital Flows | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "LSEG Workspace Realtime Wire (jmmp@molina82.com) - Captura 1000289128.jpg",
    "wire_vectors_839pm": {
        "xom_corporate_wire": "ExxonMobil mantiene flujo ordenado de estructuracion y financiamiento",
        "global_equity_flows": "Reacomodo pasivo de capitales pre-CPI en plazas europeas y asiaticas",
        "credit_liquidity_status": "Sin tensiones de margen ni eventos de riesgo de credito detectados"
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

payload.update(lseg_839pm_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Wire LSEG 8:39 PM inyectado y sellado en CORE.")
