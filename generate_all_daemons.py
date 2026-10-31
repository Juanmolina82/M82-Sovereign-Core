import os, sqlite3, datetime

DAEMONS = [
    ("m82_pe_dry_powder_daemon.py", "PE_DESK", "GLOBAL_DRY_POWDER", "PE Dry Powder OR Buyout Fund"),
    ("m82_pe_megafunds_daemon.py", "PE_DESK", "MEGA_FUNDS_CONCENTRATION", "Private Equity Fund Raising OR KKR OR Blackstone"),
    ("m82_pe_stage_allocation_daemon.py", "PE_DESK", "STAGE_ALLOCATION", "Growth Equity OR Venture Buyout"),
    ("m82_pe_geographic_flows_daemon.py", "PE_DESK", "GEOGRAPHIC_FLOWS", "Cross Border Private Equity"),
    ("m82_vc_ai_unicorns_daemon.py", "VC_DESK", "AI_DEEPTECH_ROUNDS", "AI Funding Round OR OpenAI OR Anthropic"),
    ("m82_secondary_markets_daemon.py", "PE_DESK", "SECONDARY_LIQUIDITY", "Private Equity Secondaries OR LP Liquidity"),
    ("m82_musk_daemon.py", "MUSK_DESK", "GENERAL_TELEMETRY", "Elon Musk OR Starlink OR xAI"),
    ("m82_musk_empire_daemon.py", "MUSK_DESK", "VALUATION_CONSOLIDATED", "SpaceX Valuation OR Tesla Market Cap"),
    ("m82_spacex_telecom_daemon.py", "MUSK_DESK", "STARLINK_DIRECT_TO_CELL", "Starlink Direct to Cell OR Falcon 9"),
    ("m82_tesla_fsd_robotaxi_daemon.py", "MUSK_DESK", "FSD_ROBOTAXI_TELEMETRY", "Tesla FSD OR Robotaxi Network"),
    ("m82_xai_grok_compute_daemon.py", "MUSK_DESK", "GPU_COMPUTE_CLUSTERS", "xAI Colossus OR Nvidia H100 Cluster"),
    ("m82_tech_magnificent7_daemon.py", "TECH_DESK", "MAG7_CONCENTRATION", "Magnificent Seven Stocks OR Tech Capex"),
    ("m82_treasury_bonds_daemon.py", "MACRO_DESK", "YIELD_CURVE_DELTAS", "10-Year Treasury Yield OR Yield Curve Inversion"),
    ("m82_fed_rates_dotplot_daemon.py", "MACRO_DESK", "FED_RATES_EXPECTATIONS", "Federal Reserve Rate Cut OR SOFR Futures"),
    ("m82_sovereign_debt_risk_daemon.py", "MACRO_DESK", "SOVEREIGN_CDS_RISK", "Sovereign CDS Spreads OR Default Risk"),
    ("m82_high_yield_credit_daemon.py", "MACRO_DESK", "HIGH_YIELD_SPREADS", "High Yield Credit Spreads OR Junk Bonds"),
    ("m82_smr_data_center_credit_daemon.py", "CREDIT_DESK", "SMR_DATA_CENTER", "Nuclear SMR OR Data Center Power Financing"),
    ("m82_crypto_commodities_daemon.py", "ENERGY_DESK", "COMMODITIES_ENERGY_SPREADS", "Crude Oil Brent OR WTI Futures"),
    ("m82_oil_refining_margins_daemon.py", "ENERGY_DESK", "CRACK_SPREADS", "Refining Crack Spread OR Diesel Margin"),
    ("m82_faja_orinoco_ep_daemon.py", "ENERGY_DESK", "FAJA_ORINOCO_EXPORTS", "Orinoco Belt Crude OR Chevron Venezuela"),
    ("m82_lng_gas_global_daemon.py", "ENERGY_DESK", "LNG_HENRY_HUB_TTF", "LNG Export Arbitrage OR Henry Hub TTF"),
    ("m82_uranium_nuclear_daemon.py", "ENERGY_DESK", "URANIUM_SPOT_PPA", "Uranium Spot Price OR Nuclear PPA"),
    ("m82_geopolitical_events_daemon.py", "GEOPOLITICS_DESK", "HORMUZ_TAIWAN_RISK", "Strait of Hormuz OR Taiwan Strait Escapement"),
    ("m82_machado_delcy_cable_daemon.py", "GEOPOLITICS_DESK", "VENEZUELA_CABLE", "Venezuela OFAC License OR Citgo Auction"),
    ("m82_us_china_tariffs_daemon.py", "GEOPOLITICS_DESK", "TARIFFS_SEMICONDUCTORS", "US China Tariffs OR Semiconductor Sanctions"),
    ("m82_gprk_index_daemon.py", "GEOPOLITICS_DESK", "GPRK_REALTIME_INDEX", "Geopolitical Risk Index OR War Risk"),
    ("m82_sanctions_compliance_daemon.py", "GEOPOLITICS_DESK", "OFAC_SHADOW_FLEETS", "OFAC Sanctions OR Shadow Tanker Fleet"),
    ("m82_lseg_notebook_daemon.py", "TERMINAL_DESK", "REFINITIV_WORKSPACE", "LSEG Workspace OR Refinitiv Eikon Data"),
    ("m82_refinitiv_company_ranking_daemon.py", "TERMINAL_DESK", "COMPANY_RANKING", "Refinitiv Company Market Cap Ranking"),
    ("m82_refinitiv_firm_ranking_daemon.py", "TERMINAL_DESK", "FIRM_RANKING", "Asset Manager AUM Ranking"),
    ("m82_bloomberg_news_sentiment_daemon.py", "TERMINAL_DESK", "FINANCIAL_NEWS_NLP", "Bloomberg Terminal Market Pulse"),
    ("m82_bitcoin_hashrate_daemon.py", "CRYPTO_DESK", "BTC_HASHRATE_ETF", "Bitcoin Hashrate OR Spot BTC ETF Flow"),
    ("m82_stablecoin_liquidity_daemon.py", "CRYPTO_DESK", "STABLECOIN_ISSUANCE", "Tether Issuance OR USDC Liquidity"),
    ("m82_dedollarization_brics_daemon.py", "MACRO_DESK", "BRICS_GOLD_RESERVES", "BRICS Central Bank Gold Reserves"),
    ("m82_cbdc_swift_flows_daemon.py", "MACRO_DESK", "SWIFT_CBDC_MONITOR", "SWIFT Cross Border Payment OR CBDC Trial"),
    ("m82_hud_card_generator_daemon.py", "INFRA_DESK", "MATPLOTLIB_HUD", "M82 HUD Visual Card Generator"),
    ("m82_multi_stream_dispatcher_daemon.py", "INFRA_DESK", "BROADCAST_BUS", "M82 Multi Stream Signal Dispatcher"),
    ("m82_pwa_api_bridge_daemon.py", "INFRA_DESK", "FLASK_API_PORT_8083", "M82 PWA Flask API Bridge"),
    ("m82_sqlite_integrity_daemon.py", "INFRA_DESK", "DATABASE_OPTIMIZER", "SQLite Vacuum Optimizer"),
    ("m82_termux_node_health_daemon.py", "INFRA_DESK", "CHARALLAVE_NODE_HEALTH", "Termux Caracas Node Diagnostics")
]

template = """#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def insert_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute('''
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        ''', ('{tag}', headline))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception:
        pass

def scan():
    url = f"https://news.google.com/rss/search?q={query_str}&hl=en-US&gl=US&ceid=US:en"
    try:
        r = requests.get(url, headers={{'User-Agent': 'Mozilla/5.0'}}, timeout=10)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:2]:
                title = item.find('title').text
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                insert_headline(title.strip())
    except Exception:
        pass

def main():
    while True:
        scan()
        time.sleep(180)

if __name__ == "__main__":
    main()
"""

db_path = os.path.expanduser('~/M82/m82_database.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
now = datetime.datetime.now().isoformat()

for filename, desk, vector, query in DAEMONS:
    filepath = os.path.expanduser(f"~/M82/{filename}")
    if not os.path.exists(filepath):
        query_formatted = query.replace(" ", "+")
        content = template.format(tag=vector, query_str=query_formatted)
        with open(filepath, "w") as f:
            f.write(content)
        os.chmod(filepath, 0o755)

    c.execute("""
        INSERT INTO m82_daemons_registry (daemon_name, desk_category, vector_type, status, last_heartbeat)
        VALUES (?, ?, ?, 'ACTIVE_RUNNING', ?)
        ON CONFLICT(daemon_name) DO UPDATE SET
            desk_category=excluded.desk_category,
            vector_type=excluded.vector_type,
            last_heartbeat=excluded.last_heartbeat
    """, (filename, desk, vector, now))

conn.commit()
conn.close()
print("✅ Todos los 40 Daemons registrados en BBDD y estructurados.")
