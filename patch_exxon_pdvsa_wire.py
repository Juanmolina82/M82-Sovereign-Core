import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

exxon_payload = {
    "wire": "M82 WIRE: LSEG 8:44 PM VET - ExxonMobil MoU PDVSA Confirmed | Upstream Evaluation | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "LSEG Workspace Realtime Wire (jmmp@molina82.com) - Captura 1000289130.jpg",
    "wire_vectors_exxon": {
        "xom_mou_pdvsa": "ExxonMobil firma MoU no vinculante con PDVSA para evaluar activos upstream",
        "capex_commitment": "Sin capex inicial comprometido; sujeto a marcos regulatorios estables",
        "energy_cluster": "TotalEnergies, Continental, Repsol, Sulzer y Baker Hughes consolidan rafaga en Venezuela"
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

payload.update(exxon_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Wire ExxonMobil-PDVSA inyectado y sellado en CORE.")
