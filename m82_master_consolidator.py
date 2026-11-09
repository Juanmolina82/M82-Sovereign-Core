import os, json, sqlite3, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Asegurar Estructura SQLite WAL Mode
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS m82_multi_stream (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daemon_source TEXT,
        headline TEXT UNIQUE,
        status TEXT DEFAULT 'PENDING',
        alpha_score REAL DEFAULT 0.0,
        asset_impact TEXT DEFAULT 'MACRO',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS macro_dossier (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source TEXT NOT NULL,
        category TEXT DEFAULT 'MACRO',
        headline TEXT NOT NULL,
        risk_score REAL NOT NULL,
        metadata_json TEXT,
        m82_tag TEXT DEFAULT 'M82',
        sentiment REAL DEFAULT 0.0,
        entities TEXT
    );
    """)
    conn.commit()
    conn.close()

# 2. Inyección de Estado Maestro en el Bus Atómico
def patch_master_bus():
    payload = {}
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                payload = json.load(f)
        except Exception:
            payload = {}

    master_patch = {
        "m82_core_version": "V63.0.01-A",
        "governance_mode": "BUNKER_MODE_0.30X_LOCK",
        "dry_powder": "100.0%",
        "active_daemons_count": 60,
        "nodes": {
            "caracas_hq": "CENTRAL_DIRECTIVE_STANDBY",
            "charallave_edge": "PRODUCTION_ACTIVE_L4_L5"
        },
        "sovereign_integrations": {
            "saudi_gov_aum": "$1.444T USD",
            "aramco_anchor": "91.64% ($1.323T)",
            "blackrock_aum": "$15.49T USD",
            "norges_bank": "GPFG_EQUITY_SYNCED",
            "japan_mof_record": "JPY_7.98T_SINGLE_DAY"
        },
        "watchlist": "APEC_SHENZHEN_18_19_NOV_READY",
        "wire": "M82 MASTER DOSSIER: Arquitectura Integrada v63.0.01-A | Node Charallave Edge Active | BUNKER 0.30x LOCK",
        "timestamp": time.strftime("%H:%M:%S VET")
    }

    payload.update(master_patch)
    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, DATA_PATH)
    print("[MASTER OK] Bus de datos atómico M82 consolidado e integrado.")

if __name__ == "__main__":
    init_db()
    patch_master_bus()
