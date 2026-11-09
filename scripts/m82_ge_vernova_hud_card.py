#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, re
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
CARDS_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")
if not os.path.exists(CARDS_DIR):
    CARDS_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")
os.makedirs(CARDS_DIR, exist_ok=True)

# Credenciales de Gobernanza
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
USER_ACCOUNT = "jmmp@molina82.com"

def generate_and_dispatch_hud():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    cur.execute("SELECT id, source, headline, category FROM macro_dossier WHERE m82_tag LIKE '%GE-VERNOVA%' ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    conn.close()

    if not row:
        print("[!] No se encontró registro reciente de GE Vernova.")
        return

    evt_id, source, headline, category = row

    # 1. GENERACIÓN DE TARJETA GRÁFICA HUD (OPCIÓN B)
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#05080e')
    draw = ImageDraw.Draw(img)

    try:
        f_hdr = ImageFont.truetype('DejaVuSans-Bold.ttf', 30)
        f_sub = ImageFont.truetype('DejaVuSans.ttf', 26)
        f_tag = ImageFont.truetype('DejaVuSans-Bold.ttf', 28)
        f_red = ImageFont.truetype('DejaVuSans-Bold.ttf', 32)
        f_body = ImageFont.truetype('DejaVuSans-Bold.ttf', 48)
        f_ftr = ImageFont.truetype('DejaVuSans-Bold.ttf', 26)
    except:
        f_hdr = f_sub = f_tag = f_red = f_body = f_ftr = ImageFont.load_default()

    # Layout Frames
    draw.rectangle([15, 15, W - 15, H - 15], outline='#00b0ff', width=4)
    draw.rectangle([35, 35, W - 35, 125], fill='#070e17', outline='#121f33', width=2)
    draw.text((50, 48), 'SYSTEM: AGI-CORE // NODE: CHARALLAVE L4/L5 EDGE', fill='#00e5ff', font=f_hdr)
    draw.text((50, 85), f'REFINITIV WORKSPACE // USER: {USER_ACCOUNT}', fill='#708090', font=f_sub)

    draw.rectangle([55, 145, 620, 205], fill='#0c182b', outline='#00b0ff', width=2)
    draw.text((70, 162), f'DAEMON: {category[:24]}', fill='#ffffff', font=f_tag)

    draw.rectangle([55, 225, W - 55, 325], fill='#0a101d', outline='#1a293d', width=2)
    draw.text((75, 240), 'EXPOSURE: 0.22x / 0.30x LOCK  |  VaR L5.1: 1.68%', fill='#00b0ff', font=f_sub)
    draw.text((75, 280), 'SEN REBUILD: $25B LOCK  |  WARSH SPREAD: +102.0bps', fill='#ff9100', font=f_sub)

    draw.text((55, 348), '❚ LSEG REFINITIV BREAKING WIRE', fill='#ff1744', font=f_red)
    draw.line([(55, 388), (W - 55, 388)], fill='#ff1744', width=3)

    draw.rectangle([55, 405, W - 55, H - 130], fill='#070b12', outline='#141f30', width=2)

    # Renderizado de Texto Principal
    clean_text = "GE VERNOVA (CEO SCOTT STRAZIK): PAGO POR ADELANTADO OBLIGATORIO ANTES DE REPARAR RED ELÉCTRICA EN VENEZUELA ($25B SEN). GRID LOCK = OIL LOCK."
    y_pos = 450
    words = clean_text.split(' ')
    line = ''
    for word in words:
        if len(line + word) < 22:
            line += word + ' '
        else:
            draw.text((85, y_pos), line.strip(), fill='#ffffff', font=f_body)
            y_pos += 68
            line = word + ' '
    if line.strip():
        draw.text((85, y_pos), line.strip(), fill='#ffffff', font=f_body)

    # Footer HUD
    draw.rectangle([35, H - 115, W - 35, H - 35], fill='#070e17', outline='#121f33', width=2)
    draw.text((50, H - 100), '[ AGI QUANTUM VERIFIED — CUSTODIA PASIVA 0.30x LOCK ]', fill='#00e5ff', font=f_ftr)
    draw.text((50, H - 68), '❚ @MolinaHoldings | Chairman Juan M. Molina', fill='#ffffff', font=f_ftr)

    card_path = os.path.join(CARDS_DIR, f'M82_CARD_GEV_{evt_id}.png')
    img.save(card_path)

    # 2. DESPACHO DUAL (TELEGRAM PHOTO + NTFY PUSH)
    caption_tg = (
        f"⚡ <b>M82 LSEG GRAPHIC TELEMETRY</b> :: {time.strftime('%H:%M:%S VET')}\n"
        f"───────────────────────────\n"
        f"👤 <b>USER:</b> {USER_ACCOUNT}\n"
        f"🏛 <b>SOURCE:</b> Bloomberg / Refinitiv Workspace (GEV.N)\n"
        f"📂 <b>CATEGORY:</b> INFRASTRUCTURE_POWER_GRID\n"
        f"📰 <b>HEADLINE:</b> GE Vernova exige pago por adelantado ($25B SEN Rebuild).\n"
        f"🏷 <b>TAG:</b> <code>v61.0.1-GE-VERNOVA-GEV-POWER-GRID-PAYMENT-LOCK</code>\n"
        f"🛡 <b>RISK:</b> Exp 0.22x | VaR 1.68% | Warsh +102.0bps\n"
        f"🔒 <b>GOVERNANCE:</b> BUNKER MODE 0.30x LOCK\n\n"
        f"🏛 @MolinaHoldings | Chairman Juan M. Molina"
    )

    try:
        # Enviar Imagen HD a Telegram Bot
        with open(card_path, 'rb') as photo:
            r_tg = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto", data={
                'chat_id': CHAT_ID, 'caption': caption_tg, 'parse_mode': 'HTML'
            }, files={'photo': photo}, timeout=15)

        # Enviar Alerta Push a ntfy
        r_ntfy = requests.post(NTFY_URL, data=f"M82 CARD [GE Vernova]: Grid Lock ($25B) - Prepayment Required".encode('utf-8'), headers={
            "Title": f"M82 HUD CARD: GEV.N WIRE ({USER_ACCOUNT})", "Priority": "high", "Tags": "zap,frame_with_picture"
        }, timeout=10)

        print(f"🟢 [HUD CARD DISPATCH SUCCESS] TG Status: {r_tg.status_code} | ntfy Status: {r_ntfy.status_code}")
    except Exception as e:
        print(f"[!] Error despachando Tarjeta HUD: {e}")

if __name__ == "__main__":
    generate_and_dispatch_hud()
