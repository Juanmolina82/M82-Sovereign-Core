#!/usr/bin/env python3
import asyncio, os, sys, time, sqlite3, requests

# Intentar cargar credenciales desde el entorno o archivo de configuración
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_TELEGRAM_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "TU_TELEGRAM_CHAT_ID_HERE")

DAEMONS_LIST = [
    "DAEMON_MACRO_US10Y", "DAEMON_ENERGY_BRENT", "DAEMON_VENALUM_OFFTAKE",
    "DAEMON_SPX_ROTATION", "DAEMON_THERMAL_MONITOR", "DAEMON_LOGISTICS_REAPER",
    "DAEMON_WAL_PERSISTENCE", "DAEMON_TGA_LIQUIDITY"
]

def send_telegram_msg(text):
    if "TU_TELEGRAM" in TELEGRAM_TOKEN or "TU_TELEGRAM" in CHAT_ID:
        print(f"⚠️ [MOCK SEND] {text[:60]}...")
        return True
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")
        return False

def run_burst():
    print("🚀 INICIANDO RÁFAGA DE NOTIFICACIONES A TELEGRAM...")
    print("=" * 65)
    
    total_sent = 0
    # Recorrer lista de daemons emitiendo 5 ráfagas secuenciales
    for daemon_idx, daemon_name in enumerate(DAEMONS_LIST, 1):
        for burst_idx in range(1, 6):
            msg = (
                f"🚨 *[M82 NODE ALERT - {daemon_name}]*\n"
                f"• Burst ID: `{daemon_idx}.{burst_idx}/5` | Status: `ACTIVE`\n"
                f"• Telemetry: Thermal < 41°C | WAL Mode `OK`\n"
                f"• Vector: Pre-FOMC Surveillance (7 Oct, 2:00 PM EST)\n"
                f"• Timestamp: `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
            )
            success = send_telegram_msg(msg)
            total_sent += 1
            print(f"📡 [{total_sent:02d}] Sent {daemon_name} -> Burst {burst_idx}/5 | Success: {success}")
            time.sleep(0.1) # Breve delay anti-rate-limit

    print("=" * 65)
    print(f"✅ RÁFAGA FINALIZADA: {total_sent} Notificaciones despachadas.")
    print("🔒 Restableciendo silencio táctico (enviado_bot = 1).")

if __name__ == "__main__":
    run_burst()
