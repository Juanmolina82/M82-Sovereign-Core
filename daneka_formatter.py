#!/usr/bin/env python3
import os, time, hashlib, sqlite3, html, requests

DB = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = os.environ.get("M82_TG_BOT_TOKEN", "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4")
TG_CHAT_ID = os.environ.get("M82_TG_CHAT_ID", "-1004335849125")
NTFY_URL = os.environ.get("M82_NTFY_TOPIC", "https://ntfy.sh/M82-Molina-Alerts-v2")

def init_dedup_table():
    c = sqlite3.connect(DB, timeout=60.0)
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("CREATE TABLE IF NOT EXISTS daneka_sent_hashes (msg_hash TEXT PRIMARY KEY, sent_at REAL);")
    c.commit()
    c.close()

def is_duplicate(key: str, cooldown_sec: int = 3600) -> bool:
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    now = time.time()
    c = sqlite3.connect(DB, timeout=60.0)
    c.execute("PRAGMA busy_timeout=60000;")
    row = c.execute("SELECT sent_at FROM daneka_sent_hashes WHERE msg_hash=?;", (h,)).fetchone()
    if row and (now - row[0]) < cooldown_sec:
        c.close()
        return True
    c.execute("INSERT OR REPLACE INTO daneka_sent_hashes VALUES (?, ?);", (h, now))
    c.commit()
    c.close()
    return False

def send_daneka_brief(wires: list, merey_sep="93.75", merey_live="93.92", brent="94.32", brent_chg="-4.07%"):
    init_dedup_table()
    # Filtrar heartbeats genéricos y titulares ya enviados
    clean_wires = []
    for sector, title in wires:
        if "Refinitiv Workspace Sync Active" in title:
            continue
        clean_title = title.replace("$$", "$").strip()
        if not is_duplicate(f"{sector}:{clean_title}", cooldown_sec=7200):
            clean_wires.append((html.escape(sector), html.escape(clean_title)))

    if not clean_wires:
        return {"status": "SKIPPED_NO_NEW_WIRES"}

    ts_vet = time.strftime("%d %b %Y · %H:%M VET")
    wire_lines = "\n".join([f"• <b>[{sec}]</b> {tit}" for sec, tit in clean_wires])

    card_html = (
        f"🏛 <b>DANEKA M82 :: INTELLIGENCE &amp; RISK BRIEF</b>\n"
        f"🕒 <code>{ts_vet}</code> | 📍 <code>Charallave L4/L5 Edge</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 <b>CABLES VERIFICADOS (LSEG WIRE)</b>\n"
        f"{wire_lines}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛢 <b>BENCHMARKS ENERGÍA</b>\n"
        f"• <b>Merey 16:</b> <code>${merey_sep}</code> Sep / <code>${merey_live}</code> Live\n"
        f"• <b>Brent Crude:</b> <code>${brent}</code> (<code>{brent_chg}</code>)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ <b>GOBERNANZA &amp; RIESGO (WAL SINGLE SOURCE)</b>\n"
        f"• <b>Exposición:</b> <code>0.22x / 0.30x LOCK</code> (<code>LOCKOUT: NO TRADE</code>)\n"
        f"• <b>VaR Diario:</b> <code>1.68%</code> | <b>Warsh Spread:</b> <code>+102.0 bps</code>"
    )

    rt = requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": TG_CHAT_ID, "text": card_html, "parse_mode": "HTML", "disable_web_page_preview": True},
        timeout=8
    )
    plain_ntfy = "\n".join([f"[{sec}] {tit}" for sec, tit in clean_wires]) + f" | Brent ${brent} ({brent_chg}) | Exp 0.22x/0.30x LOCK"
    rn = requests.post(NTFY_URL, data=plain_ntfy.encode("utf-8"), headers={"Title": "DANEKA M82 BRIEF", "Priority": "default"}, timeout=8)
    return {"telegram": rt.status_code, "ntfy": rn.status_code, "wires_sent": len(clean_wires)}

if __name__ == "__main__":
    sample_wires = [
        ("MUSK_INC", "3 Things You Need to Know Before Buying SpaceX"),
        ("MUSK_INC", "SpaceX Wants a Tax Break for a $24 Billion Gas Plant and Supercomputer at Starbase")
    ]
    print("OK Daneka Formatter ->", send_daneka_brief(sample_wires))
