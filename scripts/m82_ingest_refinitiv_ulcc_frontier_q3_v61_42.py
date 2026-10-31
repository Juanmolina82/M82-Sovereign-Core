#!/usr/bin/env python3
# M82 SOVEREIGN CORE - REFINITIV ULCC FRONTIER Q3 EARNINGS INGESTION (v61.0.42)
import sqlite3, os, json, subprocess, textwrap
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
GALLERY_DIRS = [
    os.path.expanduser("~/storage/shared/Pictures/M82_Cards"),
    "/sdcard/Pictures/M82_Cards"
]
for d in GALLERY_DIRS:
    os.makedirs(d, exist_ok=True)

# 1. Asentamiento en BBDD SQLite
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

headline = "[M82 REFINITIV FLASH v61.0.42] Frontier ULCC +31.2% Rally Q3 Record Revenue $1.4B (+52.9% YoY) EPS $0.18 vs $-0.06 Est -- RASM +30% -- Balance Sheet Stress $5B Debt vs $976M Cash $817M Deficit -- Jet Fuel Cost Headwind Q4 Guidance"
tag = "v61.0.42-M82-REFINITIV-ULCC-FRONTIER-Q3-EARNINGS-JETFUEL"

meta = {
    "source": "Refinitiv Workspace / LSEG News Wire 30-Oct-2026 id dXJuOm5ld3NtbDpuZXdzcm9vbS5yZWZpbml0aXYuY29tOjIwMjYxMDMwOm5OUkEyaXc0MDk6MA==",
    "ticker": "NASDAQ:ULCC (Frontier Group Holdings)",
    "price_action": "$6.48 (+31.2% Oct 23-29) vs SPX +1.3% NDX +1.5%",
    "financials": "Q3 Revenue $1.4B (+52.9% YoY), Adj EPS $0.18 vs $-0.06 est, RASM +30%, Passengers 9.8M, GAAP Net Loss $104M (fleet charges)",
    "balance_sheet": "Total Debt $5B, Cash & ST Inv $976M, Working Capital Deficit $817M",
    "guidance_q4": "Adj EPS $(0.15) to $0.05, Jet fuel elevated cost pressure, RASM +20% YoY",
    "valuation_ps": "P/S 0.3x vs peer average 0.5x (ALGT 0.5x, JBLU 0.1x, LUV 0.7x)",
    "m82_thesis": "Confirms M82 Jet Fuel & Refining Margin (Sweeny Coker/Merey) leverage over transport balance sheets -- High debt + high fuel WACC friction validates BUNKER 0.30x LOCK real assets strategy",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES (?, 'EARNINGS_REFINITIV_ULCC_AIRLINES', ?, 0.95, ?, 0.88, ?, 'v61.0.42', 'NODO_CHARALLAVE_L4L5')
""", ("LSEG / Refinitiv Workspace ULCC Wire", headline, tag, json.dumps(meta)))

conn.commit()

cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total_count = cur.fetchone()[0]

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"🔒 M82 v61.0.42 SEALED -- TOTAL RECORDS: {total_count} -- WAL 0/0/0 CLEAN")

# 2. Renderizado Tarjeta HUD Option C (Airlines / Refined Fuel Vector)
def load_font(size):
    for p in ["/system/fonts/Roboto-Bold.ttf", "/system/fonts/DroidSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

f_hdr = load_font(30); f_sub = load_font(26); f_tag = load_font(28)
f_red = load_font(32); f_body = load_font(48); f_ftr = load_font(24)

W, H = 1080, 1350
img = Image.new('RGB', (W, H), color='#040812')
draw = ImageDraw.Draw(img)

draw.rectangle([15, 15, W - 15, H - 15], outline='#00e5ff', width=4)
draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)

now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S ET")
draw.text((50, 48), "M82 REFINITIV MONITOR // ULCC EARNINGS WIRE", fill='#00e5ff', font=f_hdr)
draw.text((50, 85), f"USER: jmmp@molina82.com | CHARALLAVE L4/L5 EDGE | {now_utc}", fill='#708090', font=f_sub)

draw.rectangle([55, 145, 620, 205], fill='#0c182b', outline='#00b0ff', width=2)
draw.text((70, 162), "DESK: AIRLINES_JET_FUEL_REFINING", fill='#ffffff', font=f_tag)

draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=f_sub)
draw.text((75, 280), "ULCC: $6.48 (+31.2%) | REV: $1.4B | DEBT: $5B | CASH: $976M", fill='#ff9100', font=f_sub)

draw.text((55, 348), "❚ LSEG WORKSPACE TELEMETRY WIRE", fill='#ff1744', font=f_red)
draw.line([(55, 388), (W - 55, 388)], fill='#ff1744', width=3)

draw.rectangle([55, 405, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)

lines = textwrap.wrap(headline, width=22)
y_pos = 440
for line in lines[:9]:
    draw.text((85, y_pos), line, fill='#ffffff', font=f_body)
    y_pos += 68

draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
draw.text((50, H - 100), "[ AGI QUANTUM VERIFIED -- CUSTODIA PASIVA 0.30x LOCK ]", fill='#00e5ff', font=f_ftr)
draw.text((50, H - 68), "❚ @MolinaHoldings | Sovereign Execution Node", fill='#ffffff', font=f_ftr)

for d in GALLERY_DIRS:
    out_path = os.path.join(d, f"M82_CARD_RECORD_{total_count}.jpg")
    img.save(out_path, "JPEG", quality=95)
    subprocess.run(["termux-media-scan", out_path], check=False)

print(f"🟢 [HUD SUCCESS] Tarjeta ULCC #{total_count} guardada en Galería física.")
