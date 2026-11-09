import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}
payload.update({
    "wire": "M82 CPI READINESS: Fable Build - CPI Martes 10 Nov 8:30 AM ET - MoM +0.3% / Core +0.2% - Sin YoY oficial por shutdown",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "cpi_readiness": {
        "event": "CPI Martes 10 Nov 2026 - 8:30 AM ET",
        "consensus_mom_headline": "+0.3% MoM",
        "consensus_mom_core": "+0.2% MoM",
        "yoy_official": "NO PUBLICADO - Falta Oct 2025 por shutdown",
        "sept_reference": "Headline +0.6% MoM / 3.7% YoY - Core +0.3% MoM / 2.6% YoY",
        "fed_dec": "~80% odds hike Dic - CME FedWatch",
        "brent_ref": "$94.32 (-4.07%)",
        "wti_ref": "$87.71 (-3.43%)",
        "xau_ref": "$4,120 aprox",
        "posture": "BUNKER 0.30x LOCK - 100% Dry Powder - 0 ejecuciones hasta ver CPI"
    },
    "ai_audit": {
        "builder": "Fable 5.2",
        "auditor": "Mythos 5.2 - PENDIENTE",
        "verdict": "PENDIENTE AUDITORIA"
    }
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] CPI Readiness construido.")
