import json, os, sys, re
DATA = os.path.expanduser("~/M82/app/data.json")
LEDGER = os.path.expanduser("~/M82/m82_mythos_ledger.json")

# REGLAS DURAS M82 - NO SE PUEDEN SELLAR SIN EVIDENCIA
BANNED_PATTERNS = [
    ("diesel ruso operativo", "LAVROV_DIESEL - Sin evidencia, prohibido"),
    ("conversaciones en EE.UU.", "Rusia-Ucrania es ABU DHABI, no EE.UU."),
    ("UniCredit obtiene aprobacion", "UniCredit ESPERA aprobacion - Decision 16 Nov, no otorgada"),
    ("YoY CPI oficial", "BLS NO publica YoY Oct - Falta Oct 2025"),
    ("Anthropic $26B confirmado", "Anthropic $26B es DRAFT RETRACTADO"),
]

def load(p):
    try:
        with open(p) as f: return json.load(f)
    except: return {}

payload = load(DATA)
text = json.dumps(payload, ensure_ascii=False).lower()
fails = []
for pat, reason in BANNED_PATTERNS:
    if pat.lower() in text:
        fails.append(f"{pat} -> {reason}")

# Risk debe ser dict, nunca string
risk = payload.get("risk")
if isinstance(risk, str):
    fails.append("risk es string, debe ser dict")

# Debe tener auditor
audit = payload.get("ai_audit", {})
if "Mythos" not in str(audit):
    fails.append("Falta auditor Mythos 5.2")

if fails:
    print("[MYTHOS VETO] BLOQUEADO - No sellar:")
    for f in fails: print(f"  - {f}")
    # Registrar veto en ledger
    ledger = load(LEDGER)
    if not isinstance(ledger, list): ledger = []
    import time
    ledger.append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"), "veto": fails, "status": "BLOQUEADO"})
    with open(LEDGER, "w") as f: json.dump(ledger, f, indent=2)
    sys.exit(1)

print("[MYTHOS OK] Sin alucinaciones detectadas - Se puede sellar.")
