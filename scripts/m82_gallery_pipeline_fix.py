#!/usr/bin/env python3
import os, sys, sqlite3, subprocess
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone

# Rutas públicas visibles por la Galería de Android
TARGET_DIRS = [
    os.path.expanduser("~/storage/shared/Pictures/M82_Cards"),
    "/sdcard/Pictures/M82_Cards"
]

for d in TARGET_DIRS:
    os.makedirs(d, exist_ok=True)

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Consultar el registro #147 en SQLite
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
cur = conn.cursor()
cur.execute("SELECT id, source, category, headline, m82_tag, version FROM macro_dossier ORDER BY id DESC LIMIT 1")
row = cur.fetchone()
conn.close()

if row:
    evt_id, source, category, headline, tag, version = row
else:
    evt_id, source, category, headline, tag, version = (
        147, "M82_TELEMETRY_ENGINE", "GLOBAL_MACRO_ENERGY_SWARM",
        "[M82 TELEMETRY SWARM v61.0.30] WTI $102.80 Backwardation Boosts Implied Merey 16 Net ($88.80-$90.50) -- Tether/Circle $2.54B Freeze Restores Market Stability -- Delaware Quad-SPV Active",
        "v61.0.30-M82-SWARM-ENERGY-CRYPTO-DELAWARE-SPV", "v61.0.30"
    )

# Fuentes
def get_font(size):
    for p in ["/system/fonts/Roboto-Bold.ttf", "/system/fonts/DroidSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

f_hdr = get_font(30)
f_sub = get_font(26)
f_tag = get_font(28)
f_red = get_font(32)
f_body = get_font(48) # Texto Gigante 48pt
f_ftr = get_font(24)

W, H = 1080, 1350
img = Image.new('RGB', (W, H), color='#040812')
draw = ImageDraw.Draw(img)

draw.rectangle([15, 15, W - 15, H - 15], outline='#00e5ff', width=4)
draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)

now_str = datetime.now(timezone.utc).strftime("%H:%M:%S ET")
draw.text((50, 48), "M82 SOVEREIGN MONITOR // QUANTUM TERMINAL HUD", fill='#00e5ff', font=f_hdr)
draw.text((50, 85), f"NODE PRIMARY EDGE L5 | USER: jmmp@molina82.com | {now_str}", fill='#708090', font=f_sub)

draw.rectangle([55, 145, 620, 205], fill='#0c182b', outline='#00b0ff', width=2)
draw.text((70, 162), f"DESK: {category[:26]}", fill='#ffffff', font=f_tag)

draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=f_sub)
draw.text((75, 280), "BENCHMARKS: WTI $102.80 | MEREY 16: $88.80-$90.50 NET", fill='#ff9100', font=f_sub)

draw.text((55, 348), "❚ M82 TELEMETRY WIRE DISPATCH", fill='#ff1744', font=f_red)
draw.line([(55, 388), (W - 55, 388)], fill='#ff1744', width=3)

draw.rectangle([55, 405, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)

import textwrap
lines = textwrap.wrap(headline, width=22)
y_pos = 440
for line in lines[:9]:
    draw.text((85, y_pos), line, fill='#ffffff', font=f_body)
    y_pos += 68

draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
draw.text((50, H - 100), "[ AGI QUANTUM VERIFIED -- CUSTODIA PASIVA 0.30x LOCK ]", fill='#00e5ff', font=f_ftr)
draw.text((50, H - 68), "❚ @MolinaHoldings | Sovereign Execution Node", fill='#ffffff', font=f_ftr)

# Guardar en ambas carpetas públicas
file_name = f"M82_CARD_RECORD_{evt_id}.jpg"
for d in TARGET_DIRS:
    target_path = os.path.join(d, file_name)
    img.save(target_path, "JPEG", quality=95)
    # Disparar escáner de Android
    subprocess.run(["termux-media-scan", target_path], check=False)

print(f"🟢 [SUCCESS] Tarjeta #{evt_id} enviada e indexada en la Galería de fotos.")
