import requests, sqlite3, os
from datetime import datetime

BOT_TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
DB = os.path.expanduser("~/M82/m82_database.db")
NTFY_TOPIC = "M82-Molina-Alerts-v2"

def send_telegram_msg(msg):
    if BOT_TOKEN == "TU_TOKEN_AQUI" or CHAT_ID == "TU_CHAT_ID":
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=5)
    except Exception as e:
        print(f"⚠️ Error enviando texto a Telegram: {e}")

def run_text_dispatch():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute("""
        SELECT asset_impact, final_score, created_at
        FROM m82_multi_stream
        WHERE status='PENDING' AND final_score >= 60
        AND date(created_at)=date('now')
        ORDER BY final_score DESC LIMIT 8
    """).fetchall()

    skipped = c.execute("""
        SELECT COUNT(*) 
        FROM m82_multi_stream 
        WHERE status='SKIPPED_LOW_EV' AND date(created_at)=date('now')
    """).fetchone()[0]

    conn.close()

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    if not rows:
        msg = f"🏛️ *DANEKA M82 / @MolinaHoldings LLC*\n"
        msg += f"🕒 {now_str} ET\n\n"
        msg += f"⚪ *Sin señales activas*\n"
        msg += f"🛡️ Filtradas hoy: *{skipped}* (EV < \$500)\n"
        msg += f"💧 Net Liquidity Drain: *-176B* (Scale: 50%)\n"
        msg += f"📊 Regime: `MELTUP_CONCENTRATED`"
    else:
        msg = f"🏛️ *DANEKA M82 / @MolinaHoldings LLC*\n"
        msg += f"📊 *Resumen Ejecutivo* | {now_str} ET\n"
        msg += f"Regime: `MELTUP` | Drain: `-176B` | Scale: `50%`\n"
        msg += f"Filtradas por bajo EV: *{skipped}*\n\n"
        for asset, score, ts in rows:
            msg += f"🔥 *{asset}* | Score: `{score}` | EV $\ge$ \$500\n"
        msg += f"\n🔗 [Canal Ntfy Live](https://ntfy.sh/{NTFY_TOPIC})"

    send_telegram_msg(msg)
    print("✅ [TELEGRAM TEXT] Mensaje despachado.")

if __name__ == "__main__":
    run_text_dispatch()
