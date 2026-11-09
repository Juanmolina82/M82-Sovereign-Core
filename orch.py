#!/usr/bin/env python3
import os, time, sqlite3, requests, textwrap
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
GALLERY_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")
if not os.path.exists(GALLERY_DIR):
    GALLERY_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")
os.makedirs(GALLERY_DIR, exist_ok=True)

TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

def get_font(size):
    for p in [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def render_hud_card(evt_id, headline, daemon_source):
    W, H = 1000, 1250
    img = Image.new('RGB', (W, H), color='#05080e')
    draw = ImageDraw.Draw(img)
    f_hdr = get_font(26); f_sub = get_font(22); f_tag = get_font(24)
    f_red = get_font(28); f_body = get_font(38); f_ftr = get_font(22)

    draw.rectangle([15, 15, W - 15, H - 15], outline='#00b0ff', width=4)
    draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)
    draw.text((50, 48), "SYSTEM: AGI-CORE // NODE: SOVEREIGN EXECUTION CORE", fill='#00e5ff', font=f_hdr)
    draw.text((50, 85), "M82 SOVEREIGN MONITOR // HUD CARDS", fill='#708090', font=f_sub)

    draw.rectangle([55, 145, 550, 205], fill='#0c182b', outline='#00b0ff', width=2)
    clean_src = str(daemon_source).replace("DAEMON:", "").strip().upper()
    draw.text((70, 162), f"DAEMON: {clean_src[:26]}", fill='#ffffff', font=f_tag)

    draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
    draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=f_sub)
    draw.text((75, 280), "MEREY 16: $93.75 SEP / $93.92 LIVE  |  BRENT: $114.72", fill='#ff9100', font=f_sub)

    draw.text((55, 348), "❚ M82_SOVEREIGN WORKSPACE TELEMETRY WIRE", fill='#ff1744', font=f_red)
    draw.line([(55, 388), (W - 55, 388)], fill='#ff1744', width=3)

    draw.rectangle([55, 405, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)
    lines = textwrap.wrap(str(headline), width=28)
    y = 430
    for line in lines[:9]:
        draw.text((80, y), line, fill='#ffffff', font=f_body); y += 58

    draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
    draw.text((50, H - 100), "[ AGI QUANTUM VERIFIED — CUSTODIA PASIVA 0.30x LOCK ]", fill='#00e5ff', font=f_ftr)
    draw.text((50, H - 68), "❚ @MolinaHoldings | Sovereign Execution Node", fill='#ffffff', font=f_ftr)

    fp = os.path.join(GALLERY_DIR, f"M82_CARD_{evt_id}.png")
    img.save(fp)
    os.system(f"termux-media-scan '{fp}' >/dev/null 2>&1 || true")
    return fp

def process_stream():
    if not os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    
    cur.execute("SELECT id, headline, daemon_source FROM m82_multi_stream WHERE status='PENDING' ORDER BY id ASC LIMIT 10")
    rows = cur.fetchall()
    
    for row in rows:
        evt_id, headline, source = row
        str_hl = str(headline)
        
        # M82 ANTI-DANEKA / PLACEHOLDER FILTER
        if 'Signal update' in str_hl or '1792729293' in str_hl or len(str_hl) < 25:
            cur.execute("UPDATE m82_multi_stream SET status='PURGED_PLACEHOLDER' WHERE id=?", (evt_id,))
            conn.commit()
            print(f"🚫 [ANTI-DANEKA PURGE] Event #{evt_id} ({source}) discarded.")
            continue

        img_path = render_hud_card(evt_id, headline, source)
        caption = (
            f"⚡ *#M82 TELEMETRIA VIVA* :: {source}\n"
            f"───────────────────────────\n"
            f"🏛 *WIRE:* {headline}\n\n"
            f"🛡 *RISK:* Exp 0.22x/0.30x LOCK | VaR 1.68%\n"
            f"🛢 *ANCHOR:* Merey 16 $93.75 Sep / $93.92 Live | Brent $114.72\n"
            f"🔒 *SOVEREIGN EXECUTION CORE*"
        )
        try:
            with open(img_path, 'rb') as photo:
                r = requests.post(
                    f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto",
                    data={'chat_id': CHAT_ID, 'caption': caption, "parse_mode": "HTML"},
                    files={'photo': photo},
                    timeout=15
                )
                if r.status_code == 200:
                    cur.execute("UPDATE m82_multi_stream SET status='PROCESSED' WHERE id=?", (evt_id,))
                    conn.commit()
                    print(f"[+] Evento #{evt_id} ({source}) HD OK")
                    break
                else:
                    print(f"[-] TG {r.status_code} | {r.text[:100]}")
        except Exception as e:
            print(f"[-] {e}")
            
    conn.close()

if __name__ == "__main__":
    print("🚀 [M82 UNIFIED DISPATCHER] Anti-Daneka Filter Active — 60s Cadence")
    while True:
        try:
            process_stream()
        except Exception as e:
            print(f"[-] Error: {e}")
        time.sleep(60)

import subprocess
subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "B"], check=False)
