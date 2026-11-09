import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

cpi_payload = {
    "wire": "M82 CPI READINESS: Fable Build + Mythos Audit SELLAR - CPI Martes 10 Nov 8:30 AM ET (MoM +0.3% / Core +0.2%)",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "Fable 5.2 (Builder) ⊗ Mythos 5.2 (Auditor)",
    "cpi_readiness": {
        "event": "CPI US Release - Martes 10 Nov 2026 8:30 AM ET",
        "consensus_mom_headline": "+0.3% MoM",
        "consensus_mom_core": "+0.2% MoM",
        "yoy_status": "DISTORSIÓN SHUTDOWN OCTUBRE - FOCO EN LECTURA MOM",
        "september_ref": "Headline +0.6% MoM / 3.7% YoY - Core +0.3% MoM / 2.6% YoY",
        "fedwatch_odds": "~80% Probabilidad Hike Diciembre (CME Group)",
        "lseg_benchmarks": {
            "brent_lcoc1": 94.32,
            "wti_clc1": 87.71,
            "merey16_live": 83.15,
            "xau_gold_ref": 4073.59
        },
        "posture": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones hasta ver print CPI"
    },
    "ai_audit": {
        "builder": "Fable 5.2 - OK",
        "auditor": "Mythos 5.2 - VEREDICTO SELLAR",
        "verdict_status": "SELLADO_EN_CORE"
    }
}

payload.update(cpi_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] CPI Readiness construido e inyectado.")
