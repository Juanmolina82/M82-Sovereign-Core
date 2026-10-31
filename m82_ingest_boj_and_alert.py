#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // BOJ HIKES INGESTION & DISPATCHER (NTFY + TELEGRAM)
================================================================================
 Node: Caracas | Topic: MM82 | Telegram ID: -1004335849125
"""

import os
import sqlite3
import json
import requests

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE ENTORNO Y RUTAS
# ------------------------------------------------------------------------------
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
NTFY_TOPIC = "MM82"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1004335849125")

# Metadata del cable M82_MACRO Wire Japón
METADATA = {
    "boj_rate": 1.25,
    "boj_high": "31-year high",
    "neutral_rate_range": "1.1% to 2.5%",
    "usd_jpy": 157.87,
    "dissenters": ["Toichiro Asada", "Ayano Sato"],
    "govt_pressure": "Cabinet Office - examine cumulative effects",
    "next_hike_exp": "Oct or Dec 2026",
    "link_crude": "Middle East high oil",
    "source": "urn:newsml:newswire.refinitiv.com:20260930:nL1N45N00D"
}

CABLE_DATA = {
    "source": "M82_MACRO_REUTERS",
    "category": "MACRO_DESK_BOJ",
    "headline": "BOJ debated faster hikes - 1.25% 31Y high, neutral 1.1-2.5% - USDJPY 157.87 - doves warn soft consumption",
    "gprk_index": 94.0,
    "yield_10y_delta": 0.03,
    "oil_spread_impact": 0.8,
    "risk_score": 8.9,
    "metadata_json": json.dumps(METADATA)
}

# ------------------------------------------------------------------------------
# BASE DE DATOS (SQLITE LOCK-FREE VIA WAL & TIMEOUT)
# ------------------------------------------------------------------------------
def setup_and_inject():
    """Inyecta el cable en macro_dosier asegurando compatibilidad de concurrencia."""
    print("[*] Conectando a la BD con soporte WAL y timeout=30s...")
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception as e:
        print(f"[!] Warning activando WAL: {e}")

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
    print("✅ BOJ Sep summary inyectado exitosamente en macro_dosier.")

# ------------------------------------------------------------------------------
# DISPATCHER DE ALERTAS (NTFY + TELEGRAM FALLBACK)
# ------------------------------------------------------------------------------
def send_telegram(title, message):
    """Fallback directo a Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"*{title}*\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("  ✓ Alerta entregada exitosamente a Telegram.")
        else:
            print(f"  ❌ Error Telegram ({r.status_code}): {r.text}")
    except Exception as e:
        print(f"  ❌ Excepción enviando a Telegram: {e}")

def dispatch_alerts():
    """Envía notificación Push a ntfy.sh/MM82 con conmutación a Telegram en error 429."""
    title = f"🚨 #M82 BREAKING [{CABLE_DATA['category']}]"
    
    details = (
        f"📌 *{CABLE_DATA['headline']}*\n\n"
        f"⚡ *Risk Score:* {CABLE_DATA['risk_score']}/10 | *GPRK Index:* {CABLE_DATA['gprk_index']}\n"
        f"💴 *BOJ Rate:* 1.25% (31Y High) | *USD/JPY:* 157.87\n"
        f"📈 *Neutral Rate Range:* 1.1% - 2.5% | Espacio para +100-125bps.\n"
        f"⚠️ *Cross Carry Risk:* Fed Hold (65%) vs BOJ Accelerate → Amenaza S&P 7716 / Nasdaq 27071."
    )

    print(f"[*] Despachando alerta a ntfy.sh/{NTFY_TOPIC}...")

    headers = {
        "Title": title.encode('utf-8'),
        "Priority": "high",
        "Tags": "japan,chart_with_upwards_trend,warning"
    }

    try:
        r = requests.post(NTFY_URL, data=details.encode('utf-8'), headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"  ✓ Alerta Push entregada a ntfy.sh/{NTFY_TOPIC}")
        elif r.status_code == 429:
            print("  ⚠️ Límite de cuota 429 en ntfy.sh. Conmutando a Telegram...")
            send_telegram(title, details)
        else:
            print(f"  ⚠️ Respuesta {r.status_code} de ntfy. Conmutando a Telegram...")
            send_telegram(title, details)
    except Exception as e:
        print(f"  ❌ Error de conexión con ntfy.sh ({e}). Redirigiendo a Telegram...")
        send_telegram(title, details)

# ------------------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("================================================================================")
    print(" 🚀 INGESTION & DISPATCHER: BOJ RATE POLICY (NODO CHARALLAVE)")
    print("================================================================================")
    setup_and_inject()
    dispatch_alerts()
    print("================================================================================")
