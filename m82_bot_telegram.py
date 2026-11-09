import os, sqlite3, time, requests, json, logging
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

TELEGRAM_BOT_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TELEGRAM_CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

logging.basicConfig(
    filename=os.path.expanduser('~/M82/m82_dispatch.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    return conn

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=8)
        if r.status_code == 200:
            logging.info("Telegram Macro alert dispatched successfully.")
        else:
            logging.error(f"Telegram Dispatch Error {r.status_code}: {r.text}")
    except Exception as e:
        logging.error(f"Exception on Telegram Dispatch: {e}")

def send_ntfy_alert(title, message, priority="default", tags="chart_with_upwards_trend,rocket"):
    headers = {"Title": title, "Priority": priority, "Tags": tags}
    try:
        requests.post(NTFY_URL, data=message.encode('utf-8'), headers=headers, timeout=8)
    except Exception as e:
        logging.error(f"ntfy Dispatch Exception: {e}")

def query_macro_dossier_summary():
    try:
        conn = get_db()
        # Muestreo de categorías clave
        macro_rows = conn.execute("""
            SELECT category, headline, risk_score, m82_tag, sentiment 
            FROM macro_dossier 
            ORDER BY id DESC LIMIT 3
        """).fetchall()
        
        gh_count = conn.execute("SELECT COUNT(*) FROM github_dossier").fetchone()[0]
        conn.close()
        
        summary = "<b>📊 M82 MACRO DOSSIER SUMMARY:</b>\n"
        for r in macro_rows:
            summary += f"• <b>[{r['category']}]</b> {r['headline'][:80]}... (Risk: {r['risk_score']})\n"
        summary += f"• <b>GitHub Sovereign Repos:</b> <code>{gh_count} Repos Synced</code>\n"
        return summary
    except Exception as e:
        return f"Error leyendo Macro Dossier: {e}"

def process_telegram_updates(offset):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=5"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            for update in data.get("result", []):
                new_offset = update["update_id"] + 1
                message = update.get("message", {})
                text = message.get("text", "").strip()
                chat_id = str(message.get("chat", {}).get("id", ""))
                
                # Responder a comandos en el chat objetivo
                if chat_id == TELEGRAM_CHAT_ID:
                    if text in ["/dossier", "/macro"]:
                        dossier_text = (
                            "⚡ <b>M82 ROBUST MACRO DOSSIER ENGINE</b>\n"
                            "───────────────────────\n"
                            f"{query_macro_dossier_summary()}\n"
                            "<b>Gobernanza:</b> BUNKER MODE (0.30x LOCK)"
                        )
                        send_telegram_alert(dossier_text)
                    elif text in ["/bunker", "/status"]:
                        status_text = (
                            "🔒 <b>M82 GOVERNANCE & BUNKER METRICS</b>\n"
                            "───────────────────────\n"
                            "• <b>LOCK Protocol:</b> 0.30x (Exposición ~0.22x)\n"
                            "• <b>VaR Diaria:</b> ~1.68%\n"
                            "• <b>Warsh Spread:</b> +102.0 bps\n"
                            "• <b>Edge Topology:</b> Charallave L4/L5 Edge Active\n"
                            "• <b>WAL DB Mode:</b> PRAGMA WAL Checkpointed"
                        )
                        send_telegram_alert(status_text)
                return new_offset
    except Exception as e:
        logging.error(f"Error procesando updates de Telegram: {e}")
    return offset

def run_macro_bot():
    print("⚡ [M82 MACRO BOT] Servicio iniciado con conexión directa al Macro Dossier...")
    
    # Notificación de actualización e integración
    dossier_init = query_macro_dossier_summary()
    init_msg = (
        "⚡ <b>M82 V60 AGI QUANTUM — MACRO BOT ENGINE ONLINE</b>\n"
        "<b>Node:</b> Sovereign Edge L4/L5 Charallave\n"
        "<b>Target Chat:</b> <code>-1004335849125</code>\n"
        "───────────────────────\n"
        f"{dossier_init}\n"
        "<b>Comandos Activos:</b> <code>/dossier</code>, <code>/bunker</code>, <code>/status</code>"
    )
    send_telegram_alert(init_msg)
    send_ntfy_alert("M82 Macro Dossier Bot Synced", "Bot interconectado con macro_dossier y github_dossier.", "high", "brain,rocket")

    last_stream_id = 0
    try:
        conn = get_db()
        res = conn.execute("SELECT MAX(id) FROM m82_multi_stream").fetchone()
        if res and res[0]:
            last_stream_id = res[0]
        conn.close()
    except Exception as e:
        print(f"Error inicializando Stream ID: {e}")

    update_offset = 0

    while True:
        # 1. Escuchar comandos entrantes en Telegram
        update_offset = process_telegram_updates(update_offset)
        
        # 2. Escuchar nuevos eventos en el multi_stream y vincular con Macro Dossier
        try:
            conn = get_db()
            cur = conn.cursor()
            rows = cur.execute("""
                SELECT id, daemon_source, headline, alpha_score, sentiment, asset_impact, event_trigger 
                FROM m82_multi_stream 
                WHERE id > ? 
                ORDER BY id ASC LIMIT 5
            """, (last_stream_id,)).fetchall()
            
            for r in rows:
                row_id = r['id']
                daemon = r['daemon_source'] or 'M82_DAEMON'
                headline = r['headline'] or 'Evento telemétrico'
                alpha = r['alpha_score'] if r['alpha_score'] is not None else 0.85
                sentiment = r['sentiment'] if r['sentiment'] is not None else 0.85
                impact = r['asset_impact'] or 'NEUTRAL'
                
                q_sig = round(alpha * 0.70 + sentiment * 0.30, 4)
                var_c = round((1.0 - alpha) * 1.68, 4)
                
                # Despacho enriquecido con contexto Macro Dossier
                if alpha >= 0.88 or any(k in headline for k in ["TSLA", "SPACEX", "NFLX", "MEREY", "SETTHEDATE", "GITHUB"]):
                    msg = (
                        f"⚡ <b>M82 MACRO INTELLIGENCE :: {daemon}</b>\n"
                        f"<b>Headline:</b> {headline}\n"
                        f"───────────────────────\n"
                        f"<b>Quant Signal:</b> <code>{q_sig}</code> | <b>Alpha:</b> <code>{alpha}</code>\n"
                        f"<b>VaR Contrib:</b> <code>{var_c}%</code> | <b>Impact:</b> <code>{impact}</code>\n"
                        f"<b>Macro Sync:</b> Linked to WAL Macro Dossier"
                    )
                    send_telegram_alert(msg)
                    send_ntfy_alert(f"M82 Alert: {daemon}", f"{headline} | Quant: {q_sig}", "default", "chart_with_upwards_trend")
                    print(f"📲 [MACRO DISPATCHED] ID {row_id} -> Telegram ({daemon})")
                
                last_stream_id = row_id
                
            conn.close()
        except Exception as e:
            print(f"Error en loop de despacho Macro: {e}")
            
        time.sleep(8)

if __name__ == '__main__':
    run_macro_bot()
