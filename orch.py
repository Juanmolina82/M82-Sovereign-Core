#!/usr/bin/env python3
import os, time, sqlite3, requests, textwrap, shutil, subprocess, math, random, re
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID_PRIMARY = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_card.png")

GALLERY_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")
if not os.path.exists(GALLERY_DIR):
    GALLERY_DIR = "/sdcard/Pictures/M82_Cards"
    os.makedirs(GALLERY_DIR, exist_ok=True)

def force_all_hashtags(headline):
    words = headline.split()
    formatted = []
    for word in words:
        clean = re.sub(r'[^\w\s]', '', word)
        if clean:
            formatted.append(word.replace(clean, f"#{clean}"))
        else:
            formatted.append(word)
    return " ".join(formatted)

def get_font(size):
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

def generate_hud(headline, source):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    font_meta = get_font(26)
    font_header = get_font(38)
    font_main = get_font(60)
    font_footer = get_font(36)

    random.seed(101)
    nodes = [(random.randint(60, 940), random.randint(180, 1050)) for _ in range(18)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 260:
                draw.line([(x1, y1), (x2, y2)], fill='#10233b', width=2)
    for x, y in nodes:
        draw.ellipse([x-5, y-5, x+5, y+5], fill='#38bdf8')

    b_len, b_pad = 45, 30
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill='#ef4444', width=4)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill='#ef4444', width=4)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill='#ef4444', width=4)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill='#ef4444', width=4)

    draw.text((60, 50), "SYSTEM: AGI-CORE // NODE: M82", fill='#38bdf8', font=font_meta)
    draw.text((60, 90), f"🚨 #M82 #BREAKING STREAM", fill='#ef4444', font=font_header)
    draw.text((60, 135), f"🔴 [{str(source).upper()}]", fill='#38bdf8', font=font_meta)
    draw.line([(60, 175), (width - 60, 175)], fill='#1f2937', width=3)

    lines = textwrap.wrap(headline, width=22)
    y_text = 240
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=font_main)
        y_text += 80

    draw.line([(60, height - 140), (width - 60, height - 140)], fill='#1f2937', width=3)
    draw.text((60, height - 105), "[ AGI QUANTUM VERIFIED ]", fill='#2563eb', font=font_meta)
    draw.text((60, height - 65), "🏛 @MolinaHoldings | AGI Quantum Node", fill='#ffffff', font=font_footer)

    img.save(IMG_PATH)
    
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{int(time.time())}.png")
    try:
        shutil.copy(IMG_PATH, gallery_file)
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass
        
    return IMG_PATH

def dispatch():
    if not os.path.exists(DB_PATH): return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 1")
    row = c.fetchone()
    if row:
        row_id, source, headline = row
        all_hashtag_headline = force_all_hashtags(headline)
        
        # 1. Telegram
        try:
            img_file = generate_hud(headline, source)
            telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            caption_text = (
                f"🚨 *#M82 #BREAKING STREAM*\n\n"
                f"{all_hashtag_headline}\n\n"
                f"🏛 @MolinaHoldings | AGI Quantum Node"
            )
            with open(img_file, 'rb') as photo:
                requests.post(telegram_url, data={"chat_id": CHAT_ID_PRIMARY, "caption": caption_text, "parse_mode": "Markdown"}, files={'photo': photo}, timeout=10)
        except Exception as e:
            print(f"⚠️ Error enviando a Telegram: {e}")

        # 2. ntfy.sh (Ajuste compatibilidad UTF-8 en headers HTTP)
        try:
            headers = {
                "Title": f"M82 ALERT: [{source}]",
                "Priority": "high",
                "Tags": "rotating_light,warning"
            }
            requests.post(
                NTFY_URL,
                data=all_hashtag_headline.encode('utf-8'),
                headers=headers,
                timeout=10
            )
        except Exception as e:
            print(f"⚠️ Error enviando a ntfy.sh: {e}")

        c.execute("UPDATE m82_multi_stream SET status = 'DISPATCHED' WHERE id = ?", (row_id,))
        conn.commit()
        print(f"✅ Señal {row_id} enviada (Telegram: HUD Image | ntfy.sh: Texto puro).")

    conn.close()

if __name__ == "__main__":
    while True:
        try:
            dispatch()
        except Exception as e:
            print(f"⚠️ Error en orquestador: {e}")
        time.sleep(70)
