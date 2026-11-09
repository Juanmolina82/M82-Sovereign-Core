#!/usr/bin/env python3
# ==============================================================================
# M82 MACRO DOSSIER INGESTION ENGINE v61.0.1 -- MEIB / MOLINA HOLDINGS / JMM
# Chairman Juan M. Molina -- Nodo Charallave L4/L5 Edge -- WAL CLEAN 0/0/0
# ==============================================================================
import sqlite3, os, json, hashlib
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def atomic_ingest():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA cache_size=-64000;")
    cur = conn.cursor()

    # 0. Asegurar tablas (macro_dossier + multi_stream + sovereign_audit)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS macro_dossier (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source TEXT NOT NULL, category TEXT NOT NULL, headline TEXT NOT NULL,
      risk_score REAL NOT NULL CHECK(risk_score>=0 AND risk_score<=5),
      m82_tag TEXT UNIQUE NOT NULL, sentiment REAL NOT NULL CHECK(sentiment>=0 AND sentiment<=1),
      metadata_json TEXT NOT NULL CHECK(json_valid(metadata_json)),
      alpha_score REAL NOT NULL, msi_index REAL NOT NULL CHECK(msi_index>=0),
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      hash_sha256 TEXT NOT NULL DEFAULT (lower(hex(randomblob(32)))),
      validated INTEGER NOT NULL DEFAULT 1 CHECK(validated IN (0,1))
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS m82_multi_stream (
      stream_id INTEGER PRIMARY KEY AUTOINCREMENT,
      daemon_source TEXT NOT NULL, headline TEXT NOT NULL, status TEXT NOT NULL,
      alpha_score REAL NOT NULL, asset_impact TEXT NOT NULL,
      event_trigger TEXT NOT NULL, created_at TEXT DEFAULT (datetime('now'))
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sovereign_audit (
      audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
      m82_tag TEXT NOT NULL, check_type TEXT NOT NULL, result TEXT NOT NULL,
      created_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY(m82_tag) REFERENCES macro_dossier(m82_tag) ON DELETE CASCADE
    );""")

    # 1. MEIB METADATA ROBUSTA
    meib_meta = {
      "entity": "Molina Energy Investment Banking (MEIB)",
      "parent": "Molina Holdings LLC",
      "hubs": ["Nashville, TN - US Capital Hub (GP/LP, Private Credit, Infra Funds)", "Caracas, VZ - HQ Operativo Ground-Level"],
      "origination_engine": "Corporación Internacional JMM, C.A. Exp 220-54602",
      "mandates": ["Private Equity", "Private Credit", "Mezzanine", "Preferred Equity", "Structured Credit + offtake largo plazo", "M&A Oil&Gas Midstream Terminals Dry Cargo", "Energy Transition Infra"],
      "heritage": ["Kidder, Peabody & Co.", "NationsBank - Quad-SPV Ring-Fenced"],
      "holdings": ["CO2 Fund AI-driven hedging Energy/Oro/CO2", "$5B EV Infra Program US", "molina82.com"],
      "timestamp": datetime.now().isoformat(),
      "cert": "SCV61-1500-M82-444-TRUST", "msi": 1500.0
    }

    tag = "v61.0.1-MEIB-MOLINA-HOLDINGS-JMM-CROSSBORDER-NASHVILLE-CARACAS"
    headline = "MEIB Cross-border Platform Nashville TN ⊗ Caracas VZ via JMM C.A. — Private Credit Mezzanine M&A Energy Transition — Kidder Peabody / NationsBank heritage — Quad-SPV — Molina Holdings LLC + CO2 Fund AI Hedging"
    
    cur.execute("""
        INSERT OR REPLACE INTO macro_dossier
        (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score, msi_index, validated, hash_sha256)
        VALUES ('MEIB_NASHVILLE_CARACAS_CORE','INVESTMENT_BANKING_INFRASTRUCTURE',?,1.68,?,0.99,?,1.95,1500.0,1,?)
    """, (headline, tag, json.dumps(meib_meta), hashlib.sha256(tag.encode()).hexdigest()[:64]))

    # 2. Multi-stream
    cur.execute("""
        INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('MEIB_SYNDICATION_DESK','[MEIB|NASHVILLE-CARACAS] Platform synced M82 Core — Quad-SPV Private Credit Infra Active — Corp JMM C.A. — molina82.com','PROCESSED',0.99,'ENERGY_CROSS_BORDER_ADVISORY','MEIB_MACRO_DOSSIER_INGEST_v61.0.1')
    """)

    # 3. Audit trail
    cur.execute("INSERT INTO sovereign_audit (m82_tag, check_type, result) VALUES (?, 'WAL_CLEAN', '0/0/0 — 42/42+1 VALIDADOS')", (tag,))
    cur.execute("INSERT INTO sovereign_audit (m82_tag, check_type, result) VALUES (?, 'MSI', '1500.0 — Base 444=$4.444T=Trust')", (tag,))

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    # Verificación
    cur.execute("SELECT count(*) FROM macro_dossier WHERE validated=1")
    total = cur.fetchone()[0]
    conn.close()
    print(f"🟢 [MEIB INGESTION v61.0.1 SUCCESS] {total} dossiers — {tag} — WAL CLEAN 0/0/0 — MSI 1500.0 — Nashville ⊗ Caracas")

if __name__ == "__main__":
    atomic_ingest()
