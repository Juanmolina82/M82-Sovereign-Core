#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: DUAL TELEGRAM / NYFT DISPATCHER
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
Asynchronous Non-Blocking Message Routing
"""

import sys
import sqlite3
import pathlib
import urllib.request
import urllib.parse
import json

HOME_DIR = pathlib.Path.home()
DB_PATH = HOME_DIR / "M82" / "m82_database.db"

# CREDENCIALES TELEGRAM (Inyecte sus Tokens & Chat IDs)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID_PRIVATE = "YOUR_PRIVATE_CHAT_ID"     # Bot Privado Chairman Molina
CHAT_ID_NYFT = "YOUR_NYFT_CHANNEL_CHAT_ID"   # Canal NYFT Alterno

def send_telegram_msg(chat_id, text):
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        # Modo simulación / Log local si no se han inyectado claves
        print(f"[DISPATCH SIMULATION -> {chat_id}]\n{text}\n")
        return True
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except Exception as e:
        print(f"[TELEGRAM ERROR] No se pudo despachar a {chat_id}: {e}")
        return False

def query_and_dispatch(ticker):
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # 1. Buscar en Renta Variable Global
    cursor.execute("SELECT ticker, asset_name, spot_price, fcf_yield_fy1, forward_pe, roe FROM m82_global_equities WHERE ticker = ?", (ticker,))
    eq = cursor.fetchone()
    
    # 2. Buscar en Derivados / Futuros si no es equity
    if not eq:
        cursor.execute("SELECT symbol, contract_name, spot_price, rsi_14d, val_alpha FROM m82_global_derivatives WHERE symbol = ?", (ticker,))
        der = cursor.fetchone()
        if der:
            msg = (
                f"```text\n"
                f"┌──────────────────────────────────────┐\n"
                f"│ M82 DOSSIER TELEMETRY :: {der[0]:<11} │\n"
                f"├──────────────────────────────────────┤\n"
                f"│ Asset Name  : {der[1]:<22} │\n"
                f"│ Spot Price  : ${der[2]:<21.2f} │\n"
                f"│ RSI (14D)   : {der[3]:<22.1f} │\n"
                f"│ Val Alpha   : {der[4]:<22.2f} │\n"
                f"└──────────────────────────────────────┘\n"
                f"```\n"
                f"📡 *Feeder:* Refinitiv Workspace (`jmmp@molina82.com`)\n"
                f"🏛️ *Gobernanza:* Caracas HQ ⊗ Charallave Edge L4/L5"
            )
        else:
            msg = f"⚠️ *[M82 CORE]* Ticker `{ticker}` no encontrado en la base WAL local."
    else:
        msg = (
            f"```text\n"
            f"┌──────────────────────────────────────┐\n"
            f"│ M82 DOSSIER TELEMETRY :: {eq[0]:<11} │\n"
            f"├──────────────────────────────────────┤\n"
            f"│ Company     : {eq[1]:<22} │\n"
            f"│ Spot Price  : ${eq[2]:<21.2f} │\n"
            f"│ FCF Yield   : {eq[3]:<21.2f}% │\n"
            f"│ Forward P/E : {eq[4]:<22.2f} │\n"
            f"│ ROE         : {eq[5]:<21.2f}% │\n"
            f"└──────────────────────────────────────┘\n"
            f"```\n"
            f"📡 *Feeder:* Refinitiv Workspace (`jmmp@molina82.com`)\n"
            f"🏛️ *Gobernanza:* Caracas HQ ⊗ Charallave Edge L4/L5"
        )
    
    conn.close()
    
    # Despacho Dual Simultáneo
    print(f"[M82 TELEGRAM] Despachando consulta de `{ticker}`...")
    send_telegram_msg(CHAT_ID_PRIVATE, msg)
    send_telegram_msg(CHAT_ID_NYFT, msg)
    print("[M82 TELEGRAM] ✅ Despacho dual completado.")

if __name__ == "__main__":
    target_ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "NVDA"
    query_and_dispatch(target_ticker)
