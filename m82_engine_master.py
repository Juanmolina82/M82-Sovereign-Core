#!/usr/bin/env python3
import os, sys, time, datetime, sqlite3, json, math, random, textwrap, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARDS_DIR_PRIMARY = "/storage/emulated/0/M82card"
CARDS_DIR_LEGACY = "/sdcard/Pictures/M82_Cards"
FONT_PATH = os.path.join(BASE_DIR, "fonts/Roboto-Bold.ttf")

os.makedirs(CARDS_DIR_PRIMARY, exist_ok=True)
os.makedirs(CARDS_DIR_LEGACY, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def setup_db_and_seed_today():
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

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Snapshot real 20 Nov 2026 (Brent $90.70, UST 10Y 4.944%)
    c.execute("""
        INSERT INTO m82_mcn_checklist (timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield)
        VALUES (?, 90.70, 8.43, 1, 2, 0, 4.944)
    """, (now,))

    session_cards = [
        ("AI_VIX_SHOCK", "VIX +12.38% A 31.96 | SOX -8.69%, ANT.O -12.32% ($85.20), NBIS -18.14%, NVDA -7% | SPX 7,013 (-2.26%) Y NASDAQ 22,995 (-3.70%) EN CORRECCION | BUNKER 0.30x LOCK"),
        ("FED_HAWKISH", "FED LISA COOK: TASA ACTUAL INSUFICIENTE VS INFLACION | CME FEDWATCH DESCUENTA 98.2% DE ALZA EN DICIEMBRE | UMICH 51.5 (INFL 1Y 3.7%) | UST 10Y 4.944%"),
        ("SECTOR_ROTATION", "ROTACION DEFENSIVA LSEG: STAPLES +1.57%, COMMSRV +1.37%, HEALTH +0.99% VS INFOTECH -4.5% | DOW 48,753 TESTEA SOPORTE FIBONACCI 61.8% (48,757) | AAII -8.9%"),
        ("METALS_CRYPTO", "LIQUIDEZ TRANS-ACTIVO: ORO XAU $3,575.52 (-1.28%) | PLATA SIc1 BEAR FLAG ($37.84-$39.60) | BRENT $90.70 | WTI $82.27 | DXY 103.76 | BITCOIN $59,418-$61,622"),
        ("US_IRAN_GEOPOL", "TRUMP SOBRE IRAN: QUIEREN ACUERDO PERO NO UNO ACEPTABLE | PRIMA EN ORMUZ REVALORIZA CRUDO PESADO HEMISFERICO PARA REFINERIAS PADD 3 DE EE.UU."),
        ("VENEZUELA_CITGO", "HOJA DE RUTA @MariaCorinaYA: CONGELAR SUBASTA CITGO ANTES DEL 18-DIC, CANJE GLOBAL DE DEUDA (15-25 ANOS) CON FMI, TRANSPARENCIA Y ELECCIONES 2027")
    ]

    for src, hl in session_cards:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (src, hl, now))

    c.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

def notify_android_gallery(filepath):
    try:
        subprocess.Popen(
            ["am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{filepath}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass

def generate_hud_card(headline, source="MACRO_QUANT", row_id=0):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#040814')
    draw = ImageDraw.Draw(img)

    # Red Cuántica (Estética Opción B)
    random.seed(101 + row_id)
    nodes = [(random.randint(60, 940), random.randint(180, 1050)) for _ in range(20)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 260:
                draw.line([(x1, y1), (x2, y2)], fill='#0b192e', width=1)
    for x, y in nodes:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#132a4a')

    # Esquinas Tactical HUD (#38bdf8)
    b_len, b_pad = 35, 30
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill='#38bdf8', width=3)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill='#38bdf8', width=3)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill='#38bdf8', width=3)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill='#38bdf8', width=3)
    draw.line([(b_pad, height - b_pad), (b_pad + b_len, height - b_pad)], fill='#38bdf8', width=3)
    draw.line([(b_pad, height - b_pad), (b_pad, height - b_pad - b_len)], fill='#38bdf8', width=3)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad - b_len, height - b_pad)], fill='#38bdf8', width=3)
    draw.line([(width - b_pad, height - b_pad), (width - b_pad, height - b_pad - b_len)], fill='#38bdf8', width=3)

    try:
        f_small = ImageFont.truetype(FONT_PATH, 18)
        f_badge = ImageFont.truetype(FONT_PATH, 22)
        f_head  = ImageFont.truetype(FONT_PATH, 38)
        f_risk  = ImageFont.truetype(FONT_PATH, 20)
        f_foot  = ImageFont.truetype(FONT_PATH, 30)
    except Exception:
        f_small = f_badge = f_head = f_risk = f_foot = ImageFont.load_default()

    # Header
    draw.text((70, 60), "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM", fill='#38bdf8', font=f_small)
    draw.text((width - 250, 60), "LATENCY: 0.012ms", fill='#0284c7', font=f_small)
    draw.line([(70, 95), (width - 70, 95)], fill='#1e293b', width=2)

    # Badge Fuente (#ef4444)
    draw.rectangle([70, 122, 740, 174], fill='#0f172a', outline='#ef4444', width=2)
    draw.text((88, 136), f"[!] #M82 BREAKING  [{source.upper()}]", fill='#f87171', font=f_badge)

    # Contenedor Central
    draw.rectangle([70, 205, width - 70, height - 225], fill='#070e20', outline='#1e293b', width=2)
    wrapped_lines = textwrap.wrap(headline, width=33)[:11]
    y_start = 245
    for line in wrapped_lines:
        draw.text((98, y_start), line, fill='#ffffff', font=f_head)
        y_start += 56

    # Barra de Gobernanza Bunker
    draw.rectangle([70, height - 205, width - 70, height - 160], fill='#1c0a10', outline='#ef4444', width=1)
    draw.text((88, height - 193), "BUNKER 0.30x LOCK | EXP: 0.22x | VaR: 1.68% | WARSH: +102.0 bps", fill='#fca5a5', font=f_risk)

    # Footer
    draw.text((70, height - 135), "[ AGI QUANTUM STREAM VERIFIED ] :: CHARALLAVE L4/L5 EDGE", fill='#38bdf8', font=f_small)
    draw.text((70, height - 95), "M82 SOVEREIGN CORE // @MolinaHoldings LLC", fill='#ffffff', font=f_foot)

    ts_tag = f"{int(time.time())}_{row_id}"
    card_primary = os.path.join(CARDS_DIR_PRIMARY, f"M82_CARD_{ts_tag}.png")
    card_legacy = os.path.join(CARDS_DIR_LEGACY, f"M82_CARD_{ts_tag}.png")

    img.save(card_primary, "PNG")
    shutil.copy2(card_primary, card_legacy)

    notify_android_gallery(card_primary)
    notify_android_gallery(card_legacy)
    return card_primary

def process_all_pending():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE status = 'PENDING' ORDER BY id ASC LIMIT 25")
    rows = c.fetchall()
    for row_id, source, headline in rows:
        card_path = generate_hud_card(headline or "", source or "MACRO_QUANT", row_id)
        c.execute("UPDATE m82_multi_stream SET status = 'PROCESSED' WHERE id = ?", (row_id,))
        print(f"✅ Tarjeta Opción B HD creada (#{row_id}): {card_path}")
    if rows:
        c.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

if __name__ == "__main__":
    setup_db_and_seed_today()
    process_all_pending()
    while True:
        time.sleep(15)
        process_all_pending()
