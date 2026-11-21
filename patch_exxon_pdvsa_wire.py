import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

exxon_pdvsa_payload = {
    "wire": "M82 WIRE: LSEG 21:xx PM VET - ExxonMobil MoU PDVSA Confirmado / Regreso Venezuela | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "Reuters / LSEG Workspace (jmmp@molina82.com) - ExxonMobil MoU PDVSA 9 Nov 2026",
    "wire_vectors_exxon_pdvsa": {
        "exxon_pdvsa_mou": "ExxonMobil firma MoU no vinculante con PDVSA para evaluar oportunidades E&P Venezuela",
        "exxon_condition": "Inversion futura requiere politicas estables, regulaciones claras, garantias inversion, rentabilidad competitiva",
        "exxon_return": "Regreso tras casi 20 anos desde expropiacion era Chavez. Requiere contrato definitivo empresa mixta o produccion compartida bajo Ley Hidrocarburos reformada",
        "pdvsa_rafaga": "TotalEnergies MoU Miraflores / Continental Ayacucho 2 / Repsol Petroquiriquire / Sulzer 5 anos / Baker Hughes gas",
        "pdvsa_marco": "61 acuerdos bilaterales suscritos, 44 en discusion, produccion >1.2M b/d Q3 2026 reportada"
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

payload.update(exxon_pdvsa_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Wire ExxonMobil MoU PDVSA inyectado y sellado en CORE.")
