import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

script_payload = {
    "wire": "M82 MEDIA: Guion Reels/TikTok 60s Sellado (SpaceX + Trump Energetico + Bunker CPI) | 9 Nov 2026",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "media_script": {
        "file": "scripts/script1_60s.txt",
        "duration": "60 seconds",
        "narrative_arc": "Charallave Edge -> SpaceX USSF-627 -> Venezuela Energy -> CPI Bunker Mode",
        "status": "APPROVED_FOR_PRODUCTION"
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

payload.update(script_payload)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Guion 60s inyectado en CORE.")
