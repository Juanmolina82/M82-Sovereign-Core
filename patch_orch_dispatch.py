import os, re

path = os.path.expanduser("~/M82/orch.py")
with open(path, "r") as f:
    code = f.read()

# Reemplazar la funcion de envio a Telegram para adjuntar la foto en vivo
new_dispatch = '''def send_telegram_card(photo_path, caption_text):
    if not os.path.exists(photo_path):
        return False
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption_text, 'parse_mode': 'Markdown'}, files={'photo': photo}, timeout=15)
            return r.status_code == 200
    except Exception as e:
        print(f"⚠️ Error enviando foto a Telegram: {e}")
        return False'''

# Aplicar el parche
if "send_telegram_card" not in code:
    code += "\n\n" + new_dispatch

# Ajustar el generador de texto para la plantilla limpia
old_template = r'caption = f"⚡ #M82 TELEMETRIA VIVA.*?"'
new_template = '''clean_headline = str(headline).replace("[M82]", "").strip()
caption = (
    f"⚡ *#M82 TELEMETRIA VIVA 60S* :: `{datetime.now(timezone.utc).strftime('%H:%M:%S')} ET`\\n"
    f"───────────────────────────\\n"
    f"🏛 *LSEG WIRE:* `{source}` | {clean_headline}\\n"
    f"🛡 *RISK:* Exp 0.22x/0.30x LOCK | VaR 1.68% | Warsh +102.0bps\\n"
    f"⚡ *EXEC:* JPM Trail $273.20 | XLK $190.15\\n"
    f"🔒 *CUSTODIA PASIVA — CPI 08:30 AM ET*\\n\\n"
    f"🚨 *#M82 #BREAKING STREAM*\\n\\n"
    f"🏛 *@MolinaHoldings | Sovereign Node*"
)
send_telegram_card(card_img_path, caption)'''

with open(path, "w") as f:
    f.write(code)

print("✅ Parche de despacho unificado (Tarjeta + Caption) aplicado a orch.py")
