#!/usr/bin/env python3
import os, re, requests

NEW_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

files = ["orch.py", "m82_refinitiv_realtime_bridge.py", "m82_master_dossier.py"]

for fname in files:
    path = os.path.expanduser(f"~/M82/{fname}")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        # Reemplaza cualquier asignación de TOKEN manteniendo la estructura
        text = re.sub(r'TOKEN\s*=\s*["\'].*?["\']', f'TOKEN = "{NEW_TOKEN}"', text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Token actualizado en {fname}")

# Probar despacho directo a Telegram
url = f"https://api.telegram.org/bot{NEW_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": "⚡ *#M82 FREIGHT STRESS EXECUTION CONFIRMED*\n───────────────────────────\n🏛 *SCENARIO:* Bab-el-Mandeb Block\n🛡 *RISK:* VaR 1.68% | Lock: 0.30x\n🔒 *STATUS:* WAL 0/0/0 OK | Dispatch Resumed",
    "parse_mode": "Markdown"
}

try:
    r = requests.post(url, data=payload, timeout=10)
    print(f"[*] Telegram API Response: {r.status_code} | {r.text[:80]}")
    if r.status_code == 200:
        print("🚀 TELEGRAM RELAY RESTABLECIDO EXITOSAMENTE (200 OK)")
except Exception as e:
    print(f"[!] Error de red: {e}")
