#!/usr/bin/env python3
# ==============================================================================
# M82 V60.7.7 PRIME :: RIGID BOUNDING TEXT WRAPPER & SANITIZER (CORE ENGINE)
# ==============================================================================

import os, sqlite3, json, subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

VAULT_PATH = os.path.expanduser("~/M82/vault/protected/vault.json")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
GALLERY_DIR = os.path.expanduser("~/storage/pictures/M82_Cards")
os.makedirs(GALLERY_DIR, exist_ok=True)

def load_vault():
    if os.path.exists(VAULT_PATH):
        with open(VAULT_PATH, "r") as f: return json.load(f)
    alt = os.path.expanduser("~/M82/vault.json")
    if os.path.exists(alt):
        with open(alt, "r") as f: return json.load(f)
    return {}

credentials = load_vault()
BOT_TOKEN = credentials.get("telegram_bot_token")
CHAT_ID = credentials.get("telegram_chat_id")

def get_font(size=26):
    font_paths = [
        "/system/fonts/DroidSansMono.ttf",
        "/system/fonts/RobotoMono-Regular.ttf",
        "/system/fonts/monospace.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def force_rigid_wrap(text, max_chars=30):
    """Corta y empaqueta el texto estrictamente cada 30 caracteres para que JAMÁS toque el borde."""
    lines = []
    text = str(text).replace("\r", "")
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for w in words:
            if len(w) > max_chars:
                for i in range(0, len(w), max_chars):
                    chunk = w[i:i+max_chars]
                    if current: lines.append(current); current = ""
                    lines.append(chunk)
            elif len(current) + len(w) + (1 if current else 0) <= max_chars:
                current = f"{current} {w}".strip()
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
    return lines

def sanitize_text(val):
    if not val: return ""
    val = str(val)
    val = val.replace("REFINITIV_LIVE_BRIDGE", "GLOBAL_WIRE_DESK")
    val = val.replace("REFINITIV_LIVE", "GLOBAL_WIRE")
    val = val.replace("REFINITIV", "GLOBAL_WIRE")
    val = val.replace("Refinitiv Live Sync", "Terminal Wire Sync")
    val = val.replace("Refinitiv Live", "Terminal Wire Sync")
    val = val.replace("Refinitiv", "Global Wire")
    return val

def render_quantum_card(desk, agi_layer, wire_telemetry, thesis, risk_profile, alpha_score="0.95"):
    img = Image.new('RGB', (1000, 1250), color=(5, 10, 20))
    d = ImageDraw.Draw(img)
    
    desk = sanitize_text(desk)
    thesis = sanitize_text(thesis)
    wire_telemetry = sanitize_text(wire_telemetry)
    
    f_header = get_font(28)
    f_sub = get_font(18)
    f_title = get_font(22)
    f_body = get_font(28)
    f_badge = get_font(20)
    
    # Grilla de fondo
    for x in range(0, 1000, 35): d.line([(x, 0), (x, 1250)], fill=(10, 20, 38), width=1)
    for y in range(0, 1250, 35): d.line([(0, y), (1000, y)], fill=(10, 20, 38), width=1)
    
    # Marco exterior
    d.rectangle([15, 15, 985, 1235], outline=(0, 150, 230), width=3)
    d.rectangle([22, 22, 978, 1228], outline=(0, 70, 130), width=1)
    
    # Header Top
    d.rectangle([40, 40, 960, 115], fill=(8, 18, 35), outline=(0, 100, 180), width=1)
    d.text((60, 50), "M82 QUANTUM TERMINAL", fill=(0, 229, 255), font=f_header)
    d.text((60, 85), f"NODE: SOVEREIGN PRIMARY EDGE L5 │ {datetime.now().strftime('%H:%M:%S ET')}", fill=(100, 150, 200), font=f_sub)
    d.ellipse([920, 58, 936, 74], fill=(0, 255, 135))
    
    # Badges Top
    d.rectangle([40, 130, 470, 195], fill=(12, 28, 52), outline=(0, 140, 230), width=2)
    d.text((55, 142), "DESK CATEGORY", fill=(0, 150, 210), font=f_sub)
    d.text((55, 162), f"{desk[:20]}", fill=(0, 229, 255), font=f_badge)
    
    d.rectangle([490, 130, 960, 195], fill=(8, 32, 28), outline=(0, 180, 120), width=2)
    d.text((505, 142), "INTELLIGENCE LAYER", fill=(0, 160, 100), font=f_sub)
    d.text((505, 162), f"{agi_layer}", fill=(0, 255, 135), font=f_badge)
    
    # Telemetry Box
    d.rectangle([40, 215, 960, 790], fill=(8, 16, 30), outline=(0, 80, 150), width=2)
    d.rectangle([40, 215, 960, 265], fill=(20, 35, 60), outline=(0, 100, 180), width=1)
    d.text((60, 228), "🗲 REAL-TIME WIRE TELEMETRY DISPATCH", fill=(255, 75, 75), font=f_title)
    
    d.rectangle([780, 225, 945, 255], fill=(30, 50, 20), outline=(0, 200, 100), width=1)
    d.text((792, 230), f"ALPHA {alpha_score}", fill=(0, 255, 135), font=f_sub)
    
    # RENDERIZADO DE TELEMETRÍA CON ANCHO LÍMITE DE 30 CARACTERES (MARGEN ABSOLUTO)
    wrapped_lines = force_rigid_wrap(wire_telemetry, max_chars=30)
    y_text = 290
    for line in wrapped_lines[:9]:
        d.text((65, y_text), line, fill=(240, 248, 255), font=f_body)
        y_text += 48
        
    # Thesis Box
    d.rectangle([40, 810, 960, 1140], fill=(10, 22, 42), outline=(0, 120, 200), width=2)
    d.text((60, 830), "STRATEGIC THESIS", fill=(0, 150, 220), font=f_sub)
    d.text((60, 855), f"🗲 {thesis[:38]}", fill=(0, 229, 255), font=f_badge)
    d.line([(60, 895), (940, 895)], fill=(0, 60, 120), width=1)
    d.text((60, 910), "PORTFOLIO RISK PROFILE", fill=(200, 140, 40), font=f_sub)
    d.text((60, 935), f"🗲 {risk_profile[:38]}", fill=(255, 180, 50), font=f_badge)
    d.line([(60, 975), (940, 975)], fill=(0, 60, 120), width=1)
    d.text((60, 990), "GOVERNANCE & COMPLIANCE", fill=(120, 150, 180), font=f_sub)
    d.text((60, 1015), "🗲 ZERO-PII GATEWAY D-34 MASKED PASS  │  BUNKER MODE 0.30x LOCK", fill=(160, 200, 230), font=f_sub)
    
    # Footer
    d.line([(40, 1160), (960, 1160)], fill=(0, 100, 180), width=1)
    d.text((40, 1180), "M82 CITADEL PRIME │ INSTITUTIONAL MACRO OBSERVABILITY", fill=(100, 140, 180), font=f_sub)
    d.text((730, 1180), "ACTIVE │ @MolinaHoldings", fill=(0, 229, 255), font=f_sub)
    
    card_path = os.path.join(GALLERY_DIR, f"M82_CARD_{int(datetime.now().timestamp())}.png")
    img.save(card_path)
    
    subprocess.run(["termux-media-scan", card_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return card_path

if __name__ == "__main__":
    # Test individual directo
    render_quantum_card("BANKING", "OLLAMA LOCAL (ZERO-CLOUD)", "Telemetry event verified:\n[BAC.N | 2026-10-15 00:18:21] Pre-Market liquidity depth scanned — Financials basket stable", "BANKING Signal Shift", "Exp 0.22x / 0.30x LOCK | VaR 1.68%", "0.91")
