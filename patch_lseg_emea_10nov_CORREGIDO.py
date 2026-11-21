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
    "wire": "M82 WIRE: LSEG EMEA Morning Call CORREGIDO - Brent $91.68 / Abu Dhabi Talks / UniCredit Pendiente | 10 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "Reuters / CNN / LSEG - Morning Call 0530 GMT CORREGIDO por Mythos",
    "wire_vectors_emea_CORREGIDO": {
        "brent_crude": "$91.68 (-0.96%) - Caida por Trump descarta strikes Iran por ahora, bloqueo Hormuz sigue",
        "wti": "$85.93 (-1.06%)",
        "us_treasury_10y": "4.8863% (+2.4 bps)",
        "geopolitics_CORREGIDO": "Conversaciones Rusia-Ucrania 2 dias en ABU DHABI, no EE.UU. - Witkoff + Kushner median - Medinsky / Umerov - Inicio 06:30 GMT",
        "lavrov_diesel": "ELIMINADO - Sin evidencia - No existe acuerdo diesel ruso operativo confirmado",
        "m_and_a_CORREGIDO": "UniCredit ESPERA aprobacion incondicional UE para Commerzbank - Decision formal 16 Nov - No otorgada aun - Reuters 9 Nov fuentes",
        "merey_margin": "Brent $91.68 mantiene margen Merey 16 - Base $72 / Stress $110 - Intacto"
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
        "wait_for": "CPI 8:30 AM ET / 9:30 AM VET - Faltan ~4.3h"
    }
})

tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] EMEA CORREGIDO sellado en CORE.")
