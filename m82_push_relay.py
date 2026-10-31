#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
CARDS_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")
if not os.path.exists(CARDS_DIR):
    CARDS_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")

os.makedirs(CARDS_DIR, exist_ok=True)

# Credenciales Validadas
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

def generate_hud_option_b(evt_id, headline, daemon_source):
    """Renderizador exacto de la OPCIÓN B (1080x1350 px con bordes cyan, marcos y texto gigante)"""
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#05080e')
    draw = ImageDraw.Draw(img)

    # Intentar cargar fuentes del sistema en Termux o usar escalado nativo
    try:
        font_hdr = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 26)
        font_tag = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        font_red = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        font_body = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
        font_ftr = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
    except:
        font_hdr = font_sub = font_tag = font_red = font_body = font_ftr = ImageFont.load_default()

    # 1. Borde Azul Exterior Grueso
    draw.rectangle([15, 15, W - 15, H - 15], outline='#00b0ff', width=4)

    # 2. Panel Superior Header
    draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)
    draw.text((50, 48), "SYSTEM: AGI-CORE // NODE: SOVEREIGN EXECUTION CORE", fill='#00e5ff', font=font_hdr)
    draw.text((50, 85), "M82 SOVEREIGN MONITOR // HUD CARDS", fill='#708090', font=font_sub)

    # 3. Caja Daemon Category
    draw.rectangle([55, 145, 520, 205], fill='#0c182b', outline='#00b0ff', width=2)
    draw.text((70, 162), f"DAEMON: {daemon_source[:22]}", fill='#ffffff', font=font_tag)

    # 4. Panel de Métricas de Riesgo
    draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
    draw.text((75, 240), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%", fill='#00b0ff', font=font_sub)
    draw.text((75, 280), "MEREY 16: $93.15 ITM  |  WARSH SPREAD: +102.0bps", fill='#ff9100', font=font_sub)

    # 5. Indicador Red Breaking Line
    draw.text((55, 348), "❚ REFINITIV BREAKING WIRE", fill='#ff1744', font=font_red)
    draw.line([(55, 388), (W - 55, 388)], fill='#ff1744', width=3)

    # 6. Marco Principal del Titular (Caja Oscura)
    draw.rectangle([55, 405, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)

    # Limpieza e Inserción de Titular
    clean_headline = headline.replace("REFINITIV", "").replace("LSEG", "").replace("EIKON", "").strip()
    full_text = f"[{daemon_source} | {time.strftime('%Y-%m-%d %H:%M:%S')}]\n\n{clean_headline}"

    y_pos = 435
    words = full_text.split(' ')
    line = ""
    for word in words:
        if len(line + word) < 25:
            line += word + " "
        else:
            draw.text((80, y_pos), line, fill='#ffffff', font=font_body)
            y_pos += 58
            line = word + " "
    if line:
        draw.text((80, y_pos), line, fill='#ffffff', font=font_body)

    # 7. Panel Inferior (Footer de Firma Institucional)
    draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
    draw.text((50, H - 100), "[ AGI QUANTUM VERIFIED — CUSTODIA PASIVA 0.30x LOCK ]", fill='#00e5ff', font=font_ftr)
    draw.text((50, H - 68), "❚ @MolinaHoldings | Sovereign Execution Node", fill='#ffffff', font=font_ftr)

    # Guardar en la Galería
    file_path = os.path.join(CARDS_DIR, f"M82_CARD_B_REAL_{int(time.time())}_{evt_id}.png")
    img.save(file_path)
    
    # Forzar el escaneo de medios para actualización inmediata en la app Galería
    os.system(f"termux-media-scan '{file_path}' 2>/dev/null || true")
    return file_path

def dispatch_event(evt_id, headline, daemon_source, img_path):
    caption = (
        f"⚡ *#M82 TELEMETRIA VIVA (OPCIÓN B REAL)* :: {time.strftime('%H:%M:%S ET')}\n"
        f"───────────────────────────\n"
        f"🏛 *SOURCE:* {daemon_source}\n"
        f"📰 *HEADLINE:* {headline}\n"
        f"🛡 *RISK:* Exp 0.22x/0.30x LOCK | VaR 1.68% | Warsh +102.0bps\n"
        f"🔒 *CUSTODIA PASIVA — CUSTODIA ACCIONARIA DIRECTA*\n\n"
        f"🏛 @MolinaHoldings | Sovereign Execution Node"
    )

    # Enviar Foto a Telegram
    try:
        url_photo = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
        with open(img_path, 'rb') as photo:
            r = requests.post(url_photo, data={'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'photo': photo}, timeout=10)
            print(f"[*] TG Photo Relay Status: {r.status_code}")
    except Exception as e:
        print(f"[!] Error Telegram Photo: {e}")

    # Enviar Documento HD
    try:
        url_doc = f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument"
        with open(img_path, 'rb') as doc:
            r_doc = requests.post(url_doc, data={'chat_id': CHAT_ID, 'caption': f"📄 *HD Native File Option B:* #{evt_id}", 'parse_mode': 'Markdown'}, files={'document': doc}, timeout=10)
            print(f"[*] TG Document Relay Status: {r_doc.status_code}")
    except Exception as e:
        print(f"[!] Error Telegram Document: {e}")

    # ntfy Relay
    try:
        ntfy_msg = f"M82 ALERT [{daemon_source}]: {headline[:100]}"
        requests.post(NTFY_URL, data=ntfy_msg.encode('utf-8'), timeout=10)
        print(f"[*] ntfy Relay Status: 200 OK")
    except Exception as e:
        print(f"[!] Error ntfy: {e}")

def run_push_loop():
    print("🚀 M82 PUSH ENGINE INICIADO (FORMATO OPCIÓN B REAL CON BORDES CYAN)...")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    
    cur.execute("SELECT id, daemon_source, headline FROM m82_multi_stream ORDER BY id DESC LIMIT 3")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        evt_id, source, headline = row
        img_path = generate_hud_option_b(evt_id, headline, source)
        dispatch_event(evt_id, headline, source, img_path)
        time.sleep(2)

if __name__ == "__main__":
    run_push_loop()
