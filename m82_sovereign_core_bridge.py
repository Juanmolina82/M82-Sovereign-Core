#!/usr/bin/env python3
import sqlite3, os, time, requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")
TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
IMG_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")

os.makedirs(IMG_DIR, exist_ok=True)

def draw_option_b_hud(daemon_name, headline, exp_str, var_str, warsh_str):
    # Canvas 1080x1350 (Opción B Ratio HD)
    img = Image.new('RGB', (1080, 1350), color='#050B14')
    draw = ImageDraw.Draw(img)
    
    # Cargar fuentes del sistema o por defecto (Bold sans)
    try:
        font_header = ImageFont.truetype("Roboto-Bold.ttf", 32)
        font_sub = ImageFont.truetype("Roboto-Bold.ttf", 38)
        font_risk = ImageFont.truetype("Roboto-Medium.ttf", 34)
        font_main = ImageFont.truetype("Roboto-Bold.ttf", 52)
        font_footer = ImageFont.truetype("Roboto-Bold.ttf", 30)
    except:
        font_header = font_sub = font_risk = font_main = font_footer = ImageFont.load_default()

    # Borde Externo Cyan de Doble Trazo (Estilo Búnker M82)
    draw.rectangle([15, 15, 1065, 1335], outline='#00E5FF', width=4)
    draw.rectangle([25, 25, 1055, 1325], outline='#005577', width=1)
    
    # Caja Header Superior
    draw.rectangle([40, 40, 1040, 150], fill='#0A192F', outline='#00E5FF', width=2)
    draw.text((60, 55), "SYSTEM: AGI-CORE // NODE: SOVEREIGN EXECUTION CORE", fill='#00E5FF', font=font_header)
    draw.text((60, 95), "M82 SOVEREIGN MONITOR // HUD CARDS", fill='#8892B0', font=font_header)
    
    # Etiqueta de Daemon
    draw.rectangle([60, 170, 520, 220], outline='#00E5FF', width=2)
    draw.text((75, 178), f"DAEMON: {daemon_name.upper()}", fill='#FFFFFF', font=font_sub)
    
    # Bloque de Riesgo y Métricas
    draw.text((60, 245), f"EXPOSURE: {exp_str} | VaR L5.1: {var_str}", fill='#00E5FF', font=font_risk)
    draw.text((60, 285), f"MEREY 16: $93.15 ITM | WARSH SPREAD: {warsh_str}", fill='#FFB74D', font=font_risk)
    
    # Divisor en Rojo Vívido (Wire Breaking)
    draw.line([(60, 340), (1020, 340)], fill='#FF1744', width=4)
    draw.text((60, 355), "❚ REFINITIV BREAKING WIRE", fill='#FF1744', font=font_sub)
    
    # Inserción de Titular Gigante en Blanco (Sin solapamientos - Formato B)
    draw.text((60, 430), f"[{daemon_name.upper()}]", fill='#FFFFFF', font=font_main)
    
    # Auto-wrap para titular gigante
    words = headline.split()
    lines, current = [], ""
    for w in words:
        if len(current + " " + w) < 22:
            current += (" " if current else "") + w
        else:
            lines.append(current)
            current = w
    if current: lines.append(current)
    
    y = 510
    for line in lines[:7]:
        draw.text((60, y), line, fill='#FFFFFF', font=font_main)
        y += 75

    # Footer de Gobernanza Búnker
    draw.rectangle([40, 1240, 1040, 1300], fill='#0A192F', outline='#00E5FF', width=1)
    draw.text((60, 1255), "[ AGI QUANTUM VERIFIED — CUSTODIA PASIVA 0.30x LOCK ]", fill='#00E5FF', font=font_footer)
    
    file_path = os.path.join(IMG_DIR, f"m82_hud_b_{int(time.time())}.png")
    img.save(file_path)
    return file_path

def send_telegram_photo(photo_path, caption_text):
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "caption": caption_text, "parse_mode": "Markdown"},
                files={"photo": photo},
                timeout=15
            )
        print(f"[+] Telegram Status: {r.status_code}")
        return r.status_code
    except Exception as e:
        print(f"[!] Error: {e}")
        return 0

def loop():
    print("🚀 M82 ENGINE ACTIVE :: OPTION B HUD RENDER & DISPATCH ENGAGED")
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        daemon = "CITGO_OFAC_DESK"
        headline = "2026-10-19 14:39:33 OFAC GL 5Z Citgo auction Delaware docket update"
        
        # Generar Tarjeta Gráfica Opción B
        card_path = draw_option_b_hud(
            daemon, 
            headline, 
            "0.22x / 0.30x LOCK", 
            "1.68%", 
            "+102.0bps"
        )
        
        # Refrescar galería Android
        os.system(f"termux-media-scan '{card_path}' >/dev/null 2>&1")
        
        caption = (
            f"⚡ *#M82 TELEMETRIA VIVA (OPCIÓN B)* :: {now} VET\n"
            f"───────────────────────────\n"
            f"🏛 *M82 WIRE:* [{daemon}] {headline}\n"
            f"🛡 *RISK:* Exp 0.22x/0.30x LOCK | VaR 1.68% | Warsh +102.0bps\n"
            f"🔒 *CUSTODIA PASIVA — NODO CHARALLAVE L4/L5*"
        )
        
        send_telegram_photo(card_path, caption)
        time.sleep(60)

if __name__ == "__main__":
    loop()
