#!/usr/bin/env python3
import os
import sqlite3
import subprocess
import time
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
OUT_DIR = "/storage/emulated/0/M82card"
STATE_FILE = os.path.expanduser("~/M82/.last_hud_id")

os.makedirs(OUT_DIR, exist_ok=True)

def notify_gallery_nonblocking(filepath: str):
    # Disparo nativo Android MediaScanner sin bloquear el bucle de renderizado
    try:
        subprocess.Popen(
            [
                "am", "broadcast",
                "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d", f"file://{filepath}",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass

def wrap_text(text: str, width: int = 46):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = f"{cur} {w}".strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:14]

def render_card(row_id: int, source: str, headline: str, alpha: float, impact: str):
    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUT_DIR, f"M82_HUD_{row_id}_{ts_str}.png")

    img = Image.new("RGB", (1000, 1250), color=(8, 12, 22))
    draw = ImageDraw.Draw(img)

    draw.rectangle([28, 28, 972, 1222], outline=(0, 229, 255), width=3)
    draw.rectangle([42, 42, 958, 145], fill=(14, 24, 42), outline=(0, 180, 216), width=2)

    try:
        f_title = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 34)
        f_sub = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 24)
        f_body = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 26)
        f_foot = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 22)
    except Exception:
        f_title = f_sub = f_body = f_foot = ImageFont.load_default()

    draw.text((64, 62), "M82 SOVEREIGN CORE V60 :: HUD TELEMETRY", fill=(0, 245, 212), font=f_title)
    draw.text((64, 108), f"ID #{row_id} | SRC: {source} | ALPHA: {alpha:.2f}", fill=(148, 210, 189), font=f_sub)

    draw.rectangle([42, 168, 958, 225], fill=(45, 14, 22), outline=(255, 77, 109), width=2)
    draw.text((64, 184), "GOVERNANCE: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK", fill=(255, 117, 143), font=f_sub)

    draw.text((64, 255), f"VECTOR IMPACT: {impact}", fill=(255, 209, 102), font=f_sub)
    draw.line([64, 295, 936, 295], fill=(38, 70, 83), width=2)

    y = 325
    for line in wrap_text(headline, width=46):
        draw.text((64, y), line, fill=(237, 242, 244), font=f_body)
        y += 42

    draw.rectangle([42, 1060, 958, 1195], fill=(14, 24, 42), outline=(0, 180, 216), width=2)
    draw.text((64, 1080), "EXP: 0.22x | VaR: 1.68% | WARSH: +102.0 bps | LOCKOUT: NO TRADE", fill=(0, 229, 255), font=f_foot)
    draw.text((64, 1122), "LOCUS: CHARALLAVE L4/L5 EDGE ⊗ CARACAS HQ CENTRAL", fill=(173, 181, 189), font=f_foot)
    draw.text((64, 1158), "[ AGI QUANTUM VERIFIED ] :: @MolinaHoldings LLC", fill=(128, 255, 219), font=f_foot)

    img.save(filename, "PNG")
    notify_gallery_nonblocking(filename)
    return filename

def get_last_id():
    if os.path.exists(STATE_FILE):
        try:
            return int(open(STATE_FILE).read().strip())
        except Exception:
            pass
    return 0

def set_last_id(val: int):
    with open(STATE_FILE, "w") as f:
        f.write(str(val))

def process_queue(initial_backfill: bool = False):
    conn = sqlite3.connect(DB_PATH, timeout=120.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")

    last_id = get_last_id()
    if initial_backfill and last_id == 0:
        rows = conn.execute(
            "SELECT id, daemon_source, headline, alpha_score, asset_impact FROM m82_multi_stream ORDER BY id DESC LIMIT 12;"
        ).fetchall()
        rows.reverse()
    else:
        rows = conn.execute(
            "SELECT id, daemon_source, headline, alpha_score, asset_impact FROM m82_multi_stream WHERE id > ? ORDER BY id ASC LIMIT 25;",
            (last_id,),
        ).fetchall()
    conn.close()

    for r in rows:
        rid, src, hl, alpha, impact = r
        out = render_card(rid, src or "M82_CORE", hl or "", float(alpha or 0.90), impact or "MACRO")
        set_last_id(rid)
        print(f"🖼️ HUD READY -> {os.path.basename(out)}")

if __name__ == "__main__":
    process_queue(initial_backfill=True)
    while True:
        time.sleep(15)
        process_queue(initial_backfill=False)
