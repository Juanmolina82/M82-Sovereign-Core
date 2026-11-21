import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}
anthropic_payload = {
    "wire": "M82 WIRE: LSEG 21:xx PM VET - Anthropic IPO Filing Retracted / 867M Shares $70-80 | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "audit_source": "Reuters via LSEG Workspace (jmmp@molina82.com) - Anthropic IPO UPDATE 1 EXCLUSIVE",
    "wire_vectors_anthropic": {
        "anthropic_ipo_filing": "Anthropic envio filing IPO con 867M acciones a 70-80 USD por accion",
        "anthropic_retraction": "Segundo email: detalles de pricing inexactos, filing sera actualizado luego",
        "anthropic_comment": "Anthropic declino comentar"
    },
    "ai_audit": {"builder": "Fable 5.2 - OK", "auditor": "Mythos 5.2 - SELLAR", "verdict_status": "SELLADO_EN_CORE"},
    "risk": {"mode": "BUNKER MODE", "lock": "0.30x LOCK", "dry_powder": "100%", "executions": 0, "wait_for": "CPI Martes 8:30 AM ET"}
}
payload.update(anthropic_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Wire Anthropic IPO inyectado y sellado en CORE.")
