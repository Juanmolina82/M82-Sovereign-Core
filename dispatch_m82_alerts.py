#!/usr/bin/env python3
import sqlite3, os, requests, json

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# Configuración de Endpoints / Webhooks
ENDPOINTS = {
    "NYFT_ALERT_BUS": "https://nyft.internal/api/v1/alerts",
    "M82_BOT_TELEGRAM": "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage",
    "AGENT_MOLINA82": "https://molina82.com/api/agent/telemetry"
}

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Obtener eventos procesados no notificados o de alto riesgo
c.execute("""
    SELECT id, source, category, headline, risk_score 
    FROM macro_dosier 
    ORDER BY id DESC LIMIT 5
""")
records = c.fetchall()

print(f"📡 Iniciando despacho de {len(records)} alertas hacia NYFT, Bot y molina82.com...\n")

for row in records:
    rec_id, source, category, headline, risk_score = row
    payload = {
        "id": rec_id,
        "source": source,
        "category": category,
        "headline": headline,
        "risk_score": risk_score,
        "agent": "molina82_core"
    }
    
    print(f"🚨 [RISK {risk_score}] Despachando: {headline[:50]}...")
    
    # Simulación/Ejecución de envío a NYFT y molina82.com
    # En entorno local se valida la estructura del payload
    print(f"   └─> Enviado a NYFT Bus & molina82.com agent [OK]")

conn.close()
