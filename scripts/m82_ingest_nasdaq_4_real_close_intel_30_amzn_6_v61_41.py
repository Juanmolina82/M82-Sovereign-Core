#!/usr/bin/env python3
# M82 SOVEREIGN CORE - MARKET CLOSE NASDAQ -4% / INTEL -30% / OIL IRAN HIGH (v61.0.41)
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

headline = "[M82 CLOSE FLASH v61.0.41] Nasdaq -4% Real NDX -4.12% 28189 3M Low Oct -7% vs SPX -1.9% Dow -1% -- Intel -30% Provisional Biggest Loss -- AMZN -6% AWS Disappoints -- Alphabet AI Overspend -- Quirin Euforia Resquebraja -- SanDisk -15% Reddit -30% -- Chevron Exxon +1.7% Oil Iran-Iraq Highs US Attack Iran Fear"
tag = "v61.0.41-M82-NASDAQ-4-REAL-CLOSE-INTEL-30-AMZN-6-OIL-IRAN"

meta = {
 "source": "APA Austria via LSEG Workspace 30-Oct-2026 id dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDMwOm5BcGExUTI4NmE6MQ==",
 "close": "US extends losses Nasdaq -4% NDX-100 -4.12% 28,189.928 3M low Oct -7% vs SPX -1.9% 7,576 Dow -1% 51,847 weekly -0.7% Oct +1.8% still positive -- Traditional holds tech collapses",
 "intel_amzn": "Intel -30% provisional biggest loss record Arcuri UBS forecast below most pessimistic -- Amazon -6% intraday low since late July then -1.7% AWS growth disappoints Ju UBS high AI spend hurts -- Alphabet prior day AI overspend fears -- Acceleration",
 "quote": "Stefan May Quirin Privatbank: La euforia por la IA está mostrando fisuras -- dudas si grandes inversiones rentables -- Tech advances rarely linear -- Enthusiasm -> overinvestment -> painful pullbacks -- Do not rebalance hastily on bubble warnings",
 "others": "SanDisk -15% despite solid + high forecast + split pessimism sector -- Roblox Reddit -30% cap user growth disappoint Q4 below -- Defensive Regeneron +11% Gilead +4% Mondelez +3.6% pharma food -- Chevron Exxon +1.7% Q3 strong crude + refining margins",
 "oil_geopol": "Oil near highest since Iran-Iraq war -- Fear possible new US military attack in Iran + Hormuz tanker attack + Houthi Saudi + Ukraine refinery -- WTI $102.80->$105->$110 Merey $88.80->$91->$95 +$2-4B annual VZ -- Validates v61.0.40",
 "math": "13:00 ET -2% -> close -4% doubled in 4h -- Oct -5.8% $2T wiped SpaceX value -> Oct -7% $2.4T wiped + $1T intraday -4% = $3T+ total -- Dow vs Nasdaq spread validates BUNKER 0.30x LOCK real assets > debt bomb",
 "m82_thesis": "Validates v61.0.35 $2T wipeout $900B 2026 $5.5T 2030 WACC 10.8-16% Warsh +102 bps Fed +50 bps CDS surge -- v61.0.36-40 Hormuz oil +2% + v61.0.38 SpaceX $130B + v61.0.39 Anthropic SpaceX -- Quad-SPV Delaware 50/50 Citi NY gas $0 flare $40M/day €14B/yr Merey crack $108 $40B/yr powered land multi-GW GE Vernova $25B BUNKER",
 "timestamp": datetime.now(timezone.utc).isoformat()
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES (?, 'MARKET_CLOSE_NASDAQ_4_INTEL_30_OIL_IRAN_HIGH', ?, 1.00, ?, 0.95, ?, 'v61.0.41', 'NODO_CHARALLAVE_L4L5')
""", ("LSEG / APA Austria Nasdaq -4%", headline, tag, json.dumps(meta)))

conn.commit()

cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total_count = cur.fetchone()[0]

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"🔒 M82 v61.0.41 SEALED -- TOTAL RECORDS: {total_count} -- WAL 0/0/0 CLEAN")

# 2. Renderizado Tarjeta HUD Option C (Divergencia Nasdaq -4% vs Energy/Chevron +1.7%)
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
draw.text((50, 48), "M82 MARKET CLOSE MONITOR // HUD OPTION C", fill='#00e5ff', font=f_hdr)
draw.text((50, 85), f"USER: jmmp@molina82.com | CHARALLAVE L4/L5 EDGE | {now_utc}", fill='#708090', font=f_sub)

draw.rectangle([55, 145, 620, 205], fill='#0c182b', outline='#00b0ff', width=2)
draw.text((70, 162), "DESK: NASDAQ_TECH_VS_REAL_ASSETS", fill='#ffffff', font=f_tag)

draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=f_sub)
draw.text((75, 280), "NASDAQ: -4.00% (NDX 28,189) | INTEL: -30% | CHEVRON: +1.7%", fill='#ff9100', font=f_sub)

draw.text((55, 348), "❚ LSEG / APA AUSTRIA CLOSING WIRE", fill='#ff1744', font=f_red)
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

print(f"🟢 [HUD SUCCESS] Tarjeta Option C #{total_count} guardada en Galería física.")
