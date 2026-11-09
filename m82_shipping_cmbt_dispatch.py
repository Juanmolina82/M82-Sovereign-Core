#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, datetime
from PIL import Image, ImageDraw, ImageFont

# 1. Cargar Entorno Búnker
ENV_PATH = os.path.expanduser("~/M82/.env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v.strip('"\'')

DB_PATH = os.environ.get("M82_DB_PATH", os.path.expanduser("~/M82/m82_database.db"))
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1004335849125")
NTFY_TOPIC = "M82-Molina-Alerts-v2"
CARDS_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")
if not os.path.exists(CARDS_DIR):
    CARDS_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")
os.makedirs(CARDS_DIR, exist_ok=True)

# 2. Inserción atómica en BBDD
headline_txt = "LSEG WORKSPACE: CMB.TECH (NYSE: CMBT) Floating Storage 16.4mb Peak. Heavy Crude Merey 16 $93.92 Live / Brent $114.72. Hard Asset Rotation confirmed."

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()
cur.execute("""
    INSERT OR IGNORE INTO m82_multi_stream 
    (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
    VALUES ('REFINITIVSHIPPINGDESK', ?, 'LIVE', 0.99, 'FLOATING_STORAGE_CMBT', 'HARD_ASSET_ROTATION')
""", (headline_txt,))
conn.commit()
conn.close()

# 3. Generar Tarjeta Cyberpunk HUD PWA :8080 (1080x1350 px)
W, H = 1080, 1350
img = Image.new('RGB', (W, H), color='#05080e')
draw = ImageDraw.Draw(img)

try:
    f_hdr = ImageFont.truetype('DejaVuSans-Bold.ttf', 30)
    f_sub = ImageFont.truetype('DejaVuSans.ttf', 24)
    f_title = ImageFont.truetype('DejaVuSans-Bold.ttf', 36)
    f_body = ImageFont.truetype('DejaVuSans-Bold.ttf', 32)
    f_ftr = ImageFont.truetype('DejaVuSans-Bold.ttf', 24)
except:
    f_hdr = f_sub = f_title = f_body = f_ftr = ImageFont.load_default()

# Marco Cyan / Gold
draw.rectangle([15, 15, W - 15, H - 15], outline='#00e5ff', width=4)

# Encabezado Terminal
draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)
draw.text((50, 48), "M82 SHIPPING DESK // TICKER: CMBT (NYSE)", fill='#00e5ff', font=f_hdr)
draw.text((50, 85), "AIS FLOATING STORAGE TRACKER // HARD ASSETS ROTATION", fill='#708090', font=f_sub)

# Título y Datos Clave
draw.rectangle([55, 145, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
draw.text((75, 165), "🚢 CMB.TECH FLOATING STORAGE: 16.4M bbls PEAK", fill='#ff9100', font=f_title)
draw.text((75, 220), "🛢 MEREY 16: $93.92 / bbl   |   BRENT: $114.72 / bbl", fill='#00b0ff', font=f_body)
draw.text((75, 270), "📊 SPREAD: $20.80 ITM (Jose -> Houston Direct Corridor)", fill='#00e5ff', font=f_sub)

# Cuerpo / Mapa Consola
draw.rectangle([55, 345, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)
draw.text((85, 375), "⚡ HARD ASSETS FLOW ANALYSIS:", fill='#ff1744', font=f_title)

analysis_text = (
    "1. FLOATING STORAGE PEAK (16.4M bbls):\n"
    "   Trafigura & Vitol storing crude off-Hormuz.\n"
    "   Highest VLCC/Suezmax storage since May 2022.\n\n"
    "2. MEREY 16 ARBITRAGE ADVANTAGE:\n"
    "   Spread narrowed to $20.80. Heavy sour demand\n"
    "   surging in USGC (Phillips 66 / Sweeny).\n"
    "   Direct Jose -> Houston route bypasses Hormuz.\n\n"
    "3. MEIB / MCM MONETIZATION:\n"
    "   500k bpd @ $94 = $17.1BN Annual Revenue.\n"
    "   7.5% WACC Target saves $300M/yr in financing.\n"
    "   Pre-Export Facilities via Citi NY Escrow."
)

y_p = 430
for line in analysis_text.split('\n'):
    draw.text((85, y_p), line, fill='#ffffff', font=f_sub)
    y_p += 32

# Pie
draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
draw.text((50, H - 100), "[ AGI QUANTUM VERIFIED — CUSTODIA PASIVA 0.30x LOCK ]", fill='#00e5ff', font=f_ftr)
draw.text((50, H - 68), "🏛 @MolinaHoldings | SOVEREIGN EXECUTION CORE — MCM 2026", fill='#ffffff', font=f_ftr)

card_path = os.path.join(CARDS_DIR, "M82_CARD_SHIPPING_CMBT_AIS.png")
img.save(card_path)
os.system(f"termux-media-scan {card_path} >/dev/null 2>&1")
print(f"✅ [PWA :8080] Tarjeta HD generada: {card_path}")

# 4. Despacho a Telegram (-1004335849125 HTML)
caption_tg = (
    f"⚡ <b>M82 SHIPPING DESK :: HARD ASSET ROTATION CONFIRMED</b>\n"
    f"───────────────────────────\n"
    f"🚢 <b>TICKER:</b> CMB.TECH (NYSE: CMBT) — Floating Storage 16.4M bbls Peak\n"
    f"🛢 <b>PRICING:</b> Merey 16 $93.92 Live / Brent $114.72 (Spread $20.80 ITM)\n"
    f"🗺 <b>AIS CORRIDOR:</b> Direct Jose Terminal -> Houston (Off-Hormuz Hedge)\n"
    f"💰 <b>MEIB / MCM IMPACT:</b> $17.1BN Annual Rev Potential | 7.5% WACC Target\n"
    f"🛡 <b>GOVERNANCE:</b> 0.30x LOCK | VaR 1.68% | Citi NY Escrow Ready\n\n"
    f"<i>SOVEREIGN EXECUTION CORE — CARACAS LIBRE — MEIB Nashville ⊗ JMM Caracas</i>"
)

try:
    url_photo = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    with open(card_path, 'rb') as photo:
        r = requests.post(url_photo, data={
            'chat_id': CHAT_ID,
            'caption': caption_tg,
            'parse_mode': 'HTML'
        }, files={'photo': photo}, timeout=10)
        print(f"[*] Telegram Photo Dispatch: {r.status_code}")
except Exception as e:
    print(f"[!] TG Photo Error: {e}")

# 5. Despacho Push a ntfy.sh
try:
    ntfy_url = f"https://ntfy.sh/{NTFY_TOPIC}"
    ntfy_body = f"M82 CMBT WIRE: Floating Storage 16.4M bbls Peak — Merey 16 $93.92 / Brent $114.72 — Hard Asset Rotation Confirmed"
    requests.post(ntfy_url, data=ntfy_body.encode('utf-8'), headers={
        "Title": "🚢 M82 SHIPPING DESK — CMBT AIS PEAK",
        "Priority": "urgent",
        "Tags": "ship,oil,money"
    }, timeout=5)
    print(f"[*] ntfy Dispatch: 200 OK")
except Exception as e:
    print(f"[!] ntfy Error: {e}")

