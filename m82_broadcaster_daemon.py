import os, json, requests, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN", "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4")
CHAT_ID = "-1004335849125"
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "M82-Molina-Alerts-v2")

def broadcast_cycle():
    payload = {}
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f: payload = json.load(f)
        except Exception: payload = {}

    wire_text = payload.get("wire", "M82 WIRE: Telemetría RDP Activa")
    bunker_status = payload.get("governance_mode", "BUNKER_MODE_0.30X_LOCK")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S VET")

    msg_tg = f"""⚡ *M82 TELEMETRY BROADCAST LIVE*
────────────────────────────
*Timestamp:* {timestamp}
*Governance:* `{bunker_status}`
*Dry Powder:* `100.0%`

📡 *WIRE LSEG RDP:*
{wire_text}

📊 *MATRIZ REAL-TIME:*
• ICE Brent Crude: $94.32 (-4.07%)
• NYMEX WTI Crude: $87.71 (-3.43%)
• Merey 16 Anchor: $83.15 LIVE
• KKR Infra AUM: 6% Data Centers (7 Platforms)
• Postura: BUNKER 0.30x LOCK (Hermético)

*Caracas HQ Central ⊗ Charallave Edge Node*"""

    # 1. Despacho Telegram Supergrupo
    try:
        url_tg = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        r_tg = requests.post(url_tg, json={"chat_id": CHAT_ID, "text": msg_tg, "parse_mode": "Markdown"}, timeout=5)
        if r_tg.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] [TG OK] Entregado a Telegram Supergrupo ({CHAT_ID})")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] [TG WARN] Status {r_tg.status_code}")
    except Exception as e:
        print(f"[TG ERROR] {e}")

    # Pausa de 2 segundos para evitar HTTP 429
    time.sleep(2)

    # 2. Despacho Ntfy v2 (Rate-Limit Safe)
    try:
        url_ntfy = f"https://ntfy.sh/{NTFY_TOPIC}"
        r_ntfy = requests.post(
            url_ntfy,
            data=wire_text.encode('utf-8'),
            headers={
                "Title": "M82 TELEMETRY PULL LIVE",
                "Priority": "high",
                "Tags": "rocket,chart_with_upwards_trend"
            },
            timeout=5
        )
        if r_ntfy.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] [NTFY OK] Push emitido a https://ntfy.sh/{NTFY_TOPIC}")
        elif r_ntfy.status_code == 429:
            print(f"[{time.strftime('%H:%M:%S')}] [NTFY WARN] Rate limit alcanzado (429). Reintentando en próximo ciclo.")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] [NTFY WARN] Status {r_ntfy.status_code}")
    except Exception as e:
        print(f"[NTFY ERROR] {e}")

if __name__ == "__main__":
    broadcast_cycle()
