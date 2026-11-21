#!/usr/bin/env python3
import sqlite3, os, datetime, json

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

daemons_matrix = [
    # PE & Venture Capital
    ("m82_pe_dry_powder_daemon.py", "PE_DESK", "GLOBAL_DRY_POWDER"),
    ("m82_pe_megafunds_daemon.py", "PE_DESK", "MEGA_FUNDS_CONCENTRATION"),
    ("m82_pe_stage_allocation_daemon.py", "PE_DESK", "STAGE_ALLOCATION"),
    ("m82_pe_geographic_flows_daemon.py", "PE_DESK", "GEOGRAPHIC_FLOWS"),
    ("m82_vc_ai_unicorns_daemon.py", "VC_DESK", "AI_DEEPTECH_ROUNDS"),
    ("m82_secondary_markets_daemon.py", "PE_DESK", "M82_MACROONDARY_LIQUIDITY"),
    # Musk Empire
    ("m82_musk_daemon.py", "MUSK_DESK", "GENERAL_TELEMETRY"),
    ("m82_musk_empire_daemon.py", "MUSK_DESK", "VALUATION_CONSOLIDATED"),
    ("m82_spacex_telecom_daemon.py", "MUSK_DESK", "STARLINK_DIRECT_TO_CELL"),
    ("m82_tesla_fsd_robotaxi_daemon.py", "MUSK_DESK", "FSD_ROBOTAXI_TELEMETRY"),
    ("m82_xai_grok_compute_daemon.py", "MUSK_DESK", "GPU_COMPUTE_CLUSTERS"),
    ("m82_tech_magnificent7_daemon.py", "TECH_DESK", "MAG7_CONCENTRATION"),
    # Macro & Credit
    ("m82_treasury_bonds_daemon.py", "MACRO_DESK", "YIELD_CURVE_DELTAS"),
    ("m82_fed_rates_dotplot_daemon.py", "MACRO_DESK", "FED_RATES_EXPECTATIONS"),
    ("m82_sovereign_debt_risk_daemon.py", "MACRO_DESK", "SOVEREIGN_CDS_RISK"),
    ("m82_high_yield_credit_daemon.py", "MACRO_DESK", "HIGH_YIELD_SPREADS"),
    ("m82_smr_data_center_credit_daemon.py", "CREDIT_DESK", "SMR_DATA_CENTER_PROJECT_FINANCE"),
    # Commodities & Energy
    ("m82_crypto_commodities_daemon.py", "ENERGY_DESK", "COMMODITIES_ENERGY_SPREADS"),
    ("m82_oil_refining_margins_daemon.py", "ENERGY_DESK", "CRACK_SPREADS"),
    ("m82_faja_orinoco_ep_daemon.py", "ENERGY_DESK", "FAJA_ORINOCO_EXPORTS"),
    ("m82_lng_gas_global_daemon.py", "ENERGY_DESK", "LNG_HENRY_HUB_TTF"),
    ("m82_uranium_nuclear_daemon.py", "ENERGY_DESK", "URANIUM_SPOT_PPA"),
    # Geopolitics & Cables
    ("m82_geopolitical_events_daemon.py", "GEOPOLITICS_DESK", "HORMUZ_TAIWAN_RISK"),
    ("m82_machado_delcy_cable_daemon.py", "GEOPOLITICS_DESK", "VENEZUELA_CABLE_TELEMETRY"),
    ("m82_us_china_tariffs_daemon.py", "GEOPOLITICS_DESK", "TARIFFS_SEMICONDUCTORS"),
    ("m82_gprk_index_daemon.py", "GEOPOLITICS_DESK", "GPRK_REALTIME_INDEX"),
    ("m82_sanctions_compliance_daemon.py", "GEOPOLITICS_DESK", "OFAC_SHADOW_FLEETS"),
    # Terminals & M82_MACRO
    ("m82_m82_macro_notebook_daemon.py", "TERMINAL_DESK", "M82_WIRE_WORKSPACE_NOTEBOOK"),
    ("m82_refinitiv_company_ranking_daemon.py", "TERMINAL_DESK", "COMPANY_RANKING_FEED"),
    ("m82_refinitiv_firm_ranking_daemon.py", "TERMINAL_DESK", "FIRM_RANKING_FEED"),
    ("m82_bloomberg_news_sentiment_daemon.py", "TERMINAL_DESK", "FINANCIAL_NEWS_NLP"),
    # Crypto & Monetary
    ("m82_bitcoin_hashrate_daemon.py", "CRYPTO_DESK", "BTC_HASHRATE_ETF_FLOWS"),
    ("m82_stablecoin_liquidity_daemon.py", "CRYPTO_DESK", "STABLECOIN_ISSUANCE"),
    ("m82_dedollarization_brics_daemon.py", "MACRO_DESK", "BRICS_GOLD_RESERVES"),
    ("m82_cbdc_swift_flows_daemon.py", "MACRO_DESK", "SWIFT_CBDC_MONITOR"),
    # Infrastructure & HUD
    ("m82_hud_card_generator_daemon.py", "INFRA_DESK", "MATPLOTLIB_HUD_ENGINE"),
    ("m82_multi_stream_dispatcher_daemon.py", "INFRA_DESK", "BROADCAST_NYFT_TELEGRAM"),
    ("m82_pwa_api_bridge_daemon.py", "INFRA_DESK", "FLASK_API_PORT_8083"),
    ("m82_sqlite_integrity_daemon.py", "INFRA_DESK", "DATABASE_OPTIMIZER"),
    ("m82_termux_node_health_daemon.py", "INFRA_DESK", "CHARALLAVE_NODE_HEALTH")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS m82_daemons_registry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daemon_name TEXT UNIQUE,
        desk_category TEXT,
        vector_type TEXT,
        status TEXT,
        last_heartbeat DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

now = datetime.datetime.now().isoformat()
for d_name, desk, vector in daemons_matrix:
    c.execute("""
        INSERT INTO m82_daemons_registry (daemon_name, desk_category, vector_type, status, last_heartbeat)
        VALUES (?, ?, ?, 'REGISTERED', ?)
        ON CONFLICT(daemon_name) DO UPDATE SET
            desk_category=excluded.desk_category,
            vector_type=excluded.vector_type,
            last_heartbeat=excluded.last_heartbeat
    """, (d_name, desk, vector, now))

conn.commit()

c.execute("SELECT COUNT(*) FROM m82_daemons_registry")
total_registered = c.fetchone()[0]

print(f"=== M82 DAEMON SUITE REGISTRY ===")
print(f"✅ {total_registered} Daemons registrados correctamente en m82_daemons_registry.")
print(f"🗄️ Base de datos: {DB_PATH}")

conn.close()
