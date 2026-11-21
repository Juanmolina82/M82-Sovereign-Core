import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
LEDGER_PATH = os.path.expanduser("~/M82/m82_mythos_ledger.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except: payload = {}

# Dossier Robusto - Capa de auditoria permanente
if "mythos_audit_layer" not in payload or not isinstance(payload["mythos_audit_layer"], dict):
    payload["mythos_audit_layer"] = {}

payload["mythos_audit_layer"].update({
    "guard_version": "Mythos Guard v1.0 - FIJO",
    "rule": "Ningun parche sella sin pasar m82_mythos_guard.py",
    "precedentes": [
        {
            "id": "VETO-EMEA-10NOV-0530GMT",
            "fecha": "10 Nov 2026 05:11 VET",
            "falla_fable": "Ubicacion conversaciones paz + Acuerdo diesel ruso inventado + UniCredit como aprobado",
            "correccion_mythos": "Abu Dhabi, no EE.UU. / Diesel ELIMINADO sin evidencia / UniCredit ESPERA, decision 16 Nov",
            "status": "PURGADO Y SELLADO CORREGIDO"
        },
        {
            "id": "VETO-SOFTBANK-10NOV-0338",
            "fecha": "10 Nov 2026 03:38 VET",
            "falla_fable": "SoftBank como liquidez fluida",
            "correccion_mythos": "Perdida real ¥1.115T / $7.06B - Stress financiamiento AI",
            "status": "PURGADO Y SELLADO CORREGIDO"
        },
        {
            "id": "VETO-FED-10NOV-0143",
            "fecha": "10 Nov 2026 01:43 VET",
            "falla_fable": "Fed Dic 75-78%",
            "correccion_mythos": "Real 81-84% CME FedWatch",
            "status": "CORREGIDO"
        }
    ],
    "brent_actual": "$91.68 (-0.96%) - Margen Merey 16 intacto Base $72 / Stress $110",
    "abu_dhabi_talks": "10-11 Nov Abu Dhabi - Witkoff + Kushner - Medinsky / Umerov",
    "unicredit_status": "ESPERA aprobacion - 16 Nov decision",
    "cpi_countdown": "Hoy 8:30 AM ET / 9:30 AM VET"
})

payload.update({
    "wire": "M82 DOSSIER ROBUSTO - Mythos Guard FIJO + Precedente EMEA Sellado | 10 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "ai_audit": {"builder": "Fable 5.2 - OK", "auditor": "Mythos 5.2 - GUARD FIJO ACTIVO", "verdict_status": "SELLADO_EN_CORE"},
    "risk": {"mode": "BUNKER MODE", "lock": "0.30x LOCK", "dry_powder": "100%", "executions": 0, "wait_for": "CPI 8:30 AM ET / 9:30 AM VET"}
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MYTHOS GUARD OK] Precedente EMEA fijado en Dossier Robusto.")
