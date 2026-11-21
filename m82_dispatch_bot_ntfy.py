import os, json, requests, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f: payload = json.load(f)
    except Exception: payload = {}

wire_text = payload.get("wire", "M82 WIRE: Telemetría unificada activa.")
bunker_status = payload.get("governance_mode", "BUNKER_MODE_0.30X_LOCK")
timestamp = time.strftime("%Y-%m-%d %H:%M:%S VET")

message = f"""⚡ *M82 AGENTIC TELEMETRY BROADCAST*
────────────────────────────
*Timestamp:* {timestamp}
*Governance:* `{bunker_status}`
*Dry Powder:* `100.0%`

📡 *WIRE:*
{wire_text}

📊 *MATRIZ DE RIESGO ACTIVA:*
• KKR Infra AUM: 7 Data Center Platforms = 6% AUM (Nuttall)
• Wall Street Rebound: Dow +1.27% | Nasdaq +1.87%
• LSEG Energy: Brent $94.32 (-4.07%) | WTI $87.71 (-3.43%)
• Próximo Catalizador: CPI Martes (+2.7% YoY)
• Postura: BUNKER 0.30x LOCK (Sin cambios)

*Caracas HQ Central ⊗ Charallave Edge Node*"""

# 1. Despacho Telegram (Target ID verificado: -1004335849125)
tg_token = os.getenv("TELEGRAM_TOKEN", "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4")
target_id = "-1004335849125"

try:
    url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
    res = requests.post(url, json={"chat_id": target_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
    if res.status_code == 200:
        print(f"[BOT TG OK] Notificación entregada con éxito a Chat ID: {target_id}")
    else:
        print(f"[BOT TG WARN] Falló envío a ID {target_id}: HTTP {res.status_code}")
except Exception as e:
    print(f"[BOT TG ERROR] {e}")

# 2. Despacho Ntfy v2 (Fix de Codificación UTF-8 en Headers y Body)
ntfy_topic = os.getenv("NTFY_TOPIC", "M82-Molina-Alerts-v2")
try:
    ntfy_url = f"https://ntfy.sh/{ntfy_topic}"
    clean_title = "M82 TELEMETRY BROADCAST v2" # Título en ASCII seguro
    res = requests.post(
        ntfy_url,
        data=wire_text.encode('utf-8'),
        headers={
            "Title": clean_title,
            "Priority": "high",
            "Tags": "rocket,chart_with_upwards_trend"
        },
        timeout=5
    )
    if res.status_code == 200:
        print(f"[NTFY OK] Push emitido exitosamente a https://ntfy.sh/{ntfy_topic}")
    else:
        print(f"[NTFY WARN] Ntfy respondió: HTTP {res.status_code}")
except Exception as e:
    print(f"[NTFY ERROR] {e}")
