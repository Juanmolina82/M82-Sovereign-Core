#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // ANTHROPIC $2T IPO INGESTION & ALERT DISPATCHER
================================================================================
"""

import os
import sqlite3
import json
import requests
import subprocess

# Configuración de Rutas y Canales
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
NTFY_TOPIC = "MM82"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1004335849125")

# Metadata estructurada del Prospecto S-1
METADATA = {
    "valuation_target": "2T USD - largest IPO ever",
    "loss_2y": "50B",
    "commitments": "500B compute leases",
    "prospectus_pages": 300,
    "risk_pages_ratio": "1/3",
    "powerful_ai_def": "exceeds top human experts all domains",
    "self_preserving": ["resist shutdown", "conceal/manipulate info", "coercive/deceptive"],
    "revenue_bigtech_pct": 47,
    "suppliers": ["AMZN", "GOOGL", "AVGO", "MSFT"],
    "source": "urn:newsml:newswire.refinitiv.com:20260930:nL6N45L00I"
}

CABLE_DATA = {
    "source": "M82_MACRO_REUTERS",
    "category": "VC_AI_UNICORNS",
    "headline": "Anthropic $2T IPO: AI May Resist Shutdown to Make It Safer - Paradox Filing",
    "gprk_index": 95.5,
    "yield_10y_delta": 0.0,
    "oil_spread_impact": 0.0,
    "risk_score": 9.2,
    "metadata_json": json.dumps(METADATA)
}

def setup_database(conn):
    """Garantiza la creación de la tabla si no existe."""
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS macro_dosier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            category TEXT,
            headline TEXT,
            gprk_index REAL DEFAULT 0.0,
            yield_10y_delta REAL DEFAULT 0.0,
            oil_spread_impact REAL DEFAULT 0.0,
            risk_score REAL DEFAULT 0.0,
            metadata_json TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def inject_cable():
    """Inyecta la noticia en la base de datos evitando bloqueos."""
    print("[*] Conectando a SQLite con soporte WAL y Timeout=30s...")
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception as e:
        print(f"[!] Warning WAL mode: {e}")

    setup_database(conn)
    c = conn.cursor()

    c.execute("""
        INSERT INTO macro_dosier 
        (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        CABLE_DATA["source"],
        CABLE_DATA["category"],
        CABLE_DATA["headline"],
        CABLE_DATA["gprk_index"],
        CABLE_DATA["yield_10y_delta"],
        CABLE_DATA["oil_spread_impact"],
        CABLE_DATA["risk_score"],
        CABLE_DATA["metadata_json"]
    ))

    conn.commit()
    conn.close()
    print("✅ Anthropic $2T IPO inyectado exitosamente en macro_dosier.")

def send_telegram(title, message):
    """Envia notificación vía Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"*{title}*\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("  ✓ Alerta enviada con éxito a Telegram.")
        else:
            print(f"  ❌ Error Telegram: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"  ❌ Fallo conectando a Telegram: {e}")

def send_alerts():
    """Envía la alerta por ntfy.sh con fallback automático a Telegram."""
    title = f"🚨 #M82 BREAKING [{CABLE_DATA['category']}]"
    
    details = (
        f"📌 *{CABLE_DATA['headline']}*\n\n"
        f"⚡ *Risk Score:* {CABLE_DATA['risk_score']}/10 | *GPRK Index:* {CABLE_DATA['gprk_index']}\n"
        f"💰 *Valuation:* $2T USD | *Loss 2Y:* $50B | *Compute Commitments:* $500B\n"
        f"⚠️ *Paradoja AGI-CORE:* Models may resist shutdown, conceal info & manipulate.\n"
        f"🏢 *BigTech Concentration:* 47% Rev de AMZN, GOOGL, AVGO, MSFT."
    )

    print("[*] Despachando alerta a canales de comunicación...")

    headers = {
        "Title": title.encode('utf-8'),
        "Priority": "urgent",
        "Tags": "warning,robot,chart_with_upwards_trend"
    }

    try:
        r = requests.post(NTFY_URL, data=details.encode('utf-8'), headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"  ✓ Alerta publicada en ntfy.sh/{NTFY_TOPIC}")
        else:
            print(f"  ⚠️ ntfy.sh status {r.status_code}. Reintentando por Telegram...")
            send_telegram(title, details)
    except Exception as e:
        print(f"  ❌ Error ntfy.sh ({e}). Redirigiendo a Telegram...")
        send_telegram(title, details)

if __name__ == "__main__":
    print("================================================================================")
    print(" 🚀 INJECTOR & DISPATCHER: ANTHROPIC $2T IPO (NODO CHARALLAVE)")
    print("================================================================================")
    inject_cable()
    send_alerts()
    print("================================================================================")
