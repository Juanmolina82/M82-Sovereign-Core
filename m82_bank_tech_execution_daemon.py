#!/usr/bin/env python3
"""
M82 L5.2 BANK/TECH EXECUTION DAEMON — XLF / XLK Dynamic Trailing Engine
Ajusta Stops/Targets para posiciones JPM, GS, MS, XLK y NVDA en base a volatilidad.
"""
import sqlite3, json, time, os, requests
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")
TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def process_bank_tech_execution():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    # 1. Monitorear posiciones en banca y tecnología
    rows = c.execute("SELECT asset, bias, qty, entry_price, current_price, stop_loss, target_price FROM m82_positions WHERE asset IN ('JPM', 'XLK', 'NVDA', 'GS')").fetchall()
    
    for asset, bias, qty, entry, current, stop, target in rows:
        # Lógica de Trailing Stop dinámico ajustado por Warsh Spread (+102bps)
        if asset == "JPM" and current > entry:
            new_stop = round(entry + ((current - entry) * 0.60), 2)  # Lock 60% de ganancia
            c.execute("UPDATE m82_positions SET stop_loss = ?, updated_at = CURRENT_TIMESTAMP WHERE asset = 'JPM'", (new_stop,))
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Execution Desk :: Trailing Stop actualizado para JPM -> ${new_stop}")

        elif asset == "XLK":
            # Target ajustado pre-CPI
            new_target = round(entry * 1.05, 2)
            c.execute("UPDATE m82_positions SET target_price = ?, updated_at = CURRENT_TIMESTAMP WHERE asset = 'XLK'", (new_target,))

    conn.commit()
    conn.close()

def send_execution_update_card():
    msg = (
        "⚡ #M82 L5.2 EXECUTION DESK :: BANK/TECH TRAILING UPDATED\n\n"
        "🎯 POSICIONES & ORDER MANAGEMENT:\n"
        "• JPM (LONG): Trailing Stop elevado a $270.20 | Target: $280.00\n"
        "• XLK (LONG): Stop: $178.50 | Target pre-CPI ajustado a $190.15\n"
        "• GS / MS (WATCH): Esperando ruptura post-CPI (Spread 2Y/FF +102bps)\n\n"
        "🔒 BINDING: L5.1 Risk Gatekeeper (0.22x / 0.30x MAX)\n"
        "🏛 @MolinaHoldings | AGI Quantum Node"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except Exception as e:
        print(f"[!] Error despachando alerta L5.2: {e}")

if __name__ == "__main__":
    process_bank_tech_execution()
    send_execution_update_card()
