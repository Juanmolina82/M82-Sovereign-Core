#!/usr/bin/env python3
import os, sys, time, math, random, sqlite3, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
IMG_PATH = os.path.expanduser("~/M82/m82_vlcc_vs_crude_chart.png")
GALLERY_DIR = "/sdcard/Pictures/M82_Cards"
os.makedirs(GALLERY_DIR, exist_ok=True)

def get_font(size, bold_serif=False):
    paths = [
        os.path.expanduser("~/M82/fonts/DejaVuSerif-Bold.ttf") if bold_serif else os.path.expanduser("~/M82/fonts/Roboto-Bold.ttf"),
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans-Bold.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()

def generate_hud_option_b():
    print("🎨 [M82 QUANTUM CORE] Renderizando tarjeta con plantilla Opción B...")
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#050811')
    draw = ImageDraw.Draw(img)

    # Red de Nodos Cuánticos (Celeste sobre Fondo Oscuro)
    random.seed(42)
    nodes = [(random.randint(50, 750), random.randint(150, 850)) for _ in range(22)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 200:
                draw.line([(x1, y1), (x2, y2)], fill='#0c1a2e', width=1)
    for x, y in nodes:
        draw.ellipse([x-2, y-2, x+2, y+2], fill='#1e3a5f')

    # Esquinas HUD
    b_len, b_pad, b_color, b_w = 25, 20, '#1e293b', 2
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill=b_color, width=b_w)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill=b_color, width=b_w)

    # Cargar Fuentes Opción B
    f_meta = get_font(13)
    f_head = get_font(28)
    f_body = get_font(38, bold_serif=True)
    f_sub = get_font(22)
    f_foot = get_font(30, bold_serif=True)

    # Cabecera
    draw.text((60, 55), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#38bdf8', font=f_meta)
    draw.text((60, 90), "#M82 BREAKING STREAM", fill='#ef4444', font=f_head)
    draw.line([(60, 135), (740, 135)], fill='#1e293b', width=1)

    # Titular Grande Estilo Opción B
    headline_text = "VLCC Fletes $1.25M vs Oman $133 & Dubai $119: Pacto VE entrega $54.65/bbl -> Pérdida $7.98B/año"
    lines = textwrap.wrap(headline_text, width=26)
    
    y_text = 240
    for line in lines:
        draw.text((60, y_text), line, fill='#ffffff', font=f_body)
        y_text += 55

    # Pie de Tarjeta
    draw.line([(60, 820), (740, 820)], fill='#1e293b', width=1)
    draw.text((60, 845), "[ AGI QUANTUM VERIFIED ]", fill='#38bdf8', font=f_meta)
    draw.text((60, 880), "@MolinaHoldings LLC", fill='#ffffff', font=f_foot)

    img.save(IMG_PATH)
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_QUANTUM_{int(time.time())}.png")
    img.save(gallery_file)

    try:
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    print("✅ Tarjeta en formato Opción B generada exitosamente.")

if __name__ == "__main__":
    generate_hud_option_b()
