import os
import sqlite3
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
CARDS_DIR = "/sdcard/Pictures/M82_Cards"
FONT_BOLD = os.path.expanduser("~/M82/fonts/Roboto-Bold.ttf")
FONT_REG = os.path.expanduser("~/M82/fonts/Roboto-Regular.ttf")
BOT_TOKEN = os.getenv("M82_BOT_TOKEN")
CHAT_ID = "-1004335849125"

def generate_hud_card(rec_id, source, headline, alpha_score):
    os.makedirs(CARDS_DIR, exist_ok=True)
    
    # Canvas Principal 1000x1250 px (Fondo Azul Noche)
    img = Image.new('RGB', (1000, 1250), color=(2, 8, 20))
    draw = ImageDraw.Draw(img)
    
    # Cargar Fuentes Vectoriales Garantizadas
    try:
        f_header = ImageFont.truetype(FONT_BOLD, 36)
        f_sub = ImageFont.truetype(FONT_REG, 24)
        f_label = ImageFont.truetype(FONT_BOLD, 22)
        f_val = ImageFont.truetype(FONT_BOLD, 28)
        f_body = ImageFont.truetype(FONT_BOLD, 46)     # Texto central GIGANTE
        f_thesis = ImageFont.truetype(FONT_BOLD, 32)   # Tesis estratégica prominente
        f_small = ImageFont.truetype(FONT_BOLD, 24)    # Gobernanza legible
        print("[M82 FONT SUCCESS] Fuentes TrueType cargadas correctamente.")
    except Exception as e:
        print(f"[M82 FONT WARNING] Fallback a sistema: {e}")
        f_header = f_sub = f_label = f_val = f_body = f_thesis = f_small = ImageFont.load_default()

    # Borde Exterior Neón
    draw.rectangle([10, 10, 990, 1240], outline=(0, 204, 255), width=4)
    draw.rectangle([16, 16, 984, 1234], outline=(0, 102, 204), width=2)
    
    # 1. Header: M82 QUANTUM TERMINAL
    draw.rectangle([30, 30, 970, 105], fill=(5, 20, 45), outline=(0, 204, 255), width=2)
    draw.text((50, 42), "M82 QUANTUM TERMINAL", fill=(0, 255, 204), font=f_header)
    draw.text((50, 78), f"NODE: SOVEREIGN EDGE L5  |  ID: {rec_id}  |  {datetime.now().strftime('%H:%M:%S ET')}", fill=(130, 180, 230), font=f_sub)
    draw.ellipse([925, 48, 950, 73], fill=(0, 255, 128))
    
    # 2. Category & Intelligence
    draw.rectangle([30, 115, 480, 175], fill=(8, 28, 55), outline=(0, 153, 255), width=2)
    draw.text((45, 120), "DESK CATEGORY", fill=(100, 170, 230), font=f_label)
    draw.text((45, 142), f"{source.upper()}", fill=(0, 255, 255), font=f_val)
    
    draw.rectangle([495, 115, 970, 175], fill=(5, 35, 25), outline=(0, 255, 128), width=2)
    draw.text((510, 120), "INTELLIGENCE LAYER", fill=(100, 210, 160), font=f_label)
    draw.text((510, 142), "OLLAMA LOCAL (ZERO-CLOUD)", fill=(0, 255, 128), font=f_val)
    
    # 3. Telemetry Header & Alpha Score
    draw.text((30, 192), "⚡ REAL-TIME WIRE TELEMETRY DISPATCH", fill=(255, 80, 80), font=f_sub)
    draw.rectangle([760, 188, 970, 222], fill=(0, 60, 30), outline=(0, 255, 128), width=1)
    draw.text((775, 194), f"ALPHA {alpha_score:.2f}", fill=(0, 255, 128), font=f_val)
    
    # 4. Marco Central (Texto Gigante 46pt)
    draw.rectangle([30, 230, 970, 680], fill=(4, 15, 32), outline=(0, 153, 255), width=3)
    
    # Formateo de líneas cortas para llenar el marco con letra grande
    words = headline.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line + " " + word) <= 20:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
        
    y = 260
    for line in lines[:7]:
        draw.text((55, y), line, fill=(255, 255, 255), font=f_body)
        y += 58
        
    # 5. Marco Inferior: Strategic Thesis & Governance
    draw.rectangle([30, 700, 970, 1170], fill=(6, 20, 40), outline=(0, 204, 255), width=2)
    
    draw.text((50, 712), "STRATEGIC THESIS", fill=(100, 170, 230), font=f_label)
    draw.text((50, 738), f"⚡ {source.upper()} Signal Shift", fill=(0, 255, 255), font=f_thesis)
    draw.line([(50, 780), (950, 780)], fill=(0, 90, 180), width=1)
    
    draw.text((50, 798), "PORTFOLIO RISK PROFILE", fill=(240, 180, 40), font=f_label)
    draw.text((50, 824), "🛡 Exp 0.22x / 0.30x LOCK  |  VaR 1.68%", fill=(255, 220, 90), font=f_thesis)
    draw.line([(50, 868), (950, 868)], fill=(0, 90, 180), width=1)
    
    draw.text((50, 886), "GOVERNANCE & COMPLIANCE", fill=(100, 170, 230), font=f_label)
    draw.text((50, 914), "🔒 ZERO-PII GATEWAY D-34 MASKED PASS", fill=(210, 230, 250), font=f_small)
    draw.text((50, 948), "🛡 BUNKER MODE 0.30x LOCK ACTIVE", fill=(0, 255, 128), font=f_small)
    
    # Footer
    draw.line([(30, 1190), (970, 1190)], fill=(0, 204, 255), width=1)
    draw.text((30, 1202), "M82 CITADEL PRIME  |  INSTITUTIONAL MACRO OBSERVABILITY", fill=(100, 170, 230), font=f_sub)
    draw.text((710, 1202), "ACTIVE  |  @MolinaHoldings", fill=(0, 255, 204), font=f_sub)
    
    file_path = os.path.join(CARDS_DIR, f"M82_TOP_{rec_id}_1000x1250.png")
    img.save(file_path)
    return file_path

def dispatch_next():
    if not BOT_TOKEN:
        print("[M82 DISPATCH WARNING] M82_BOT_TOKEN no detectado.")
        return

    conn = sqlite3.connect(DB_PATH, timeout=60)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, daemon_source, headline, alpha_score FROM m82_multi_stream WHERE status='VERIFIED' ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        rec_id, source, headline, score = row
        card_path = generate_hud_card(rec_id, source, headline, score)
        
        caption = f"🤖 #M82 [{source}] 📰 {headline[:130]}...\n📊 Alpha: {score} | 🔒 Zero-PII\n#M82 #TOP"
        if len(caption) > 240:
            caption = caption[:237] + "..."
            
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(card_path, 'rb') as photo:
            payload = {'chat_id': CHAT_ID, 'caption': caption}
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files)
            
        if response.status_code == 200:
            cursor.execute("UPDATE m82_multi_stream SET status='DISPATCHED' WHERE id=?", (rec_id,))
            conn.commit()
            print(f"[M82 DISPATCH] ID {rec_id} DISPATCHED SUCCESS (200 OK)")
        else:
            print(f"[M82 DISPATCH ERROR] {response.text}")
            
    conn.close()

if __name__ == "__main__":
    dispatch_next()
