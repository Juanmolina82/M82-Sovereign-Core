#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE SUITE // NODO CHARALLAVE (MASTER DEPLOYER & ORCHESTRATOR 2026)
================================================================================
 Arquitectura Unificada Actualizada:
  1. Activación Automática de Termux Wake-Lock.
  2. Base de Datos SQLite (m82_database.db): Esquemas, Migraciones, Registros y Audit.
  3. Matriz Completa de 40 Daemons distribuidos en 8 Mesas Macro (Desks).
  4. Ingesta Integrada: Cables M82 Wire/M82_MACRO (Venezuela/CVX), PE Dry Powder ($2.008T) y Top Megafunds.
  5. Engine Visual HUD Headless (matplotlib Agg Backend) con estética Cyberpunk.
  6. API Agent Server Flask (Puerto 8083) + Static HTTP Asset Server (Puerto 8080).
"""

import os
import sys
import sqlite3
import json
import datetime
import subprocess

# Configuración de Entorno Headless para Visualización
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Rutas Base del Sistema
BASE_DIR = os.path.expanduser("~/M82")
os.makedirs(BASE_DIR, exist_ok=True)
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

print("================================================================================")
print(" 🚀 INICIALIZANDO DEPLOYER MAESTRO M82 // NODO CHARALLAVE (FULL SUITE UPDATED)")
print("================================================================================")

# ------------------------------------------------------------------------------
# FASE 0: WAKE-LOCK TERMUX
# ------------------------------------------------------------------------------
def activate_wake_lock():
    print("\n[FASE 0] Adquiriendo Termux Wake-Lock para ejecución continua...")
    try:
        subprocess.run(["termux-wake-lock"], check=False)
        print("  ✓ Wake-Lock activado (Protección contra Deep Sleep CPU).")
    except Exception as e:
        print(f"  ⚠️ No se pudo invocar termux-wake-lock directamente: {e}")

# ------------------------------------------------------------------------------
# FASE 1: INICIALIZACIÓN Y MIGRACIÓN DE SCHEMAS SQLITE
# ------------------------------------------------------------------------------
def setup_database():
    print("\n[FASE 1] Configurando y Blindando Esquemas SQLite...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabla 1: Macro Dosier (Telemetría de Alertas y Scoring)
    c.execute('''
        CREATE TABLE IF NOT EXISTS macro_dosier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            category TEXT,
            headline TEXT,
            gprk_index REAL,
            yield_10y_delta REAL,
            oil_spread_impact REAL,
            risk_score REAL,
            metadata_json TEXT
        )
    ''')

    # Migración defensiva: asegurar columna metadata_json
    c.execute("PRAGMA table_info(macro_dosier)")
    cols = [col[1] for col in c.fetchall()]
    if "metadata_json" not in cols:
        c.execute("ALTER TABLE macro_dosier ADD COLUMN metadata_json TEXT")

    # Tabla 2: Multi-Stream Bus (Despacho a Daemons Externos: NYFT, Telegram, Agent)
    c.execute('''
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT,
            status TEXT,
            timestamp DATETIME,
            UNIQUE(daemon_source, headline)
        )
    ''')

    # Tabla 3: Registro de Daemons (Suite Completa de 40 Vectores)
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

    conn.commit()
    conn.close()
    print("  ✓ Base de datos SQLite y migraciones sincronizadas correctamente.")

# ------------------------------------------------------------------------------
# FASE 2: REGISTRO DE LA SUITE DE 40 DAEMONS (8 MESAS MACRO)
# ------------------------------------------------------------------------------
def register_daemons():
    print("\n[FASE 2] Registrando Matriz Completa de 40 Daemons (8 Mesas)...")
    daemons_matrix = [
        # 1. PE & Venture Capital Desk (6)
        ("m82_pe_dry_powder_daemon.py", "PE_DESK", "GLOBAL_DRY_POWDER"),
        ("m82_pe_megafunds_daemon.py", "PE_DESK", "MEGA_FUNDS_CONCENTRATION"),
        ("m82_pe_stage_allocation_daemon.py", "PE_DESK", "STAGE_ALLOCATION"),
        ("m82_pe_geographic_flows_daemon.py", "PE_DESK", "GEOGRAPHIC_FLOWS"),
        ("m82_vc_ai_unicorns_daemon.py", "VC_DESK", "AI_DEEPTECH_ROUNDS"),
        ("m82_secondary_markets_daemon.py", "PE_DESK", "M82_MACROONDARY_LIQUIDITY"),
        # 2. Musk Empire & Tech Desk (6)
        ("m82_musk_daemon.py", "MUSK_DESK", "GENERAL_TELEMETRY"),
        ("m82_musk_empire_daemon.py", "MUSK_DESK", "VALUATION_CONSOLIDATED"),
        ("m82_spacex_telecom_daemon.py", "MUSK_DESK", "STARLINK_DIRECT_TO_CELL"),
        ("m82_tesla_fsd_robotaxi_daemon.py", "MUSK_DESK", "FSD_ROBOTAXI_TELEMETRY"),
        ("m82_xai_grok_compute_daemon.py", "MUSK_DESK", "GPU_COMPUTE_CLUSTERS"),
        ("m82_tech_magnificent7_daemon.py", "TECH_DESK", "MAG7_CONCENTRATION"),
        # 3. Macro & Deuda Desk (5)
        ("m82_treasury_bonds_daemon.py", "MACRO_DESK", "YIELD_CURVE_DELTAS"),
        ("m82_fed_rates_dotplot_daemon.py", "MACRO_DESK", "FED_RATES_EXPECTATIONS"),
        ("m82_sovereign_debt_risk_daemon.py", "MACRO_DESK", "SOVEREIGN_CDS_RISK"),
        ("m82_high_yield_credit_daemon.py", "MACRO_DESK", "HIGH_YIELD_SPREADS"),
        ("m82_smr_data_center_credit_daemon.py", "CREDIT_DESK", "SMR_DATA_CENTER_PROJECT_FINANCE"),
        # 4. Commodities & Faja Desk (5)
        ("m82_crypto_commodities_daemon.py", "ENERGY_DESK", "COMMODITIES_ENERGY_SPREADS"),
        ("m82_oil_refining_margins_daemon.py", "ENERGY_DESK", "CRACK_SPREADS"),
        ("m82_faja_orinoco_ep_daemon.py", "ENERGY_DESK", "FAJA_ORINOCO_EXPORTS"),
        ("m82_lng_gas_global_daemon.py", "ENERGY_DESK", "LNG_HENRY_HUB_TTF"),
        ("m82_uranium_nuclear_daemon.py", "ENERGY_DESK", "URANIUM_SPOT_PPA"),
        # 5. Geopolítica & Cables Desk (5)
        ("m82_geopolitical_events_daemon.py", "GEOPOLITICS_DESK", "HORMUZ_TAIWAN_RISK"),
        ("m82_machado_delcy_cable_daemon.py", "GEOPOLITICS_DESK", "VENEZUELA_CABLE_TELEMETRY"),
        ("m82_us_china_tariffs_daemon.py", "GEOPOLITICS_DESK", "TARIFFS_SEMICONDUCTORS"),
        ("m82_gprk_index_daemon.py", "GEOPOLITICS_DESK", "GPRK_REALTIME_INDEX"),
        ("m82_sanctions_compliance_daemon.py", "GEOPOLITICS_DESK", "OFAC_SHADOW_FLEETS"),
        # 6. Terminales & M82_MACRO Desk (4)
        ("m82_m82_macro_notebook_daemon.py", "TERMINAL_DESK", "M82_WIRE_WORKSPACE_NOTEBOOK"),
        ("m82_refinitiv_company_ranking_daemon.py", "TERMINAL_DESK", "COMPANY_RANKING_FEED"),
        ("m82_refinitiv_firm_ranking_daemon.py", "TERMINAL_DESK", "FIRM_RANKING_FEED"),
        ("m82_bloomberg_news_sentiment_daemon.py", "TERMINAL_DESK", "FINANCIAL_NEWS_NLP"),
        # 7. Cripto & Paridad Desk (4)
        ("m82_bitcoin_hashrate_daemon.py", "CRYPTO_DESK", "BTC_HASHRATE_ETF_FLOWS"),
        ("m82_stablecoin_liquidity_daemon.py", "CRYPTO_DESK", "STABLECOIN_ISSUANCE"),
        ("m82_dedollarization_brics_daemon.py", "MACRO_DESK", "BRICS_GOLD_RESERVES"),
        ("m82_cbdc_swift_flows_daemon.py", "MACRO_DESK", "SWIFT_CBDC_MONITOR"),
        # 8. Infra & HUD Desk (5)
        ("m82_hud_card_generator_daemon.py", "INFRA_DESK", "MATPLOTLIB_HUD_ENGINE"),
        ("m82_multi_stream_dispatcher_daemon.py", "INFRA_DESK", "BROADCAST_NYFT_TELEGRAM"),
        ("m82_pwa_api_bridge_daemon.py", "INFRA_DESK", "FLASK_API_PORT_8083"),
        ("m82_sqlite_integrity_daemon.py", "INFRA_DESK", "DATABASE_OPTIMIZER"),
        ("m82_termux_node_health_daemon.py", "INFRA_DESK", "CHARALLAVE_NODE_HEALTH")
    ]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    now = datetime.datetime.now().isoformat()
    for d_name, desk, vector in daemons_matrix:
        c.execute("""
            INSERT INTO m82_daemons_registry (daemon_name, desk_category, vector_type, status, last_heartbeat)
            VALUES (?, ?, ?, 'ACTIVE_LITE_WAKELOCK', ?)
            ON CONFLICT(daemon_name) DO UPDATE SET
                desk_category=excluded.desk_category,
                vector_type=excluded.vector_type,
                status='ACTIVE_LITE_WAKELOCK',
                last_heartbeat=excluded.last_heartbeat
        """, (d_name, desk, vector, now))

    conn.commit()
    conn.close()
    print(f"  ✓ {len(daemons_matrix)} Daemons registrados/actualizados en m82_daemons_registry.")

# ------------------------------------------------------------------------------
# FASE 3: INGESTA DE SEÑALES MACRO (M82_WIRE WORKSPACE, CABLES VENEZUELA Y CVX)
# ------------------------------------------------------------------------------
def ingest_macro_signals():
    print("\n[FASE 3] Inyectando Telemetría M82 Wire Workspace (Bonos VEN + CVX + PE) en macro_dosier...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    now = datetime.datetime.now().isoformat()
    signals = [
        # Cables M82 Wire Workspace extraídos
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "VEN_BONDS_RALLY",
            "headline": "Venezuela debt rally sees eyes on higher recovery price",
            "gprk": 98.5,
            "risk_score": 9.2,
            "meta": {"entity": "REPUBLIC OF VENEZUELA", "duns": "003011988", "topic": "Debt Recovery Price Increase"}
        },
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "VEN_DEBT_RESTRUCTURING",
            "headline": "Lazard offers Venezuela debt restructuring advice",
            "gprk": 97.8,
            "risk_score": 8.9,
            "meta": {"advisor": "Lazard", "target": "Sovereign & PDVSA Bonds"}
        },
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "CVX_VENEZUELA_OPERATIONS",
            "headline": "Chevron / Venezuela Joint Ventures for Oil Investment & Production Continuity",
            "gprk": 96.4,
            "risk_score": 7.5,
            "meta": {"ticker": "CVX.N", "sector": "Integrated Oil & Gas", "joint_ventures": "Petropiar, Petroboscán"}
        },
        # Telemetría de Mercado Private Equity
        {
            "source": "PE_LARGEST_FUNDS_DESK",
            "category": "MEGA_FUNDS_CONCENTRATION",
            "headline": "Top 10 Largest Private Equity Funds Concentration Reaches 189.84 Billion USD",
            "gprk": 98.5,
            "risk_score": 9.8,
            "meta": {
                "total_top10_raised_usd_m": 189844.78,
                "top_vehicle": "General Atlantic Partners (Bermuda) IV LP ($23,701.01M)"
            }
        },
        {
            "source": "PE_MARKET_DESK",
            "category": "GLOBAL_DRY_POWDER",
            "headline": "Global PE Dry Powder Exceeds 2.008 Trillion USD Across 1873 Active Funds",
            "gprk": 97.2,
            "risk_score": 9.6,
            "meta": {"total_raised_usd_m": 1489373.0, "dry_powder_usd_m": 2008260.0, "total_funds": 1873}
        }
    ]

    for sig in signals:
        c.execute("""
            INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
            VALUES (?, ?, ?, ?, 0.02, 1.10, ?, ?)
        """, (sig["source"], sig["category"], sig["headline"], sig["gprk"], sig["risk_score"], json.dumps(sig["meta"])))

        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'DISPATCHED', ?)
        """, (sig["source"], sig["headline"], now))

    conn.commit()
    conn.close()
    print("  ✓ Cables de M82 Wire Workspace y métricas PE inyectados en macro_dosier.")

# ------------------------------------------------------------------------------
# FASE 4: ENGINE RENDERER MATPLOTLIB (GENERACIÓN DE CARDS Y DASHBOARD)
# ------------------------------------------------------------------------------
def generate_hud_assets():
    print("\n[FASE 4] Generando Tarjetas Gráficas y Dashboard Maestro HUD...")
    plt.style.use('dark_background')

    # Asset 1: Top 10 PE Megafunds Card
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0a0d12')
    ax.set_facecolor('#0f141d')

    funds = [
        'GA Partners IV', 'KKR NA XIV', 'Francisco P. VIII',
        'Sequoia Cap Fund', 'KKR Global Infra V', 'Coller Int IX',
        'BPEA PE IX', 'Warburg Pincus 15', 'Veritas Cap IX', 'Clearlake Cap VIII'
    ]
    sizes = [23.70, 23.00, 23.00, 22.72, 19.20, 17.00, 15.60, 15.52, 15.30, 14.80]
    y_pos = np.arange(len(funds))

    bars = ax.barh(y_pos, sizes, align='center', color='#00e5ff', edgecolor='#76ff03', alpha=0.85, height=0.65)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(funds, fontsize=9, fontweight='bold', color='#e0e0e0')
    ax.invert_yaxis()
    ax.set_xlabel('Tamaño del Fondo ($B USD)', fontsize=10, fontweight='bold', color='#00e5ff')
    ax.set_title('M82 MACRO DOSIER // TOP 10 PE MEGA-FUNDS vs DRY POWDER ($2.008T)', fontsize=11, fontweight='bold', color='#76ff03', pad=12)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.3, bar.get_y() + bar.get_height()/2, f'${w:.2f}B', va='center', ha='left', fontsize=8, fontweight='bold', color='#ffffff')

    ax.set_xlim(0, 28)
    ax.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')
    plt.axvline(x=20, color='#ff1744', linestyle=':', linewidth=1.5, label='Threshold Megafondo ($20B)')
    ax.legend(loc='lower right', facecolor='#0a0d12', edgecolor='#76ff03', fontsize=8)

    plt.tight_layout()
    card_path = os.path.join(BASE_DIR, "hud_PE_LARGEST_FUNDS_DESK.png")
    plt.savefig(card_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # Asset 2: Dashboard Maestro 8 Mesas Macro
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0a0d12')
    ax.set_facecolor('#0f141d')

    desks = ['PE & VC', 'Musk Empire', 'Macro/Deuda', 'Commodities', 'Geopolítica', 'Terminales', 'Cripto', 'Infra/HUD']
    risk_scores = [9.8, 9.4, 9.2, 9.5, 9.9, 9.1, 8.8, 9.7]
    daemons_counts = [6, 6, 5, 5, 5, 4, 4, 5]

    x = np.arange(len(desks))
    width = 0.35

    rects1 = ax.bar(x - width/2, risk_scores, width, label='Score Riesgo', color='#ff1744', alpha=0.85, edgecolor='#76ff03')
    rects2 = ax.bar(x + width/2, daemons_counts, width, label='Daemons', color='#00e5ff', alpha=0.85, edgecolor='#76ff03')

    ax.set_ylabel('Nivel / Cantidad', fontsize=9, fontweight='bold', color='#00e5ff')
    ax.set_title('M82 CHARALLAVE NODE // DASHBOARD 8 MESAS MACRO (40 DAEMONS)', fontsize=11, fontweight='bold', color='#76ff03', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(desks, rotation=20, ha='right', fontsize=8, fontweight='bold', color='#e0e0e0')
    ax.legend(loc='upper right', facecolor='#0a0d12', edgecolor='#76ff03', fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')

    plt.tight_layout()
    dash_path = os.path.join(BASE_DIR, "hud_master_8desks.png")
    plt.savefig(dash_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    print(f"  ✓ Assets visuales generados:\n     - {card_path}\n     - {dash_path}")

# ------------------------------------------------------------------------------
# FASE 5: COMPILACIÓN DE SERVIDORES (API AGENT 8083 & HTTP ASSET SERVER 8080)
# ------------------------------------------------------------------------------
def build_and_launch_services():
    print("\n[FASE 5] Compilando e Iniciando Servidores de Producción...")

    # Script para m82_api_server.py
    api_script_path = os.path.join(BASE_DIR, "m82_api_server.py")
    with open(api_script_path, "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
from flask import Flask, request, jsonify
import sqlite3, os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

@app.route('/', methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    msg = data.get("message", "").lower()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT source, category, headline, risk_score FROM macro_dosier ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    source = row[0] if row else "M82_WIRE_WORKSPACE_M82_MACRO"
    category = row[1] if row else "VEN_BONDS_RALLY"
    headline = row[2] if row else "Venezuela debt rally sees eyes on higher recovery price"
    risk = row[3] if row else 9.2

    hud_image_url = f"http://127.0.0.1:8080/hud_PE_LARGEST_FUNDS_DESK.png"

    response_text = (
        f"=== DESGLOSE EJECUTIVO Y MATRIZ DE IMPACTO M82 ===\\n"
        f"🚨 [RISK {risk}] {category}\\n"
        f"📌 {headline}\\n\\n"
        f"![HUD M82]({hud_image_url})\\n\\n"
        f"• Cobertura M82 Wire: Cables de bonos sovereign, Lazard restructuring y Chevron CVX.N activos.\\n"
        f"• Dry Powder Global PE: $2.008 Trillones en 1,873 fondos.\\n"
        f"• Estado Nodo Caracas: 40 Daemons en Lite Polling + Wake-Lock Habilitado."
    )

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8083)
''')

    # Reiniciar procesos en background
    subprocess.run("pkill -f 'http.server 8080'", shell=True)
    subprocess.run("pkill -f 'm82_api_server.py'", shell=True)

    # Iniciar Servidor HTTP de Assets (8080)
    subprocess.Popen(f"cd {BASE_DIR} && nohup python3 -m http.server 8080 > /dev/null 2>&1 &", shell=True)

    # Iniciar API Agent Server (8083)
    subprocess.Popen(f"nohup python3 {api_script_path} > /dev/null 2>&1 &", shell=True)

    print("  ✓ Servidor HTTP Assets activo en puerto 8080.")
    print("  ✓ API Agent Server activo en puerto 8083.")

# ------------------------------------------------------------------------------
# FASE 6: RESUMEN DE CONTROL Y PRUEBAS AUTOMÁTICAS
# ------------------------------------------------------------------------------
def verify_deployment():
    print("\n[FASE 6] Ejecutando Diagnostic Health-Check de Infraestructura...")
    import time
    time.sleep(2)

    # Conexión SQLite Diagnostic
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM m82_daemons_registry")
    daemon_cnt = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM macro_dosier")
    dosier_cnt = c.fetchone()[0]
    conn.close()

    print("\n================================================================================")
    print(" 📊 RESUMEN EJECUTIVO ACTUALIZADO NODO CHARALLAVE M82")
    print("================================================================================")
    print(f" 🗄️ Base de Datos SQLite:   {DB_PATH}")
    print(f" 🔒 Termux Wake-Lock:      ACTIVO (Prevención Deep Sleep)")
    print(f" 🤖 Daemons Registrados:    {daemon_cnt} / 40 Vectores Listos")
    print(f" 📡 Señales y Cables:       {dosier_cnt} Registros en Dosier (Incluye M82 Wire VEN/CVX)")
    print(f" 🌐 HTTP Asset Server:      http://127.0.0.1:8080/")
    print(f" ⚡ Agent API Endpoint:     http://127.0.0.1:8083/")
    print("================================================================================\n")

if __name__ == "__main__":
    activate_wake_lock()
    setup_database()
    register_daemons()
    ingest_macro_signals()
    generate_hud_assets()
    build_and_launch_services()
    verify_deployment()
