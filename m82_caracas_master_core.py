#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: CARACAS HQ MASTER CORE ORCHESTRATOR
# Parent Entity: Molina Holdings LLC (Delaware / Florida)
# Venue: Caracas HQ Master Node (L5 Edge) — Corp. Intl JMM, C.A.
# ==============================================================================

import os, sqlite3, hashlib, time, json, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
GALLERY_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")
os.makedirs(GALLERY_DIR, exist_ok=True)

# Lote de Telemetría Sincronizada (Zero-PII / Refinitiv Workspace / Geopolítica)
CORE_TELEMETRY = [
    ("TECH_AI", "Anthropic Q3 $16.8B revenue + profit — Disclosed Oct 14 SF Investor Day — $2T IPO Target", "Semi Capacity Crunch vs Power Demand", 0.98),
    ("TECH_AI", "Advanced Energy Industries (AEIS) 52% Undervalued — Power Product Launch for GPU Clusters", "Semi Capacity Crunch vs Power Demand", 0.92),
    ("MACRO", "Michigan Energy Emergency declared — Grid capacity strain vs AI Data Center demand expansion", "Macro Pulse Scan", 0.89),
    ("BANKING", "Hitachi Energy CEO on Grid Infrastructure Bottlenecks & AI Power Security Requirements", "Financials Basket Compliance", 0.88),
    ("TREASURY", "US 10Y Yield shifts to 4.08% as Energy Prices Stabilize — Fixed Income Duration Relief", "Ajuste Curva & Duracion", 0.85),
    ("COMMODITIES", "Faja del Orinoco Heavy Crude Flow — Jose-Houston Corridor via Molina Holdings US Structure", "Faja Heavy Crude", 0.94),
    ("INSTITUTIONAL", "LPL Financial Institutional Desk Referral — Molina Holdings LLC (US) / Corp. Intl JMM C.A.", "Prime Brokerage Gateway", 0.95)
]

def init_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")
    
    # Esquema Unificado de Ingesta
    c.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP,
            daemon_source TEXT,
            headline TEXT,
            headline_hash TEXT UNIQUE,
            desk TEXT,
            status TEXT DEFAULT 'PENDING',
            alpha_score REAL DEFAULT 0.0,
            asset_impact TEXT DEFAULT 'MACRO'
        )
    """)
    
    # Esquema de Registro de Nodos / Sede
    c.execute("""
        CREATE TABLE IF NOT EXISTS m82_node_governance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_name TEXT UNIQUE,
            venue_location TEXT,
            corporate_parent TEXT,
            operating_sub TEXT,
            status TEXT DEFAULT 'ACTIVE',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Registrar Sede Caracas HQ
    c.execute("""
        INSERT INTO m82_node_governance (node_name, venue_location, corporate_parent, operating_sub, status)
        VALUES ('M82_CARACAS_L5_EDGE', 'Caracas HQ Master Node, Venezuela', 'Molina Holdings LLC', 'Corporacion Internacional JMM, C.A.', 'ACTIVE')
        ON CONFLICT(node_name) DO UPDATE SET
            venue_location=excluded.venue_location,
            updated_at=CURRENT_TIMESTAMP;
    """)
    
    conn.commit()
    conn.close()

def process_ingestion():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    inserted = 0
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for desk, headline, tag, alpha in CORE_TELEMETRY:
        clean_hl = f"[{desk} | Caracas HQ] {headline}"[:115]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]
        
        try:
            c.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, ?, CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha, "CARACAS_CORE"))
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # Omite duplicados detectados por SHA-256
            
    conn.commit()
    
    # Lectura de estado
    c.execute("SELECT COUNT(*) FROM m82_multi_stream")
    total_records = c.fetchone()[0]
    conn.close()
    
    print(f"✅ Ingesta de Plataforma completada: {inserted} nuevos eventos registrados.")
    print(f"📊 Registros totales en m82_database.db (WAL Mode): {total_records}")

if __name__ == "__main__":
    init_database()
    process_ingestion()
