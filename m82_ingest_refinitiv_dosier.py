#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // M82_WIRE DATAINGESTION & DOSIER SYSTEM
================================================================================
 Pipeline de ingesta masiva para procesar métricas de M82_MACRO M82 Wire Workspace:
  - Commodities (Brent, Gasoil, Heating Oil, WTI, NatGas)
  - Shipping & Fletes (Baltic Dry Index, DFRT ME-JAP)
  - Precious Metals & FX (Gold, Silver, EUR/USD, BTC)
  - Breaking News & Technicals de M82 Wire (RTRS)
"""

import os
import sqlite3
import json
import datetime
import subprocess

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Dataset parseado desde la telemetría de M82 Wire (30 de Septiembre de 2026)
M82_WIRE_SNAPSHOT = {
    "timestamp": "2026-09-30T19:42:00-04:00",
    "market_data": [
        {"ticker": "LCOc1", "name": "Brent Crude", "category": "ENERGY_DESK", "latest": 98.03, "ytd_perf": 70.14, "unit": "USD/bbl"},
        {"ticker": "CLc1", "name": "WTI Light Sweet", "category": "ENERGY_DESK", "latest": 89.99, "ytd_perf": 57.47, "unit": "USD/bbl"},
        {"ticker": "LGOc1", "name": "Gasoil Low Sulphur", "category": "ENERGY_DESK", "latest": 1465.00, "ytd_perf": 135.25, "unit": "USD/MT"},
        {"ticker": "HOc1", "name": "Heating Oil", "category": "ENERGY_DESK", "latest": 4.6593, "ytd_perf": 133.75, "unit": "USD/gal"},
        {"ticker": "DFRT-ME-JAP", "name": "Freight Middle East to Japan", "category": "INFRA_DESK", "latest": 1516.30, "ytd_perf": 1516.30, "unit": "INDEX"},
        {"ticker": "BADI", "name": "Baltic Dry Index", "category": "INFRA_DESK", "latest": 3178.00, "ytd_perf": 65.85, "unit": "PTS"},
        {"ticker": "XAU=", "name": "Gold Spot", "category": "MACRO_DESK", "latest": 4154.53, "ytd_perf": -3.67, "unit": "USD/oz"},
        {"ticker": "BTC=", "name": "Bitcoin", "category": "TECH_DESK", "latest": 83590.08, "ytd_perf": -4.64, "unit": "USD"},
        {"ticker": "EUR=", "name": "EUR/USD", "category": "MACRO_DESK", "latest": 1.1330, "ytd_perf": -3.55, "unit": "FX"}
    ],
    "breaking_cables": [
        {
            "category": "GEOPOLITICS_DESK",
            "source": "RTRS",
            "headline": "Oil prices rise by about $1/bbl on stalled US-Iran talks and tight fuel markets",
            "risk_score": 9.8,
            "metadata": {"impact": "HIGH_VOLATILITY", "oil_spread_impact": 1.0}
        },
        {
            "category": "VENEZUELA_DESK",
            "source": "NABEP_M82",
            "headline": "Venezuela PDVSA crude exports rally to 65B barrels capacity with 16c to 54c bond yield surge",
            "risk_score": 9.9,
            "metadata": {"gprk_index": 99.9, "yield_10y_delta": 0.38}
        },
        {
            "category": "MACRO_DESK",
            "source": "RTRS",
            "headline": "Inflation comes in cooler than expected. Diesel could change that",
            "risk_score": 8.5,
            "metadata": {"cpi_core": "0.3%", "impact": "CONTAINED"}
        }
    ]
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Asegurar tabla de indicadores de mercado
    c.execute("""
        CREATE TABLE IF NOT EXISTS m82_refinitiv_market_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE,
            name TEXT,
            category TEXT,
            latest REAL,
            ytd_perf REAL,
            unit TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def execute_ingestion():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()

    print("================================================================================")
    print(" 🚀 INGESTION DE METRICAS M82_WIRE EN M82 DOSIER")
    print("================================================================================")

    # 1. Ingestar métricas de mercado
    count_metrics = 0
    for item in M82_WIRE_SNAPSHOT["market_data"]:
        c.execute("""
            INSERT INTO m82_refinitiv_market_metrics (ticker, name, category, latest, ytd_perf, unit, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ticker) DO UPDATE SET
                latest=excluded.latest,
                ytd_perf=excluded.ytd_perf,
                updated_at=excluded.updated_at
        """, (item["ticker"], item["name"], item["category"], item["latest"], item["ytd_perf"], item["unit"], now))
        count_metrics += 1

    print(f"  ✓ {count_metrics} Métricas financieras/commodities actualizadas en SQLite.")

    # 2. Ingestar cables de noticias y calcular disparadores HUD
    high_risk_event = None
    for cable in M82_WIRE_SNAPSHOT["breaking_cables"]:
        c.execute("""
            INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cable["source"],
            cable["category"],
            cable["headline"],
            cable["metadata"].get("gprk_index", 95.0),
            cable["metadata"].get("yield_10y_delta", 0.0),
            cable["metadata"].get("oil_spread_impact", 0.0),
            cable["risk_score"],
            json.dumps(cable["metadata"])
        ))
        
        if cable["risk_score"] >= 9.5:
            high_risk_event = cable

    conn.commit()
    conn.close()

    print("  ✓ Cables de noticias e inteligencia geopolítica registrados.")

    # 3. Disparar generación automática de Tarjeta HUD si hay evento crítico
    if high_risk_event:
        print("\n ⚠️ EVENTO CRITICO DETECTADO (Risk Score >= 9.5)")
        print(f" ├─> Categoria: {high_risk_event['category']}")
        print(f" └─> Headline:  {high_risk_event['headline']}")
        print("\n 🎨 Ejecutando m82_hud_card_generator_daemon.py...")
        
        try:
            cmd = ["python3", os.path.join(BASE_DIR, "m82_hud_card_generator_daemon.py")]
            subprocess.run(cmd, check=True)
            print("  ✓ Tarjeta #M82 BREAKING STREAM generada dinámicamente.")
        except Exception as e:
            print(f"  ❌ Error al generar tarjeta HUD: {e}")

    print("================================================================================")

if __name__ == "__main__":
    execute_ingestion()
