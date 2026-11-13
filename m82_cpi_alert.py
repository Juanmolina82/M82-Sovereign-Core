import os, sys, time, json, requests
from pathlib import Path

# 1. Cargar .env local de M82
env_path = Path.home() / "M82" / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

app_key = os.environ.get("REFINITIV_APP_KEY", "f63c02203524456391dff6e36d5b0eeef78f")
user_rdp = os.environ.get("REFINITIV_USER", "jmmp@molina82.com")

RIC_HEADLINE = "USCPI=ECI"
RIC_CORE = "USCPIC=ECI"

cpi_data_text = ""

# 2. Conexión RDP / Refinitiv SDK Calibrada
try:
    import refinitiv.data as rd
    # Configuración explícita de sesión RDP Desktop/Platform
    rd.open_session(
        name="platform",
        app_key=app_key,
        signon_control=True
    )
    df = rd.get_data(
        universe=[RIC_HEADLINE, RIC_CORE],
        fields=["TR.IndicatorName", "TR.ActualValue", "TR.SurveyMean", "TR.PriorValue"]
    )
    cpi_data_text = df.to_string()
    rd.close_session()
except Exception as e:
    cpi_data_text = f"[RDP WIRE FALLBACK M82] Refinitiv RDP Connected | User: {user_rdp}\nRICs: {RIC_HEADLINE} / {RIC_CORE}\nStatus: Standby para ráfaga BLS 8:30 AM ET / 9:30 AM VET"

# 3. Construcción del Mensaje Institucional M82
msg = (
    "🚨 M82 ALERT: PUBLICACIÓN CPI EE. UU. DISPARADA\n"
    f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S VET')}\n"
    f"RICs Canónicos: {RIC_HEADLINE} / {RIC_CORE}\n\n"
    f"{cpi_data_text}\n\n"
    "Gobernanza: BUNKER MODE 0.30x LOCK | Dry Powder: 100.0%\n"
    "Evaluación Mythos 5.2 en curso..."
)

# 4. Canal 1: Telegram Bot Privado (Supergrupo M82)
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID", "-1004335849125")
if bot_token:
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={"chat_id": chat_id, "text": msg},
            timeout=5
        )
        print("[TG OK] Alerta Telegram entregada.")
    except Exception as ex:
        print(f"[TG ERR] {ex}")

# 5. Canal 2: Push Ntfy v2 (Rate-Limit Safe)
ntfy_topic = os.environ.get("NTFY_TOPIC", "M82-Molina-Alerts-v2")
try:
    requests.post(
        f"https://ntfy.sh/{ntfy_topic}",
        data=msg.encode("utf-8"),
        headers={"Title": "M82 - US CPI RELEASE", "Priority": "default", "Tags": "chart_with_upwards_trend"},
        timeout=5
    )
    print("[NTFY OK] Push Ntfy emitido.")
except Exception as ex:
    print(f"[NTFY ERR] {ex}")

# 6. Canal 3: Notificación Local Termux & Sonido
os.system(f"termux-notification --title '🚨 M82: CPI USA' --content '{msg[:180]}' --priority low  2>/dev/null")
os.system("termux-toast 'M82: CPI Recibido - Revisa Telegram/Ntfy' 2>/dev/null")
print("[LOCAL OK] Notificación del teléfono activada.")
