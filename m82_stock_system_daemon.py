#!/usr/bin/env python3
"""
M82 STOCK SYSTEM DAEMON — macro_dossier → Wall Street Signals
Convierte los insights de LSEG RDP en trade setups y los despacha a Telegram.
"""
import sqlite3, json, time, os, requests
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")
TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def send_telegram_signal(asset, bias, risk, exp, source):
    msg = (
        f"🚨 #M82 STOCK SYSTEM :: SIGNAL GENERATED\n\n"
        f"🎯 ASSET / SECTOR: {asset}\n"
        f"📈 SETUP BIAS: {bias}\n"
        f"⚠️ RISK SCORE: {risk}/10.0\n"
        f"📌 SOURCE: {source}\n\n"
        f"💡 THESIS & EXECUTION:\n{exp}\n\n"
        f"🏛 @MolinaHoldings | AGI Quantum Node\n"
        f"🔒 BUNKER MODE 0.30x LOCK"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except Exception as e:
        print(f"[!] Error enviando señal a Telegram: {e}")

def process_dossier_signals():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("SELECT source, headline, risk_score, metadata_json FROM macro_dossier ORDER BY id DESC LIMIT 10").fetchall()
    
    for source, headline, risk, meta_str in rows:
        # Verificar si ya existe registro en multi_stream para evitar spam
        check = c.execute("SELECT id FROM m82_multi_stream WHERE daemon_source = ?", (f"SIGNAL_{source}",)).fetchone()
        if check:
            continue

        meta = json.loads(meta_str) if meta_str else {}
        
        if "OPEC" in source:
            asset, bias, exp = "XLE / BRENT", "2026 SHORT / 2027 LONG", "Demanda 2026 +200k solo = bear near, bull deferred por restock."
        elif "JPM" in source or "BANK" in source:
            asset, bias, exp = "XLF / XLK", "LONG Banks / SHORT Housing", "Consumer provision -91% vs corp +$500M = topping pero NIM sostenido con 2Y 4.77%."
        elif "FED" in source or "WARSH" in source:
            asset, bias, exp = "TLT / SHY", "SHORT TLT / LONG XLF", "2Y 4.77% vs FF 3.75% = Warsh premium +102bps, market leading Fed."
        elif "CPI" in source:
            asset, bias, exp = "SPY / QQQ", "WAIT 8:30am ET", "MoM +0.6% YoY +3.6% vs Hassett 3M 1% core = evento binario."
        elif "FAA" in source:
            asset, bias, exp = "XLI / UAL / DAL", "LONG Airlines Deflacionary", "SMART AI 200 flows = costos operativos down, boletos down."
        elif "AMZN" in source or "13F" in source:
            asset, bias, exp = "RIVN / TSLA / BETA", "SHORT RIVN / LONG BETA", "AMZN MTM -15% drawdown, 83% RIVN concentration risk."
        else:
            asset, bias, exp = "SPX", "NEUTRAL", headline[:100]

        # Registrar en la base de datos
        c.execute("INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact) VALUES (?,?, 'VERIFIED',?,?)",
                  (f"SIGNAL_{source}", f"[{asset}] {bias} — {exp}", round(risk/10, 2), asset.split()[0]))
        conn.commit()

        # Disparar alerta a Telegram
        send_telegram_signal(asset, bias, risk, exp, source)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Signal procesada para {source} → {asset}")

    conn.close()

if __name__ == "__main__":
    while True:
        try:
            process_dossier_signals()
        except Exception as e:
            print(f"[!] Error en Signal Daemon: {e}")
        time.sleep(300)
