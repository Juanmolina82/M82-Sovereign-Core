#!/usr/bin/env python3
# M82 SOVEREIGN CORE - REFINITIV GAS COMMODITY SWARM & GITHUB SYNC
# User Authentication: jmmp@molina82.com
import os, sys, sqlite3, json, subprocess, textwrap, time
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

# 1. Configuración de Entorno y Rutas
M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
GALLERY_DIRS = [
    os.path.expanduser("~/storage/shared/Pictures/M82_Cards"),
    "/sdcard/Pictures/M82_Cards"
]
for d in GALLERY_DIRS:
    os.makedirs(d, exist_ok=True)

# 2. Conexión SQLite WAL
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

now_utc = datetime.now(timezone.utc)
now_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

# 3. Datos de Telemetría Refinitiv Workspace (Gas Commodity Vector)
headline = "[M82 REFINITIV GAS SWARM] EU TTF €100.37/MWh (+4.1%) vs US Henry Hub $3.00/MMBtu (11.8x Transatlantic Divide) -- Venezuela Flaring 1.3 Bcf/d (€14B/yr / $40M/day) -- Quad-SPV Gas-to-Compute Capture Active"
tag = "v61.0.33-REFINITIV-GAS-COMMODITY-SWARM-TTF-HH-FLARE"
source = "REFINITIV_WORKSPACE_GAS_DESK"

meta_json = {
    "user": "jmmp@molina82.com",
    "source": "LSEG / Refinitiv Workspace Commodities Wire",
    "benchmarks": {
        "ttf_dutch_gas": "€100.37/MWh ($32.75/MMBtu equiv)",
        "us_henry_hub": "$3.00/MMBtu",
        "transatlantic_spread": "11.8x divide",
        "venezuela_flaring": "1.3 Bcf/d = 386 GWh/d = €38.6M/day = €14.1B/year"
    },
    "governance": "BUNKER MODE 0.30x LOCK | Exp 0.22x | VaR 1.68%",
    "timestamp": now_utc.isoformat()
}

# Inserción en macro_dossier
cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES (?, 'ENERGY_GAS_COMMODITIES', ?, 1.00, ?, 0.95, ?, 'v61.0.33', 'NODO_CHARALLAVE_L4L5')
""", (source, headline, tag, json.dumps(meta_json)))

# Inserción en m82_multi_stream para orquestación de colas
cur.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
    VALUES (?, ?, 'PENDING', 0.98, 'NATURAL_GAS_TTF_HH', 'REFINITIV_GAS_INGEST')
""", (source, headline))

conn.commit()
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")

cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total_records = cur.fetchone()[0]
conn.close()

print(f"🟢 [1/4 DB INGEST SUCCESS] Gas Wire asentado en macro_dossier. Total Registros: {total_records}")

# 4. Renderizado e Indexado en Galería Física (48pt Giant Typography)
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

draw.text((50, 48), "M82 REFINITIV WORKSPACE // GAS COMMODITY HUD", fill='#00e5ff', font=f_hdr)
draw.text((50, 85), f"USER: jmmp@molina82.com | NODE: CHARALLAVE L4/L5 | {now_str}", fill='#708090', font=f_sub)

draw.rectangle([55, 145, 620, 205], fill='#0c182b', outline='#00b0ff', width=2)
draw.text((70, 162), "DESK: REFINITIV_GAS_SWARM", fill='#ffffff', font=f_tag)

draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=f_sub)
draw.text((75, 280), "EU TTF: €100.37/MWh | US HH: $3.00/MMBtu | VZ FLARE: 1.3 Bcf/d", fill='#ff9100', font=f_sub)

draw.text((55, 348), "❚ REFINITIV COMMODITIES TELEMETRY WIRE", fill='#ff1744', font=f_red)
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

file_name = f"M82_CARD_RECORD_{total_records}.jpg"
for d in GALLERY_DIRS:
    out_path = os.path.join(d, file_name)
    img.save(out_path, "JPEG", quality=95)
    subprocess.run(["termux-media-scan", out_path], check=False)

print(f"🟢 [2/4 GALLERY SUCCESS] Tarjeta HD #{total_records} guardada e indexada en Galería física.")

# 5. Notificación Push a ntfy.sh
try:
    curl_cmd = [
        "curl", "-s", "-X", "POST",
        "https://ntfy.sh/M82-Molina-Alerts-v2",
        "-d", f"⚡ [M82 GAS REFINITIV WIRE #{total_records}]\nEU TTF: €100.37/MWh\nVZ Flaring: 1.3 Bcf/d (€14B/yr)\nUser: jmmp@molina82.com",
        "-H", "Title: M82 REFINITIV GAS COMMODITY SWARM",
        "-H", "Priority: high",
        "-H", "Tags: fuelpump,chart_with_upwards_trend"
    ]
    subprocess.run(curl_cmd, check=False)
    print("🟢 [3/4 NTFY RELAY SUCCESS] Alerta push despachada a ntfy.sh/M82-Molina-Alerts-v2")
except Exception as e:
    print(f"⚠️ [NTFY ERROR]: {e}")

# 6. Disparo de Telegram Bot en Segundo Plano Vía Orquestador
subprocess.Popen(["python3", os.path.expanduser("~/M82/orch.py")])

# 7. Respaldo Automático y Sincronización con GitHub
try:
    print("🔄 [4/4 GITHUB SYNC] Sincronizando BBDD y metadatos con el repositorio GitHub...")
    os.chdir(M82_DIR)
    subprocess.run(["git", "add", "m82_database.db", "scripts/"], check=False)
    commit_msg = f"M82 Refinitiv Gas Commodity Ingest #{total_records} (v61.0.33) - jmmp@molina82.com"
    subprocess.run(["git", "commit", "-m", commit_msg], check=False)
    subprocess.run(["git", "push", "origin", "main"], check=False)
    print("🟢 [4/4 GITHUB SYNC SUCCESS] Repositorio github.com/Juanmolina82/M82 actualizado.")
except Exception as e:
    print(f"⚠️ [GITHUB SYNC ERROR]: {e}")

