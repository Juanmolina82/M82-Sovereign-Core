import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

payload.update({
    "wire": "M82 WIRE: LSEG 3:38 AM VET - SoftBank LOSS ¥1.115T / Nikkei +2.7% Rebote Pre-CPI | 10 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "Reuters / Dow Jones / LSEG - SoftBank Earnings 10 Nov 07:44 GMT",
    "wire_vectors_338am_CORREGIDO": {
        "softbank_real": "Perdida neta ¥1.115T ($7.06B) Jul-Sep - Miss vs +¥53.5B esperado - Perdida ¥597.2B data-center procurement USA - Financiamiento x2 a ¥462B",
        "softbank_rally_previo": "Accion +14.38% ANTES de earnings - Rebote tecnico, no validacion de resultados - SB Energy IPO retrasado",
        "openai_exposure": "$64.6B / 13% - Riesgo concentracion, no fortaleza liquidez",
        "asia_markets": "Nikkei +2.7% a 60,471 - KOSPI +4-5.5% - Rebote post -6% viernes - Yen 158.06",
        "reading_mythos": "SoftBank confirma STRESS de financiamiento AI, no liquidez fluida. Valida BUNKER, no sesgo positivo."
    },
    "ai_audit": {
        "builder": "Fable 5.2 - CORREGIDO",
        "auditor": "Mythos 5.2 - SELLAR CORREGIDO",
        "verdict_status": "SELLADO_EN_CORE_CORREGIDO"
    },
    "risk": {
        "mode": "BUNKER MODE",
        "lock": "0.30x LOCK",
        "dry_powder": "100%",
        "executions": 0,
        "wait_for": "CPI 8:30 AM ET / 9:30 AM VET - Faltan ~4.8h"
    }
})

tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Wire LSEG 3:38 AM CORREGIDO sellado en CORE.")
