import os, json, sqlite3, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Asegurar Estructura Directoria y SQLite WAL Mode
os.makedirs(os.path.expanduser("~/M82/app"), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("PRAGMA journal_mode=WAL;")
c.execute("PRAGMA busy_timeout=60000;")
conn.commit()
conn.close()

# 2. Re-Estructuración Atómica del CORE (10 Vectores Consolidados)
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

unified_core = {
    "m82_system_tag": "M82_MACRO_DOSSIER_ROBUSTO_V63.0.01-A",
    "governance_mode": "BUNKER_MODE_0.30X_LOCK",
    "dry_powder": "100.0%",
    "active_daemons": 60,
    "vectors_consolidated": [
        "MIDTERMS_US_POLITICAL",
        "VENEZUELA_FORTUNE_OIL_EIA_CORRECTED",
        "RUBIO_STATE_DEPT_MONITOR",
        "AI_GUARDRAILS_US_CHINA",
        "NVDA_HUANG_PROBE_UPDATE6",
        "IRAN_HORMUZ_STALEMATE",
        "JAPAN_MOF_YEN_RECORD_7.98T",
        "GOLD_4000_FLOOR_XAU_4106",
        "COMMODITIES_XAG_52.92",
        "SAUDI_GOV_PORTFOLIO_1.444T"
    ],
    "wire": "M82 MASTER CORE: Arquitectura Unificada 1 CORE / 1 REPO | 60 Daemons Listos | BUNKER 0.30x LOCK",
    "timestamp": time.strftime("%H:%M:%S VET")
}

payload.update(unified_core)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[UNIFY OK] CORE único data.json consolidado al 100%.")
