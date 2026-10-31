#!/usr/bin/env python3
import sqlite3, os, time, requests
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")
TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

def loop():
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
            card = (
                f"🏛️ M82 TELEMETRIA VIVA 60S :: {now}\n"
                f"───────────────────────────\n"
                f"⚡ MESA DINERO: NFLX $12.87B | SPACEX $14.6B\n"
                f"🛢️ MEREY 16: $93.15 ITM PADD3 | VENZ 2027 $50.61\n"
                f"🛡️ RISK: Exp 0.22x / 0.30x LOCK | VaR 1.68%\n"
                f"🔒 BUNKER PASIVO — WAL CLEAN 0/0/0"
            )
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": card}, timeout=10)
            requests.post(NTFY_URL, data=f"M82 STREAM [{now}] Exp 0.22x VaR 1.68%".encode('utf-8'), timeout=10)
        except Exception as e:
            print(f"[!] Loop error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    loop()
