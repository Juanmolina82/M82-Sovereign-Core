#!/usr/bin/env python3
import os, sys, time, datetime, sqlite3, subprocess, math, random, textwrap
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARD_PATH = os.path.join(BASE_DIR, "cards/m82_current_card.png")
LOG_PATH = os.path.join(BASE_DIR, "m82_log.txt")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

os.makedirs(GALLERY_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "cards"), exist_ok=True)

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [M82-MACRO-CORE] {msg}"
    print(formatted, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(formatted + "\n")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    return conn

def load_system_font(size):
    # Rutas estándar de fuentes nativas en Android / Termux
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/system/fonts/DroidSans.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_large_text(draw, position, text, font, fill, scale=3):
    # Si la fuente es la por defecto (minúscula), escalamos por renderizado de matriz
    if isinstance(font, ImageFont.ImageFont):
        x, y = position
        # Crear lienzo temporal para agrandar
        temp_img = Image.new('RGBA', (600, 100), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((0, 0), text, font=font, fill=fill)
        bbox = temp_img.getbbox()
        if bbox:
            cropped = temp_img.crop(bbox)
            resized = cropped.resize((cropped.width * scale, cropped.height * scale), Image.NEAREST)
            draw._image.paste(resized, (x, y), resized)
    else:
        draw.text(position, text, font=font, fill=fill)

def generate_option_b_card(headline_text, source="MACRO_QUANT"):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#030712')
    draw = ImageDraw.Draw(img)

    # 1. Red de Nodos sutiles
    random.seed(101)
    nodes = [(random.randint(80, 920), random.randint(180, 1050)) for _ in range(16)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 280:
                draw.line([(x1, y1), (x2, y2)], fill='#0f172a', width=1)
    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#1e293b')

    # 2. Esquinas Tácticas HUD
    b_len, b_pad, b_w = 35, 25, 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill='#1e293b', width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill='#1e293b', width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill='#1e293b', width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill='#1e293b', width=b_w)

    # 3. Fuentes Nativas del Sistema
    f_small = load_system_font(24)
    f_title = load_system_font(42)
    f_head  = load_system_font(54)
    f_foot  = load_system_font(44)

    # 4. Header Superior
    draw_large_text(draw, (70, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM", f_small, '#0284c7', scale=2)

    # 5. Título Principal
    draw_large_text(draw, (70, 120), "#M82 BREAKING STREAM", f_title, '#ef4444', scale=3)
    draw.line([(70, 185), (width - 70, 185)], fill='#1e293b', width=2)

    # 6. Texto Central Enorme en Blanco
    wrapped_lines = textwrap.wrap(headline_text, width=22)
    y_start = 280
    for line in wrapped_lines:
        if y_start + 80 < height - 200:
            draw_large_text(draw, (70, y_start), line, f_head, '#ffffff', scale=4)
            y_start += 85

    # 7. Footer
    draw.line([(70, height - 190), (width - 70, height - 190)], fill='#1e293b', width=2)
    draw_large_text(draw, (70, height - 150), "[ AGI QUANTUM VERIFIED ]", f_small, '#0284c7', scale=2)
    draw_large_text(draw, (70, height - 95), "@MolinaHoldings LLC", f_foot, '#ffffff', scale=3)

    img.save(CARD_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{int(time.time())}.png")
    img.save(gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    return CARD_PATH

def send_telegram(text, image_path=None):
    if image_path and os.path.exists(image_path):
        cmd = f"curl -s -X POST 'https://api.telegram.org/bot{TOKEN}/sendPhoto' -F 'chat_id={CHAT_ID}' -F 'photo=@{image_path}' -F 'caption={text}'"
    else:
        cmd = f"curl -s -X POST 'https://api.telegram.org/bot{TOKEN}/sendMessage' -d 'chat_id={CHAT_ID}' -d 'text={text}'"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)

def run_pipeline():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1")
    row = c.fetchone()
    
    if row:
        row_id, source, headline = row
        log(f"📌 Imprimiendo tarjeta HD de tamaño gigante para ID {row_id}...")
        card_file = generate_option_b_card(headline, source)
        caption = f"🚨 *#M82 BREAKING STREAM*\n\n{headline}\n\n🏛 @MolinaHoldings LLC | AGI Quantum Node"
        send_telegram(caption, card_file)
        
        c.execute("UPDATE m82_multi_stream SET status = 'SENT_DISPATCHED' WHERE id = ?", (row_id,))
        conn.commit()
        log(f"✅ Tarjeta enviada con letras gigantes.")
    else:
        log("💤 No hay señales PENDING en cola.")
        
    conn.close()

if __name__ == "__main__":
    run_pipeline()
