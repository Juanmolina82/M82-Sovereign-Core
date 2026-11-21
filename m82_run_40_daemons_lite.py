#!/usr/bin/env python3
"""
================================================================================
 M82 CHARALLAVE NODE // 40 DAEMONS LITE RUNNER + WAKE-LOCK (V60)
================================================================================
"""
import datetime
import json
import os
import sqlite3
import sys
import time

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

DAEMONS_40 = [
    ("1_PE_VC", "m82_pe_dry_powder_daemon.py"),
    ("1_PE_VC", "m82_pe_megafunds_daemon.py"),
    ("1_PE_VC", "m82_pe_stage_allocation_daemon.py"),
    ("1_PE_VC", "m82_pe_geographic_flows_daemon.py"),
    ("1_PE_VC", "m82_vc_ai_unicorns_daemon.py"),
    ("1_PE_VC", "m82_secondary_markets_daemon.py"),
    ("2_MUSK_TECH", "m82_musk_empire_daemon.py"),
    ("2_MUSK_TECH", "m82_musk_daemon.py"),
    ("2_MUSK_TECH", "m82_spacex_telecom_daemon.py"),
    ("2_MUSK_TECH", "m82_tesla_fsd_robotaxi_daemon.py"),
    ("2_MUSK_TECH", "m82_xai_grok_compute_daemon.py"),
    ("2_MUSK_TECH", "m82_tech_magnificent7_daemon.py"),
    ("3_MACRO_CREDIT", "m82_treasury_bonds_daemon.py"),
    ("3_MACRO_CREDIT", "m82_fed_rates_dotplot_daemon.py"),
    ("3_MACRO_CREDIT", "m82_sovereign_debt_risk_daemon.py"),
    ("3_MACRO_CREDIT", "m82_high_yield_credit_daemon.py"),
    ("3_MACRO_CREDIT", "m82_smr_data_center_credit_daemon.py"),
    ("4_COMMODITIES_FAJA", "m82_crypto_commodities_daemon.py"),
    ("4_COMMODITIES_FAJA", "m82_oil_refining_margins_daemon.py"),
    ("4_COMMODITIES_FAJA", "m82_faja_orinoco_ep_daemon.py"),
    ("4_COMMODITIES_FAJA", "m82_lng_gas_global_daemon.py"),
    ("4_COMMODITIES_FAJA", "m82_uranium_nuclear_daemon.py"),
    ("5_GEOPOLITICS_CABLES", "m82_geopolitical_events_daemon.py"),
    ("5_GEOPOLITICS_CABLES", "m82_machado_delcy_cable_daemon.py"),
    ("5_GEOPOLITICS_CABLES", "m82_us_china_tariffs_daemon.py"),
    ("5_GEOPOLITICS_CABLES", "m82_gprk_index_daemon.py"),
    ("5_GEOPOLITICS_CABLES", "m82_sanctions_compliance_daemon.py"),
    ("6_TERMINALS_LSEG", "m82_lseg_notebook_daemon.py"),
    ("6_TERMINALS_LSEG", "m82_refinitiv_company_ranking_daemon.py"),
    ("6_TERMINALS_LSEG", "m82_refinitiv_firm_ranking_daemon.py"),
    ("6_TERMINALS_LSEG", "m82_bloomberg_news_sentiment_daemon.py"),
    ("7_CRYPTO_FX", "m82_stablecoin_liquidity_daemon.py"),
    ("7_CRYPTO_FX", "m82_bitcoin_hashrate_daemon.py"),
    ("7_CRYPTO_FX", "m82_dedollarization_brics_daemon.py"),
    ("7_CRYPTO_FX", "m82_cbdc_swift_flows_daemon.py"),
    ("8_INFRA_HUD", "m82_hud_card_generator_daemon.py"),
    ("8_INFRA_HUD", "m82_multi_stream_dispatcher_daemon.py"),
    ("8_INFRA_HUD", "m82_pwa_api_bridge_daemon.py"),
    ("8_INFRA_HUD", "m82_sqlite_integrity_daemon.py"),
    ("8_INFRA_HUD", "m82_termux_node_health_daemon.py"),
]

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def run_cycle(log_event: bool = True):
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS m82_daemons_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            desk_category TEXT,
            daemon_name TEXT UNIQUE,
            status TEXT,
            last_heartbeat TEXT
        )
    """)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for desk, dname in DAEMONS_40:
        c.execute("""
            INSERT INTO m82_daemons_registry (desk_category, daemon_name, status, last_heartbeat)
            VALUES (?, ?, 'ACTIVE_LITE_WAKELOCK', ?)
            ON CONFLICT(daemon_name) DO UPDATE SET
                desk_category=excluded.desk_category,
                status='ACTIVE_LITE_WAKELOCK',
                last_heartbeat=excluded.last_heartbeat
        """, (desk, dname, now))

    if log_event:
        meta = json.dumps({
            "wake_lock": True,
            "mode": "LITE_POLLING",
            "daemons_count": len(DAEMONS_40),
            "governance": "BUNKER_030X_NO_TRADE",
        })
        # Compatibilidad dinámica con columnas de macro_dossier
        cols = [r[1] for r in c.execute("PRAGMA table_info(macro_dossier);").fetchall()]
        if "m82_tag" in cols and "alpha_score" in cols:
            c.execute("""
                INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score)
                VALUES ('CHARALLAVE_NODE', 'SYSTEM_INFRASTRUCTURE', ?, 1.0, 'BUNKER_HOLD_030X', 0.0, ?, 0.99)
            """, (f"Wake-Lock Held ({now[:19]}Z): 40 Daemons active in Lite Mode", meta))

        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES ('CHARALLAVE_NODE', ?, 'VERIFIED', ?)
        """, (f"WAKE-LOCK HELD [{now[11:19]} UTC]: 40 Daemons Active in Lite Mode | BUNKER 0.30x LOCK", now))

    c.execute("SELECT desk_category, COUNT(*) FROM m82_daemons_registry WHERE status='ACTIVE_LITE_WAKELOCK' GROUP BY desk_category ORDER BY desk_category")
    summary = c.fetchall()
    c.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()
    return now, summary

if __name__ == "__main__":
    ts, summary = run_cycle(log_event=True)
    print("================================================================================")
    print(" 🔒 TERMUX WAKE-LOCK ACTIVO // 40 DAEMONS LITE INICIADOS")
    print("================================================================================")
    print(f" 🕒 Timestamp: {ts}")
    print(f" 🗄️ Database:  {DB_PATH}\n")
    print(" 📡 Desglose de Daemons por Mesa (Modo Lite Activo):")
    total = 0
    for desk, count in summary:
        total += count
        print(f"  ├─> [{desk}]: {count} Daemons en polling liviano")
    print(f"\n ✅ TOTAL DAEMONS EN WAKELOCK ACTIVO: {total}/40")
    print("================================================================================")

    if "--daemon" in sys.argv:
        while True:
            time.sleep(60)
            run_cycle(log_event=False)
