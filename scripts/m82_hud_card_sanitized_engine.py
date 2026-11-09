#!/usr/bin/env python3
# M82 SOVEREIGN CORE - HARD SANITIZED HUD ENGINE (PERMANENT OPSEC & BRAND PURGE)
import sqlite3, os, json, subprocess, textwrap, re
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
GALLERY_DIRS = [
    os.path.expanduser("~/storage/shared/Pictures/M82_Cards"),
    "/sdcard/Pictures/M82_Cards"
]
for d in GALLERY_DIRS:
    os.makedirs(d, exist_ok=True)

# 1. Consulta del registro más reciente en macro_dossier
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
cur = conn.cursor()
cur.execute("SELECT id, headline, category, version FROM macro_dossier ORDER BY id DESC LIMIT 1;")
row = cur.fetchone()
conn.close()

if not row:
    print("⚠️ No hay registros en macro_dossier.")
    exit(1)

rec_id, headline, category, version = row

# --- PURGA HARDCODED DE SEGURIDAD Y MARCAS ---
def purge_sensitive_data(text):
    if not text: return ""
    # PII & OPSEC Ubicaciones
    text = re.sub(r'(?i)charallave(\s*l4/l5\s*edge)?', 'SOVEREIGN EDGE', text)
    text = re.sub(r'(?i)jmmp@molina82\.com', '[REDACTED]', text)
    # Trademarks & Copyright
    text = re.sub(r'(?i)refinitiv_?', '', text)
    text = re.sub(r'(?i)refinitiv', '', text)
    text = re.sub(r'(?i)workspace', '', text)
    text = re.sub(r'(?i)lseg', '', text)
    return text.strip()

clean_headline = purge_sensitive_data(headline)
clean_category = purge_sensitive_data(category)
if not clean_category or clean_category == "":
    clean_category = "GLOBAL_MACRO_QUANT"

# 2. Carga de Tipografías
def load_font(size):
    for p in ["/system/fonts/Roboto-Bold.ttf", "/system/fonts/DroidSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

f_hdr = load_font(30); f_sub = load_font(26); f_tag = load_font(28)
f_red = load_font(32); f_body = load_font(48); f_ftr = load_font(24)

# 3. Canvas y Renderizado (1080 x 1350 px)
W, H = 1080, 1350
img = Image.new('RGB', (W, H), color='#040812')
draw = ImageDraw.Draw(img)

# Bordes
draw.rectangle([15, 15, W - 15, H - 15], outline='#00e5ff', width=4)
draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)

now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S ET")

# Cabecera 100% Sanitizada (Sin Ubicación de Nodo, Sin PII, Sin Marcas)
draw.text((50, 48), "M82 SOVEREIGN MONITOR // QUANTUM TERMINAL HUD", fill='#00e5ff', font=f_hdr)
draw.text((50, 85), f"NODE: SOVEREIGN EDGE CORE | SECURE OPERATOR D-34 | {now_utc}", fill='#708090', font=f_sub)

draw.rectangle([55, 145, 620, 205], fill='#0c182b', outline='#00b0ff', width=2)
draw.text((70, 162), f"DESK: {clean_category[:26]}", fill='#ffffff', font=f_tag)

draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=f_sub)
draw.text((75, 280), "ULCC: $6.48 (+31.2%) | REV: $1.4B | DEBT: $5B | CASH: $976M", fill='#ff9100', font=f_sub)

draw.text((55, 348), "❚ M82 TELEMETRY WIRE DISPATCH", fill='#ff1744', font=f_red)
draw.line([(55, 388), (W - 55, 388)], fill='#ff1744', width=3)

draw.rectangle([55, 405, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)

lines = textwrap.wrap(clean_headline, width=22)
y_pos = 440
for line in lines[:9]:
    draw.text((85, y_pos), line, fill='#ffffff', font=f_body)
    y_pos += 68

draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
draw.text((50, H - 100), "[ AGI QUANTUM VERIFIED -- CUSTODIA PASIVA 0.30x LOCK ]", fill='#00e5ff', font=f_ftr)
draw.text((50, H - 68), "❚ SOVEREIGN EDGE CORE | Sovereign Execution Node", fill='#ffffff', font=f_ftr)

# Guardar e Indexar
for d in GALLERY_DIRS:
    out_path = os.path.join(d, f"M82_CARD_HARD_SANITIZED_{rec_id}.jpg")
    img.save(out_path, "JPEG", quality=95)
    subprocess.run(["termux-media-scan", out_path], check=False)

print(f"🟢 [OPSEC & COPYRIGHT CLEAN] Tarjeta generada exitosamente sin PII ni referencias a Nodos/Marcas: M82_CARD_HARD_SANITIZED_{rec_id}.jpg")
