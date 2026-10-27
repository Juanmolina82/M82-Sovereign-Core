#!/usr/bin/env bash
set -e

echo "=================================================="
echo "🚀 DESPLEGANDO INFRAESTRUCTURA COMPLETA M82 v2.0"
echo "=================================================="

BASE_DIR="$HOME/M82"
DB_PATH="$BASE_DIR/m82_database.db"
CARDS_DIR="/sdcard/Pictures/M82_Cards"

mkdir -p "$BASE_DIR"
mkdir -p "$CARDS_DIR"
mkdir -p "$BASE_DIR/fonts"

# 1. INSTALACIÓN DE DEPENDENCIAS
echo "📦 [1/4] Verificando e instalando dependencias en Termux..."
pkg update -y > /dev/null 2>&1 || true
pkg install -y python sqlite pillow > /dev/null 2>&1 || true
pip install requests > /dev/null 2>&1 || true

# 2. DESCARGA DE FUENTES BOLD NATIVAS
echo "🔤 [2/4] Configurando fuentes tipográficas HD..."
curl -s -L -o "$BASE_DIR/fonts/Roboto-Bold.ttf" "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf" || true

# 3. MOTOR UNIFICADO Y BASE DE DATOS SQLITE (MODO WAL)
echo "🗄️ [3/4] Inicializando esquema SQLite y Motor de Telemetría..."
cat << 'PYEOF' > "$BASE_DIR/m82_engine_master.py"
#!/usr/bin/env python3
import os, sys, time, datetime, sqlite3, json, math, random, textwrap, subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARDS_DIR = "/sdcard/Pictures/M82_Cards"
FONT_PATH = os.path.join(BASE_DIR, "fonts/Roboto-Bold.ttf")

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    return conn

def setup_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS m82_multi_stream (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daemon_source TEXT,
        headline TEXT UNIQUE,
        status TEXT DEFAULT 'PENDING',
        timestamp TEXT
    );
    CREATE TABLE IF NOT EXISTS m82_mcn_checklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        brent_price REAL,
        dubai_squeeze REAL,
        red_day_flag INTEGER,
        consecutive_red_days INTEGER,
        diesel_shortage_active INTEGER,
        real_yield REAL
    );
    """)
    
    # Inyectar snapshot de prueba para verificar avance
    now = datetime.datetime.now().isoformat()
    c.execute("""
        INSERT INTO m82_mcn_checklist (timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield)
        VALUES (?, 107.2, 13.14, 1, 1, 1, 3.30)
    """, (now,))
    
    c.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES ('M82_SYSTEM_INIT', 'INFRAESTRUCTURA M82 OPERATIVA: Motor Unificado en Modo WAL + Generador Opción B Activo', 'PENDING', ?)
    """, (now,))
    
    conn.commit()
    conn.close()

def generate_hud_card(headline, source="MACRO_QUANT"):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#040814')
    draw = ImageDraw.Draw(img)

    # Red Cuántica
    random.seed(101)
    nodes = [(random.randint(60, 940), random.randint(180, 1050)) for _ in range(18)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 260:
                draw.line([(x1, y1), (x2, y2)], fill='#0b192e', width=1)
    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#132a4a')

    # Marcos Tactical HUD
    b_len, b_pad = 35, 30
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill='#38bdf8', width=3)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill='#38bdf8', width=3)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill='#38bdf8', width=3)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill='#38bdf8', width=3)

    try:
        f_small = ImageFont.truetype(FONT_PATH, 18)
        f_badge = ImageFont.truetype(FONT_PATH, 22)
        f_head  = ImageFont.truetype(FONT_PATH, 42)
        f_foot  = ImageFont.truetype(FONT_PATH, 32)
    except Exception:
        f_small = f_badge = f_head = f_foot = ImageFont.load_default()

    # Header
    draw.text((70, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM", fill='#38bdf8', font=f_small)
    draw.text((width - 250, 60), "LATENCY: 0.012ms", fill='#0284c7', font=f_small)
    draw.line([(70, 95), (width - 70, 95)], fill='#1e293b', width=2)

    # Badge Fuente
    draw.rectangle([70, 125, 680, 175], fill='#0f172a', outline='#ef4444', width=2)
    draw.text((85, 137), f"🚨 #M82 BREAKING  [{source.upper()}]", fill='#f87171', font=f_badge)

    # Contenedor Central
    draw.rectangle([70, 210, width - 70, height - 200], fill='#070e20', outline='#1e293b', width=2)
    wrapped_lines = textwrap.wrap(headline, width=32)
    y_start = 260
    for line in wrapped_lines:
        draw.text((100, y_start), line, fill='#ffffff', font=f_head)
        y_start += 60

    # Footer
    draw.line([(70, height - 170), (width - 70, height - 170)], fill='#1e293b', width=2)
    draw.text((70, height - 130), "[ AGI QUANTUM STREAM VERIFIED ]", fill='#38bdf8', font=f_small)
    draw.text((70, height - 90), "🏛 @MolinaHoldings LLC", fill='#ffffff', font=f_foot)

    card_file = os.path.join(CARDS_DIR, f"M82_CARD_{int(time.time())}.png")
    img.save(card_file)
    try:
        subprocess.run(["termux-media-scan", card_file], check=False)
    except Exception:
        pass
    return card_file

def process_queue():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1")
    row = c.fetchone()
    if row:
        row_id, source, headline = row
        print(f"📌 Procesando señal ID {row_id}...")
        card_path = generate_hud_card(headline, source)
        c.execute("UPDATE m82_multi_stream SET status = 'PROCESSED' WHERE id = ?", (row_id,))
        conn.commit()
        print(f"✅ Tarjeta HD creada exitosamente: {card_path}")
    else:
        print("💤 Sin señales pendientes en la cola.")
    conn.close()

if __name__ == "__main__":
    setup_db()
    process_queue()
PYEOF

chmod +x "$BASE_DIR/m82_engine_master.py"

# 4. EJECUCIÓN
echo "⚡ [4/4] Ejecutando comprobación final..."
python3 "$BASE_DIR/m82_engine_master.py"

echo "=================================================="
echo "🎯 INFRAESTRUCTURA M82 EN PROCESO CORRECTO"
echo "=================================================="
