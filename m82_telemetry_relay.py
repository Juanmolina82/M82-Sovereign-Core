#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

# Credenciales Inyectadas
TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def send_telegram(text_msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text_msg,
            "parse_mode": "Markdown"
        }
        r = requests.post(url, data=payload, timeout=10)
        print(f"[*] Telegram Dispatch: HTTP {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"[!] Telegram Exception: {e}")
        return False

def send_ntfy(msg):
    try:
        headers = {
            "Priority": "high",
            "Tags": "warning,chart_with_upwards_trend"
        }
        r = requests.post(NTFY_URL, data=msg.encode('utf-8'), headers=headers, timeout=10)
        print(f"[*] ntfy Dispatch: HTTP {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"[!] ntfy Exception: {e}")
        return False

def dispatch_latest_signals():
    if not os.path.exists(DB_PATH):
        print("[!] BBDD m82_database.db no encontrada.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA busy_timeout=120000;")
        cur = conn.cursor()

        # Extraer los últimos registros para transmisión
        cur.execute("SELECT id, m82_tag, risk_score, alpha_score, headline FROM macro_dossier ORDER BY id DESC LIMIT 1;")
        row = cur.fetchone()
        conn.close()

        if row:
            rec_id, tag, risk, alpha, headline = row
            now = time.strftime("%H:%M:%S ET")
            
            tg_msg = (
                f"⚡ *#M82 TELEMETRIA VIVA MULTICHANNEL* :: {now}\n"
                f"───────────────────────────\n"
                f"🏛 *TAG:* `{tag}`\n"
                f"📊 *ALPHA:* `{alpha}` | *RISK:* `{risk}`\n"
                f"📰 *HEADLINE:* {headline}\n"
                f"🛡 *GOVERNANCE:* Exp 0.22x/0.30x LOCK | VaR 1.68% | Warsh +102bps\n"
                f"🔒 *CUSTODIA PASIVA EN NODO CHARALLAVE L4/L5 EDGE*\n\n"
                f"🏛 @MolinaHoldings LLC | AGI Quantum Engine"
            )

            ntfy_msg = f"M82 LIVE [{now}] Tag: {tag} | Alpha: {alpha} | Risk: {risk}"

            send_telegram(tg_msg)
            send_ntfy(ntfy_msg)

    except Exception as e:
        print(f"[!] DB Error: {e}")

if __name__ == "__main__":
    print("🚀 DISPARANDO PRUEBA MULTI-CANAL...")
    dispatch_latest_signals()
