#!/usr/bin/env python3
import os, sys, re, requests

M82_DIR = os.path.expanduser("~/M82")
ORCH_PATH = os.path.join(M82_DIR, "orch.py")
IMG_PATH = os.path.join(M82_DIR, "m82_timeline_latest.png")

if not os.path.exists(IMG_PATH):
    print("⚠️ No se encontró m82_timeline_latest.png")
    sys.exit(1)

# 1. Extraer TOKEN funcional de orch.py
token = None
if os.path.exists(ORCH_PATH):
    with open(ORCH_PATH, "r") as f:
        content = f.read()
        match = re.search(r'TOKEN\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            token = match.group(1)

if not token:
    print("⚠️ No se pudo extraer el TOKEN activo de orch.py")
    sys.exit(1)

CHAT_ID = "-1004335849125"
url = f"https://api.telegram.org/bot{token}/sendPhoto"
caption = "⚡ *M82 REFINITIV WORKSPACE // PRIVATE WIRE TIMELINE*\n🏛 @MolinaHoldings | Sovereign Node"

# 2. Despachar a Telegram
try:
    with open(IMG_PATH, 'rb') as photo:
        r = requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'photo': photo}, timeout=15)
        if r.status_code == 200:
            print(f"✅ TELEGRAM RELAY TIMELINE :: 200 OK Photo + Caption -> @MolinaHoldings (Token: {token[:12]}...)")
        else:
            print(f"⚠️ Error Telegram Relay: {r.status_code} | {r.text}")
except Exception as e:
    print(f"⚠️ Excepción al despachar: {e}")
