#!/usr/bin/env python3
import os, textwrap, math, random
from PIL import Image, ImageDraw, ImageFont

GALLERY_DIR = "/sdcard/Pictures/M82_Cards"

def build_hud_card(headline="Exclusive | Pentagon-Backed Oil Company Is Set to Vie for Chevron's Crown in Venezuela", tag="#M82 BREAKING [VENEZUELA_DESK]"):
    os.makedirs(GALLERY_DIR, exist_ok=True)
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='#050B14')
    draw = ImageDraw.Draw(img)

    # 1. Red neural / Constelación de fondo
    random.seed(42)
    nodes = [(random.randint(80, 720), random.randint(100, 900)) for _ in range(25)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 180:
                draw.line([(x1, y1), (x2, y2)], fill='#102A45', width=1)
    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#0099FF')

    # 2. Marco y esquinas Tactical HUD
    draw.rectangle([30, 30, width-30, height-30], outline='#102A45', width=1)
    
    # 3. Cargar Fuentes (fallback a default si no existen ttf)
    try:
        font_tag = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 22)
        font_title = ImageFont.truetype("/system/fonts/DroidSerif-Regular.ttf", 40)
        font_footer = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 26)
    except:
        font_tag = font_title = font_footer = ImageFont.load_default()

    # 4. Header / Tag
    draw.text((60, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms", fill='#335577', font=font_tag)
    draw.text((60, 100), tag, fill='#DD3333', font=font_tag)

    # 5. Titular Principal (Wrap ajustado a 24 caracteres para bloque limpio)
    wrapped_lines = textwrap.wrap(headline, width=24)
    y_text = 240
    for line in wrapped_lines:
        draw.text((60, y_text), line, fill='#FFFFFF', font=font_title)
        y_text += 52

    # 6. Marca de Agua / Footer
    draw.text((60, height - 100), "[ AGI QUANTUM VERIFIED ]", fill='#225588', font=font_tag)
    draw.text((60, height - 60), "@MolinaHoldings", fill='#FFFFFF', font=font_footer)
    draw.text((280, height - 58), "LLC", fill='#666666', font=font_tag)

    out_path = os.path.join(GALLERY_DIR, "m82_breaking_card.png")
    img.save(out_path)
    print(f"✅ Tarjeta generada exitosamente en: {out_path}")

if __name__ == "__main__":
    build_hud_card()
