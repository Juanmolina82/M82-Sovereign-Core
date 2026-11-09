#!/usr/bin/env python3
import os, sys, time, math, random, sqlite3, subprocess, requests, textwrap, shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [CORE-ORCHESTRATOR] {msg}", flush=True)

def generate_hud_card(headline, source):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    random.seed(101)
    nodes = [(random.randint(60, 940), random.randint(180, 1050)) for _ in range(20)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 260:
                draw.line([(x1, y1), (x2, y2)], fill='#10233b', width=1)
    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#38bdf8')

    # Marcos esquineros HUD
    b_len, b_pad = 35, 30
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill='#ef4444', width=3)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill='#ef4444', width=3)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill='#ef4444', width=3)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill='#ef4444', width=3)

    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]
    font_main = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_main = ImageFont.truetype(path, 42)
                font_meta = ImageFont.truetype(path, 18)
                font_header = ImageFont.truetype(path, 28)
                font_footer = ImageFont.truetype(path, 32)
                break
            except Exception:
                pass

    if not font_main:
        font_main = font_meta = font_header = font_footer = ImageFont.load_default()

    draw.text((70, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#38bdf8', font=font_meta)
    draw.text((70, 95), f"#M82 BREAKING STREAM [{str(source).upper()}]", fill='#ef4444', font=font_header)
    draw.line([(70, 140), (width - 70, 140)], fill='#1f2937', width=2)

    formatted_headline = headline.title()
    lines = textwrap.wrap(formatted_headline, width=30)
    y_text = 280
    for line in lines:
        draw.text((70, y_text), line, fill='#ffffff', font=font_main)
        y_text += 60

    draw.line([(70, height - 170), (width - 70, height - 170)], fill='#1f2937', width=2)
    draw.text((70, height - 130), "[ AGI QUANTUM VERIFIED ]", fill='#2563eb', font=font_meta)
    draw.text((70, height - 90), "🏛 @MolinaHoldings LLC", fill='#ffffff', font=font_footer)

    img.save(IMG_PATH)

    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{int(time.time())}.png")
    try:
        shutil.copy(IMG_PATH, gallery_file)
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    return IMG_PATH

def send_telegram(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data=payload, files={'photo': photo}, timeout=15)
            return r.status_code == 200
    except Exception as e:
        log(f"❌ Telegram Error: {e}")
        return False

def send_ntfy(source, headline):
    try:
        headers = {
            "Title": f"M82 [{str(source).upper()}]".encode('utf-8').decode('latin-1'),
            "Priority": "high",
            "Tags": "warning,chart_with_upwards_trend"
        }
        requests.post(NTFY_URL, data=headline.encode('utf-8'), headers=headers, timeout=8)
    except Exception:
        pass

def dispatch_signals():
    if not os.path.exists(DB_PATH):
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 1")
        row = c.fetchone()

        if row:
            row_id, source, headline = row
            caption = (
                f"🚨 *#M82 BREAKING SUMMARY*\n\n"
                f"🔴 *[{str(source).upper()}]*\n"
                f"{headline}\n\n"
                f"🏛 @MolinaHoldings LLC"
            )

            img_file = generate_hud_card(headline, source)
            send_ntfy(source, headline)

            if send_telegram(img_file, caption):
                c.execute("UPDATE m82_multi_stream SET status = 'DISPATCHED' WHERE id = ?", (row_id,))
                c.execute("""
                    INSERT INTO macro_dosier (source, category, headline, risk_score, m82_tag)
                    VALUES (?, 'REALTIME_INGEST', ?, 9.0, ?)
                    ON CONFLICT(headline) DO NOTHING
                """, (source, headline, source))
                conn.commit()
                log(f"✅ Señal ID {row_id} despachada a Telegram, Ntfy y Galería.")

        conn.close()
    except Exception as e:
        log(f"❌ Error Dispatcher: {e}")

def main():
    log("🚀 ORQUESTADOR CORE QUANTUM M82 ONLINE")
    while True:
        dispatch_signals()
        time.sleep(10)

if __name__ == "__main__":
    main()
