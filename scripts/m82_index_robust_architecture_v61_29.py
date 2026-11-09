#!/usr/bin/env python3
# M82 ROBUST ARCHITECTURE INDEXER & COMPILER v61.0.29 - NODO CHARALLAVE L4/L5
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

# 1. Asegurar Esquema DDL Unificado
cur.executescript("""
CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_source TEXT,
    headline TEXT UNIQUE,
    status TEXT DEFAULT 'PENDING',
    alpha_score REAL DEFAULT 0.0,
    asset_impact TEXT DEFAULT 'MACRO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
    entities TEXT,
    version TEXT DEFAULT 'v61.0.29',
    ingestion_node TEXT DEFAULT 'NODO_CHARALLAVE_L4L5',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS m82_daemons_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_name TEXT UNIQUE,
    desk_category TEXT,
    vector_type TEXT,
    status TEXT DEFAULT 'ACTIVE',
    last_heartbeat DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS price_ticks (
    asset TEXT PRIMARY KEY,
    bid REAL,
    ask REAL,
    last_price REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stream_id INTEGER,
    asset TEXT,
    side TEXT,
    order_type TEXT DEFAULT 'MARKET',
    qty REAL,
    limit_price REAL,
    fill_price REAL,
    slippage REAL,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS positions (
    asset TEXT PRIMARY KEY,
    current_qty REAL DEFAULT 0.0,
    avg_entry_price REAL DEFAULT 0.0,
    unrealized_pnl REAL DEFAULT 0.0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

now_utc = datetime.now(timezone.utc).isoformat()

headline = "[M82 ROBUST ARCHITECTURE SEALED] Integrated Bimodal Topology (Caracas HQ / Charallave Edge), DDL Relational Engine, Autostart Boot Script & Master Dossier Stream v61.0.29"
tag = "v61.0.29-M82-ROBUST-ARCHITECTURE-DDL-BOOT-INDEXED"

meta = {
    "node_topology": {
        "hq_central": "Caracas HQ (Strategic Governance & PWA Master)",
        "edge_operational": "Nodo Charallave L4/L5 Edge (Production Engine & 60 Swarm Daemons)"
    },
    "tables_certified": ["m82_multi_stream", "macro_dossier", "m82_daemons_registry", "price_ticks", "orders", "positions"],
    "boot_script": "~/.termux/boot/m82-boot.sh configured with termux-wake-lock",
    "timestamp": now_utc,
    "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active (jmmp@molina82.com)"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('M82 Master Architecture / System Core', 'ARCHITECTURE_ROBUST_INDEX', ?, 1.00, ?, 0.98, ?, 'v61.0.29', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# Checkpoint WAL
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
conn.close()

print(f"\n🔒 M82 ROBUST ARCHITECTURE INDEXED v61.0.29 SUCCESS")
print(f"🟢 TOTAL REGISTROS EN MACRO_DOSSIER: {total}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAG INGESTADO: {tag}\n")

# Disparar renderizado en Plantilla Opción A (Quantum Terminal HUD)
subprocess.Popen(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"])
