import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

conn = sqlite3.connect(DB_PATH, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS m82_daemons_registry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daemon_name TEXT UNIQUE,
        desk_category TEXT,
        vector_type TEXT,
        status TEXT,
        last_heartbeat DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

ALL_DAEMONS = [
    # 1. PE & VC Desk (6)
    ('m82_pe_dry_powder_daemon.py', 'PE_DESK', 'GLOBAL_DRY_POWDER'),
    ('m82_pe_megafunds_daemon.py', 'PE_DESK', 'MEGA_FUNDS_CONCENTRATION'),
    ('m82_pe_stage_allocation_daemon.py', 'PE_DESK', 'STAGE_ALLOCATION'),
    ('m82_pe_geographic_flows_daemon.py', 'PE_DESK', 'GEOGRAPHIC_FLOWS'),
    ('m82_vc_ai_unicorns_daemon.py', 'VC_DESK', 'AI_DEEPTECH_ROUNDS'),
    ('m82_secondary_markets_daemon.py', 'PE_DESK', 'SECONDARY_LIQUIDITY'),
    
    # 2. Musk & Tech Desk (6)
    ('m82_musk_empire_daemon.py', 'MUSK_DESK', 'VALUATION_CONSOLIDATED'),
    ('m82_musk_daemon.py', 'MUSK_DESK', 'GENERAL_TELEMETRY'),
    ('m82_spacex_telecom_daemon.py', 'MUSK_DESK', 'STARLINK_DIRECT_TO_CELL'),
    ('m82_tesla_fsd_robotaxi_daemon.py', 'MUSK_DESK', 'FSD_ROBOTAXI_TELEMETRY'),
    ('m82_xai_grok_compute_daemon.py', 'MUSK_DESK', 'GPU_COMPUTE_CLUSTERS'),
    ('m82_tech_magnificent7_daemon.py', 'TECH_DESK', 'MAG7_CONCENTRATION'),
    
    # 3. Macro & Credit Desk (6)
    ('m82_treasury_bonds_daemon.py', 'MACRO_DESK', 'YIELD_CURVE_DELTAS'),
    ('m82_fed_rates_dotplot_daemon.py', 'MACRO_DESK', 'FED_RATES_EXPECTATIONS'),
    ('m82_sovereign_debt_risk_daemon.py', 'MACRO_DESK', 'SOVEREIGN_CDS_RISK'),
    ('m82_high_yield_credit_daemon.py', 'MACRO_DESK', 'HIGH_YIELD_SPREADS'),
    ('m82_smr_data_center_credit_daemon.py', 'CREDIT_DESK', 'SMR_DATA_CENTER_PROJECT_FINANCE'),
    ('m82_macro_daemon.py', 'MACRO_DESK', 'MACRO_INTELLIGENCE'),
    
    # 4. Commodities & Faja Desk (6)
    ('m82_crypto_commodities_daemon.py', 'ENERGY_DESK', 'COMMODITIES_ENERGY_SPREADS'),
    ('m82_oil_refining_margins_daemon.py', 'ENERGY_DESK', 'CRACK_SPREADS'),
    ('m82_faja_orinoco_ep_daemon.py', 'ENERGY_DESK', 'FAJA_ORINOCO_EXPORTS'),
    ('m82_lng_gas_global_daemon.py', 'ENERGY_DESK', 'LNG_HENRY_HUB_TTF'),
    ('m82_uranium_nuclear_daemon.py', 'ENERGY_DESK', 'URANIUM_SPOT_PPA'),
    ('m82_netback_calc.py', 'ENERGY_DESK', 'NETBACK_MODELING'),
    
    # 5. Geopolitics & Tail-Risk Desk (8)
    ('m82_geopolitical_events_daemon.py', 'GEOPOLITICS_DESK', 'HORMUZ_TAIWAN_RISK'),
    ('m82_machado_delcy_cable_daemon.py', 'GEOPOLITICS_DESK', 'VENEZUELA_CABLE_TELEMETRY'),
    ('m82_us_china_tariffs_daemon.py', 'GEOPOLITICS_DESK', 'TARIFFS_SEMICONDUCTORS'),
    ('m82_gprk_index_daemon.py', 'GEOPOLITICS_DESK', 'GPRK_REALTIME_INDEX'),
    ('m82_sanctions_compliance_daemon.py', 'GEOPOLITICS_DESK', 'OFAC_SHADOW_FLEETS'),
    ('m82_southcom_monitor.py', 'GEOPOLITICS_DESK', 'CARIBBEAN_MILITARY_RISK'),
    ('m82_midterm_radar.py', 'GEOPOLITICS_DESK', 'SPR_MIDTERM_POLICY'),
    ('m82_daemon_alert_brent.py', 'GEOPOLITICS_DESK', 'BRENT_TRIGGER_SENTINEL'),
    
    # 6. Terminals & LSEG Desk (6)
    ('m82_lseg_notebook_daemon.py', 'TERMINAL_DESK', 'REFINITIV_WORKSPACE_NOTEBOOK'),
    ('refinitiv_bridge.py', 'TERMINAL_DESK', 'EIKON_BREAKING_NEWS'),
    ('ingest_lseg_api.py', 'TERMINAL_DESK', 'LSEG_REST_API_LIVE'),
    ('m82_refinitiv_company_ranking_daemon.py', 'TERMINAL_DESK', 'COMPANY_RANKING_FEED'),
    ('m82_refinitiv_firm_ranking_daemon.py', 'TERMINAL_DESK', 'FIRM_RANKING_FEED'),
    ('m82_bloomberg_news_sentiment_daemon.py', 'TERMINAL_DESK', 'FINANCIAL_NEWS_NLP'),
    
    # 7. Crypto, Arbitrage & Parity Desk (8)
    ('m82_stablecoin_liquidity_daemon.py', 'CRYPTO_DESK', 'STABLECOIN_ISSUANCE'),
    ('m82_bitcoin_hashrate_daemon.py', 'CRYPTO_DESK', 'BTC_HASHRATE_ETF_FLOWS'),
    ('m82_dedollarization_brics_daemon.py', 'MACRO_DESK', 'BRICS_GOLD_RESERVES'),
    ('m82_cbdc_swift_flows_daemon.py', 'MACRO_DESK', 'SWIFT_CBDC_MONITOR'),
    ('m82_arbitration_carry.py', 'ARBITRAGE_DESK', 'ICSID_LATAM_CARRY'),
    ('price_feeder.py', 'QUANT_DESK', 'REALTIME_PRICE_TICKS'),
    ('price_gate.py', 'QUANT_DESK', 'LIMIT_PRICE_GATEWAY'),
    ('alpha_finbert.py', 'QUANT_DESK', 'NLP_ALPHA_SCORING'),
    
    # 8. Infra, Engine & HUD Desk (18)
    ('m82_hud_card_generator_daemon.py', 'INFRA_DESK', 'MATPLOTLIB_HUD_ENGINE'),
    ('m82_multi_stream_dispatcher_daemon.py', 'INFRA_DESK', 'BROADCAST_NYFT_TELEGRAM'),
    ('m82_pwa_api_bridge_daemon.py', 'INFRA_DESK', 'FLASK_API_PORT_8083'),
    ('m82_sqlite_integrity_daemon.py', 'INFRA_DESK', 'DATABASE_OPTIMIZER'),
    ('m82_termux_node_health_daemon.py', 'INFRA_DESK', 'CHARALLAVE_NODE_HEALTH'),
    ('m82_wal_sentinel.py', 'INFRA_DESK', 'WAL_CHECKPOINT_SENTINEL'),
    ('m82_watchdog.py', 'INFRA_DESK', 'PROCESS_SUPERVISOR_PARENT'),
    ('m82_daemon_factory.py', 'INFRA_DESK', 'DYNAMIC_DAEMON_FACTORY'),
    ('m82_scheduler_v9.py', 'INFRA_DESK', 'TASK_SCHEDULER_CRON'),
    ('m82_core_orchestrator.py', 'INFRA_DESK', 'TELEGRAM_HUD_ORCHESTRATOR'),
    ('m82_engine_master.py', 'INFRA_DESK', 'TELEMETRY_ENGINE_MASTER'),
    ('m82_api_server.py', 'INFRA_DESK', 'FLASK_ENDPOINT_SERVER'),
    ('m82_macro200_engine.py', 'INFRA_DESK', 'MACRO200_CORE_LOOP'),
    ('core_ingestor.py', 'INFRA_DESK', 'SHA256_DEDUPLICATOR'),
    ('m82_telegram_bot.py', 'INFRA_DESK', 'MULTICHANNEL_DISPATCH_BOT'),
    ('orch.py', 'INFRA_DESK', 'DUAL_DISPATCH_ORCHESTRATOR'),
    ('ingest.py', 'INFRA_DESK', 'UNIFIED_SIGNAL_INGESTOR'),
    ('m82_master_dossier.py', 'INFRA_DESK', '40_THREAD_MASTER_WORKER')
]

now = datetime.datetime.now().isoformat()
for d_name, desk, vector in ALL_DAEMONS:
    c.execute("""
        INSERT INTO m82_daemons_registry (daemon_name, desk_category, vector_type, status, last_heartbeat)
        VALUES (?, ?, ?, 'ACTIVE_REGISTERED', ?)
        ON CONFLICT(daemon_name) DO UPDATE SET
            desk_category=excluded.desk_category,
            vector_type=excluded.vector_type,
            last_heartbeat=excluded.last_heartbeat
    """, (d_name, desk, vector, now))

c.execute("PRAGMA wal_checkpoint(PASSIVE);")
conn.commit()
conn.close()
print(f"✅ Sincronizados {len(ALL_DAEMONS)} daemons en m82_database.db")
