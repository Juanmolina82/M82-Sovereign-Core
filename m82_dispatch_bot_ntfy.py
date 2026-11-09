import os, json, requests, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Carga de Variables de Entorno y Payload
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

wire_text = payload.get("wire", "M82 WIRE: Broadcast activo desde Nodo Charallave Edge.")
bunker_status = payload.get("governance_mode", "BUNKER_MODE_0.30X_LOCK")
timestamp = time.strftime("%Y-%m-%d %H:%M:%S VET")

# Formateo del Mensaje de Difusión Institucional
message = f"""⚡ *M82 AGENTIC TELEMETRY BROADCAST*
────────────────────────────
*Timestamp:* {timestamp}
*Governance:* `{bunker_status}`
*Dry Powder:* `100.0%`

📡 *WIRE:*
{wire_text}

📊 *DATOS CLAVE INGESTADOS:*
• NVDA Shock: -8% Mon (~$350B loss) | Korea Supply OK
• Saudi Gov Portfolio: $1.444T AUM (Aramco 91.64%)
• FedWatch Dec Hike: 79% Prob
• Japan MOF Intervention: Record ¥7.98T single-day

*Caracas HQ Central ⊗ Charallave Edge Node*"""

# 2. Despacho vía Bot Privado de Telegram (si variables están activas)
telegram_token = os.getenv("TELEGRAM_TOKEN", "")
chat_id = os.getenv("CHAT_ID", "")

if telegram_token and chat_id:
    try:
        tg_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        tg_res = requests.post(tg_url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
        if tg_res.status_code == 200:
            print("[BOT TG OK] Alerta enviada con éxito al Bot Privado Telegram.")
        else:
            print(f"[BOT TG WARN] Telegram respondió HTTP {tg_res.status_code}")
    except Exception as e:
        print(f"[BOT TG ERROR] {e}")
else:
    print("[BOT TG SKIP] TELEGRAM_TOKEN o CHAT_ID no configurados en entorno. Despacho alterno activo.")

# 3. Despacho vía Canal Alterno Ntfy (Push Server)
ntfy_topic = os.getenv("NTFY_TOPIC", "m82_sovereign_alerts")
try:
    ntfy_url = f"https://ntfy.sh/{ntfy_topic}"
    ntfy_res = requests.post(
        ntfy_url,
        data=wire_text.encode('utf-8'),
        headers={
            "Title": "⚡ M82 TELEMETRY BROADCAST",
            "Priority": "high",
            "Tags": "warning,chart_with_upwards_trend"
        },
        timeout=5
    )
    if ntfy_res.status_code == 200:
        print(f"[NTFY OK] Notificación Push emitida con éxito al tópico: {ntfy_topic}")
    else:
        print(f"[NTFY WARN] Ntfy respondió HTTP {ntfy_res.status_code}")
except Exception as e:
    print(f"[NTFY ERROR] {e}")

