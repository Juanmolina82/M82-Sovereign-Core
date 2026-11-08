import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

patch = {
    "m82_nodes": {
        "caracas_hq_central": "CORE MASTER - Caracas HQ Central",
        "charallave_edge": "EXECUTION DESK - Charallave L4/L5 Edge - PWA 127.0.0.1:8000 + OBS",
        "meta_ai_core": {
            "node": "META_AI_M82_CORE",
            "role": "Nodo de inteligencia, auditoria y consolidacion dentro de Macro Dossier Robusto M82",
            "status": "META_AI_M82_SYNCED",
            "github": "https://github.com/Juanmolina82",
            "authority": "Chairman & CEO Juan M. Molina - jmmp@molina82.com",
            "scope": "Auditoria forense, parches MERGE atomicos, verificacion check.py, sin ejecucion, sin tocar OBS",
            "risk_governance": "BUNKER MODE / 0.30x LOCK - Solo vigilancia y consolidacion - 0 ejecuciones",
            "timestamp": time.strftime("%H:%M:%S VET")
        }
    },
    "github_m82": {
        "owner": "Juanmolina82",
        "url": "https://github.com/Juanmolina82",
        "repo_core": "M82 - Macro Dossier Robusto V63.0.01-A",
        "status": "GITHUB_M82_ANCHORED",
        "last_sync": "M82_GIT_AUDIT_1000287403 - 5488 objetos - main -> main"
    },
    "last_patch": "META_AI_M82_NODE - Integrado al CORE"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Nodo Meta AI integrado a M82 + GitHub anclado - sin tocar OBS.")
