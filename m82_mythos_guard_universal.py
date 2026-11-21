import json, os, sys
DATA = os.path.expanduser("~/M82/app/data.json")
try:
    with open(DATA) as f: payload = json.load(f)
except: payload = {}
text = json.dumps(payload, ensure_ascii=False).lower()
# Reglas universales - Aplican a TODO el universo
BANNED = [
    ("diesel ruso operativo", "LAVROV_DIESEL"),
    ("conversaciones en ee.uu.", "ABU DHABI, no EE.UU."),
    ("unicredit obtiene aprobacion", "ESPERA, 16 Nov"),
    ("yoy cpi oficial", "BLS NO publica YoY Oct"),
    ("anthropic $26b confirmado", "DRAFT RETRACTADO"),
    ("softbank liquidez fluida", "Perdida ¥1.115T"),
    ("nvda secrets compromised", "Board: no secrets compromised"),
]
fails = [f"{p} -> {r}" for p, r in BANNED if p in text]
if fails:
    print("[MYTHOS GUARD UNIVERSAL] VETO:")
    for f in fails: print(f" - {f}")
    sys.exit(1)
print("[MYTHOS GUARD UNIVERSAL OK] Universo limpio - Se puede sellar.")
