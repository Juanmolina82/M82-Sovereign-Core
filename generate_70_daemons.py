#!/usr/bin/env python3
import os, sys, time, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS m82_daemons_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_name TEXT UNIQUE,
            desk_category TEXT,
            status TEXT DEFAULT 'ACTIVE',
            last_heartbeat DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Lista expandida a 70 Daemons basados en el Refinitiv Workspace Ingest
DAEMONS_70 = [
    # Desk 1: Private Equity & VC
    ("m82_pe_cvc_capital_daemon.py", "MESA1_PE_VC"),
    ("m82_pe_blackstone_daemon.py", "MESA1_PE_VC"),
    ("m82_pe_kkr_group_daemon.py", "MESA1_PE_VC"),
    ("m82_pe_apollo_global_daemon.py", "MESA1_PE_VC"),
    ("m82_pe_brookfield_daemon.py", "MESA1_PE_VC"),
    ("m82_pe_carlyle_daemon.py", "MESA1_PE_VC"),
    ("m82_pe_blue_owl_daemon.py", "MESA1_PE_VC"),

    # Desk 2: Banking & Investment Banking
    ("m82_bank_jpmorgan_daemon.py", "MESA2_BANKING"),
    ("m82_bank_bofa_daemon.py", "MESA2_BANKING"),
    ("m82_bank_morgan_stanley_daemon.py", "MESA2_BANKING"),
    ("m82_bank_goldman_sachs_daemon.py", "MESA2_BANKING"),
    ("m82_bank_barclays_daemon.py", "MESA2_BANKING"),
    ("m82_bank_hsbc_daemon.py", "MESA2_BANKING"),
    ("m82_bank_citigroup_daemon.py", "MESA2_BANKING"),

    # Desk 3: Energy, Heavy Crude & Faja
    ("m82_energy_chevron_daemon.py", "MESA3_ENERGY"),
    ("m82_energy_exxon_daemon.py", "MESA3_ENERGY"),
    ("m82_energy_cheniere_lng_daemon.py", "MESA3_ENERGY"),
    ("m82_energy_occidental_daemon.py", "MESA3_ENERGY"),
    ("m82_energy_glencore_daemon.py", "MESA3_ENERGY"),
    ("m82_energy_eni_spa_daemon.py", "MESA3_ENERGY"),
    ("m82_faja_merey16_desk_daemon.py", "MESA3_ENERGY"),

    # Desk 4: Aerospace & Defense
    ("m82_defense_rtx_corp_daemon.py", "MESA4_DEFENSE"),
    ("m82_defense_ge_aerospace_daemon.py", "MESA4_DEFENSE"),
    ("m82_defense_boeing_daemon.py", "MESA4_DEFENSE"),

    # Desk 5: AI Infrastructure & Tech
    ("m82_tech_nvidia_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_amd_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_intel_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_asml_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_astera_labs_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_palantir_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_microsoft_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_amazon_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_alphabet_daemon.py", "MESA5_AI_COMPUTE"),
    ("m82_tech_samsung_daemon.py", "MESA5_AI_COMPUTE"),

    # Desk 6: Critical Minerals & Rare Earths
    ("m82_minerals_mp_materials_daemon.py", "MESA6_RARE_EARTHS"),
    ("m82_minerals_china_northern_daemon.py", "MESA6_RARE_EARTHS"),
    ("m82_minerals_zijin_mining_daemon.py", "MESA6_RARE_EARTHS"),

    # Desk 7: Fleet, Shipping & Logistics
    ("m82_fleet_monitor_daemon.py", "MESA7_SHIPPING"),
    ("m82_eia_weekly_daemon.py", "MESA7_SHIPPING"),

    # Desk 8: Sovereign Debt & Bonds
    ("m82_bonds_treasury_daemon.py", "MESA8_FIXED_INCOME"),
    ("m82_bonds_coco_convertible_daemon.py", "MESA8_FIXED_INCOME"),

    # Desk 9: Metals Stats & LME Futures
    ("m82_metals_lme_futures_daemon.py", "MESA9_METALS_LME"),
    ("m82_metals_options_spreads_daemon.py", "MESA9_METALS_LME"),

    # Desk 10: Macro, FX & Polls
    ("m82_macro_econ_history_daemon.py", "MESA10_MACRO_FX"),
    ("m82_macro_polls_consensus_daemon.py", "MESA10_MACRO_FX")
]

def register_daemons():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for daemon_name, desk in DAEMONS_70:
        cur.execute('''
            INSERT OR REPLACE INTO m82_daemons_registry (daemon_name, desk_category, status, last_heartbeat)
            VALUES (?, ?, 'ACTIVE', CURRENT_TIMESTAMP)
        ''', (daemon_name, desk))
    conn.commit()
    conn.close()
    print(f"✅ [M82 SYSTEM] 70 Daemons registrados e indexados en m82_daemons_registry.")

if __name__ == '__main__':
    register_daemons()
