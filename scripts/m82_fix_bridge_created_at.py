#!/usr/bin/env python3
# M82 HOTFIX DDL & REFINITIV REALTIME BRIDGE RE-DEPLOYMENT
import os, sys, time, sqlite3, requests
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
USER_ID = "jmmp@molina82.com"

# 1. Asegurar DDL de la columna created_at
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=30000;")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE macro_dossier ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;")
    print("🟢 Columna 'created_at' agregada exitosamente a macro_dossier.")
except sqlite3.OperationalError:
    print("ℹ️ La columna 'created_at' ya existe en el esquema.")

conn.commit()
conn.close()

# 2. Re-escribir script del puente con consulta tolerante a fallos
bridge_code = '''#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
USER_ID = "jmmp@molina82.com"

def dispatch_live_feed():
    if not os.path.exists(DB_PATH):
        print(f"[!] BBDD no encontrada en {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, source, category, headline, risk_score, m82_tag, version 
        FROM macro_dossier ORDER BY id DESC LIMIT 1
    """)
    row = cur.fetchone()
    
    cur.execute("SELECT COUNT(*) FROM macro_dossier;")
    total_records = cur.fetchone()[0]
    conn.close()

    if not row:
        print("[!] No hay registros para despachar.")
        return

    rec_id, source, category, headline, risk, tag, version = row
    now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    caption_tg = (
        f"⚡ <b>M82 SOVEREIGN TELEMETRY</b> :: {now_utc}\\n"
        f"───────────────────────────\\n"
        f"👤 <b>AUTHENTICATED USER:</b> <code>{USER_ID}</code>\\n"
        f"🏛 <b>SOURCE:</b> {source}\\n"
        f"📂 <b>CATEGORY:</b> {category}\\n"
        f"🏷 <b>VERSION & TAG:</b> {version} | <code>{tag}</code>\\n"
        f"📰 <b>HEADLINE:</b> {headline}\\n\\n"
        f"📊 <b>TOTAL DOSSIER RECORDS:</b> {total_records}\\n"
        f"🛡 <b>RISK LOCK:</b> Exp 0.22x | VaR 1.68% | Warsh +102.0bps\\n"
        f"🔒 <b>GOVERNANCE:</b> BUNKER MODE 0.30x LOCK\\n\\n"
        f"🏛 @MolinaHoldings | Chairman Juan M. Molina"
    )

    # 1. Enviar a Telegram Bot Privado
    try:
        url_tg = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        r_tg = requests.post(url_tg, data={
            'chat_id': CHAT_ID,
            'text': caption_tg,
            'parse_mode': 'HTML'
        }, timeout=10)
        print(f"[*] Telegram Dispatch Status: {r_tg.status_code}")
    except Exception as e:
        print(f"[!] Error Telegram: {e}")

    # 2. Enviar a ntfy Push
    try:
        ntfy_msg = f"[{USER_ID}] M82 WIRE ({version}): {headline[:100]}... (Total: {total_records})"
        r_ntfy = requests.post(NTFY_URL, data=ntfy_msg.encode('utf-8'), headers={
            "Title": f"M82 WIRE: {source}",
            "Priority": "high",
            "Tags": "chart_with_upwards_trend,shield"
        }, timeout=10)
        print(f"[*] ntfy Push Dispatch Status: {r_ntfy.status_code}")
    except Exception as e:
        print(f"[!] Error ntfy: {e}")

def main_loop():
    print(f"🚀 M82 STREAMING BRIDGE ONLINE :: USER {USER_ID}")
    print("🟢 BUCLE CONTINUO ACTIVADO (DISPAROS CADA 60S)")
    while True:
        try:
            dispatch_live_feed()
        except Exception as err:
            print(f"[!] Error en ciclo de disparo: {err}")
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
'''

with open(os.path.expanduser("~/M82/scripts/m82_refinitiv_realtime_bridge.py"), "w") as f:
    f.write(bridge_code)

print("🟢 Script m82_refinitiv_realtime_bridge.py actualizado de forma segura.")
