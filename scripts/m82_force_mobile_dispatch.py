#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Credenciales de Gobernanza M82
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

def send_instant_broadcast():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # Obtener los 3 registros más recientes de macro_dossier
    cur.execute("SELECT id, source, category, headline, m82_tag FROM macro_dossier ORDER BY id DESC LIMIT 3")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("[!] No hay registros recientes en macro_dossier.")
        return

    print(f"🚀 [M82 DISPATCH] Transmitiendo {len(rows)} alertas recientes a Telegram & ntfy...")

    for row in rows:
        rec_id, source, category, headline, tag = row
        
        # Formato de Alerta para Telegram (HTML)
        caption_tg = (
            f"⚡ <b>M82 SOVEREIGN TELEMETRY</b> :: {time.strftime('%H:%M:%S VET')}\n"
            f"───────────────────────────\n"
            f"🏛 <b>SOURCE:</b> {source}\n"
            f"📂 <b>CATEGORY:</b> {category}\n"
            f"📰 <b>HEADLINE:</b> {headline}\n"
            f"🏷 <b>TAG:</b> <code>{tag}</code>\n"
            f"🛡 <b>RISK:</b> Exp 0.22x | VaR 1.68% | Warsh +102.0bps\n"
            f"🔒 <b>GOVERNANCE:</b> BUNKER MODE 0.30x LOCK\n\n"
            f"🏛 @MolinaHoldings | Chairman Juan M. Molina"
        )

        # 1. Enviar a Bot Privado de Telegram
        try:
            url_tg = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
            r_tg = requests.post(url_tg, data={
                'chat_id': CHAT_ID,
                'text': caption_tg,
                'parse_mode': 'HTML'
            }, timeout=10)
            print(f"[*] Telegram Status: {r_tg.status_code}")
        except Exception as e:
            print(f"[!] Telegram Error: {e}")

        # 2. Enviar a ntfy Push
        try:
            ntfy_msg = f"M82 [{category}]: {headline[:110]}..."
            r_ntfy = requests.post(NTFY_URL, data=ntfy_msg.encode('utf-8'), headers={
                "Title": f"M82 ALERT: {source}",
                "Priority": "high",
                "Tags": "chart_with_upwards_trend,shield"
            }, timeout=10)
            print(f"[*] ntfy Status: {r_ntfy.status_code}")
        except Exception as e:
            print(f"[!] ntfy Error: {e}")

        time.sleep(1.5)

if __name__ == "__main__":
    send_instant_broadcast()
