#!/usr/bin/env python3
import sqlite3, json, os, urllib.request, urllib.parse, math
from PIL import Image, ImageDraw, ImageFont

TELEGRAM_TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4")
TELEGRAM_CHAT_ID = os.getenv("M82_CHAT_ID", "-1004335849125")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
CARD_IMG_PATH = os.path.expanduser("~/M82/latest_card.png")

def load_safe_font(size):
    font_candidates = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_scaled_text(draw, position, text, fill, scale=3):
    x, y = position
    temp_img = Image.new('RGBA', (800, 100), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), text, fill=fill, font=ImageFont.load_default())
    w = int(temp_img.width * scale)
    h = int(temp_img.height * scale)
    resized_img = temp_img.resize((w, h), Image.Resampling.NEAREST)
    draw._image.paste(resized_img, (x, y), resized_img)

def generate_corporate_card(headline, source_tag):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#070A12')
    draw = ImageDraw.Draw(img)

    # Red Quantum M82
    nodes = [(700, 220), (820, 290), (910, 200), (970, 320), 
             (580, 580), (750, 560), (850, 640), (980, 600),
             (480, 640), (580, 750), (720, 900), (220, 940)]
    
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            dist = math.hypot(nodes[i][0]-nodes[j][0], nodes[i][1]-nodes[j][1])
            if dist < 280:
                draw.line([nodes[i], nodes[j]], fill='#132238', width=2)

    for x, y in nodes:
        draw.ellipse([x-4, y-4, x+4, y+4], fill='#38BDF8')

    font_main = load_safe_font(54)
    font_header = load_safe_font(32)
    font_small = load_safe_font(20)

    # Marcos esquineros
    draw.line([(40, 40), (80, 40)], fill='#334155', width=4)
    draw.line([(40, 40), (40, 80)], fill='#334155', width=4)
    draw.line([(920, 40), (960, 40)], fill='#334155', width=4)
    draw.line([(960, 40), (960, 80)], fill='#334155', width=4)
    
    draw.line([(40, 1210), (80, 1210)], fill='#334155', width=4)
    draw.line([(40, 1170), (40, 1210)], fill='#334155', width=4)
    draw.line([(920, 1210), (960, 1210)], fill='#334155', width=4)
    draw.line([(960, 1170), (960, 1210)], fill='#334155', width=4)

    # Encabezado
    draw.text((75, 70), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#475569', font=font_small)
    draw.text((75, 120), f"#M82 BREAKING [{source_tag.upper()}]", fill='#DC2626', font=font_header)
    draw.line([(75, 180), (925, 180)], fill='#1E293B', width=2)

    # Headline Formateado
    formatted_headline = headline.title()
    words = formatted_headline.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 20:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))

    # Renderizado del titular
    y_pos = 320
    is_default = isinstance(font_main, ImageFont.ImageFont)
    
    for line in lines:
        if is_default:
            draw_scaled_text(draw, (75, y_pos), line, fill='#FFFFFF', scale=4)
            y_pos += 85
        else:
            draw.text((75, y_pos), line, fill='#FFFFFF', font=font_main)
            y_pos += 85

    # Pie Institucional
    draw.text((75, 1040), "[ AGI QUANTUM VERIFIED ]", fill='#1D4ED8', font=font_small)
    draw.text((75, 1085), "@MolinaHoldings LLC", fill='#FFFFFF', font=font_header)

    img.save(CARD_IMG_PATH)

def send_telegram_photo():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    
    if not os.path.exists(CARD_IMG_PATH):
        print("❌ Imagen no encontrada para envío.")
        return

    with open(CARD_IMG_PATH, 'rb') as f:
        img_bytes = f.read()

    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{TELEGRAM_CHAT_ID}\r\n".encode())
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"card.png\"\r\nContent-Type: image/png\r\n\r\n".encode())
    body.append(img_bytes)
    body.append(f"\r\n--{boundary}--\r\n".encode())
    
    payload = b"".join(body)
    req = urllib.request.Request(url, data=payload, headers=headers)
    
    try:
        urllib.request.urlopen(req, timeout=10)
        print("✅ Tarjeta corporativa generada y enviada a Telegram exitosamente.")
    except Exception as e:
        print(f"❌ Error al enviar imagen a Telegram: {e}")

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("❌ Base de datos no encontrada.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT headline, m82_tag FROM macro_dosier WHERE risk_score >= 8.0 ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    if row:
        generate_corporate_card(row[0], row[1])
        send_telegram_photo()
    conn.close()
