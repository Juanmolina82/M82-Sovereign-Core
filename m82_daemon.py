#!/usr/bin/env python3
import time
import subprocess
import urllib.request
import sqlite3
import os
import sys

# --- CONFIGURACIÓN DEL NODO CHARALLAVE ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = "-1004335849125"
DB_PATH = "m82_database.db"
CHECK_INTERVAL = 15  # segundos entre chequeos de salud

SERVICES = {
    "REST_API": {
        "port": 8083,
        "url": "http://127.0.0.1:8083/signals",
        "cmd": [sys.executable, "-m", "http.server", "8083"],  # Reemplazar por comando de API si difiere
    },
    "PWA_HUD": {
        "port": 8080,
        "url": "http://127.0.0.1:8080",
        "cmd": [sys.executable, "-m", "http.server", "8080"],
    }
}

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN:
        print(f"[DAEMON] ⚠️ Telegram Token no detectado. Mensaje retenido: {message}")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": message}).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[DAEMON] Error enviando alerta Telegram: {e}")

def check_service(name, cfg):
    try:
        req = urllib.request.Request(cfg["url"], headers={'User-Agent': 'M82-Daemon/1.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                return True
    except Exception:
        pass
    return False

def restart_service(name, cfg):
    print(f"[DAEMON] 🔴 Servicio {name} caído en puerto {cfg['port']}. Reiniciando...")
    send_telegram_alert(f"⚠️ [M82 DAEMON] Servicio {name} (:{cfg['port']}) no responde. Intentando reinicio...")
    
    # Matar cualquier proceso colgado en el puerto objetivo
    try:
        subprocess.run(f"fuser -k {cfg['port']}/tcp", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    except Exception:
        pass

    # Iniciar servicio en segundo plano
    subprocess.Popen(cfg["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    if check_service(name, cfg):
        print(f"[DAEMON] 🟢 Servicio {name} restablecido correctamente.")
        send_telegram_alert(f"✅ [M82 DAEMON] Servicio {name} (:{cfg['port']}) recuperado y operativo.")
    else:
        print(f"[DAEMON] ❌ Fallo al reiniciar {name}.")

def checkpoint_sqlite_wal():
    """ Mantenimiento preventivo WAL para liberar espacio y consolidar transacciones """
    try:
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
            conn.close()
            print("[DAEMON] ⚙️ PRAGMA wal_checkpoint(PASSIVE) ejecutado con éxito.")
    except Exception as e:
        print(f"[DAEMON] Error en mantenimiento WAL: {e}")

def main():
    print("==================================================")
    print(" 🛡️  M82 DAEMON DE SUPERVISIÓN - NODO CHARALLAVE ")
    print("==================================================")
    print(f"[DAEMON] Intervalo de monitoreo: {CHECK_INTERVAL}s")
    print(f"[DAEMON] Base de datos supervisada: {DB_PATH}")
    
    cycle_count = 0
    while True:
        try:
            # 1. Supervisión de Servicios HTTP (:8083 / :8080)
            for name, cfg in SERVICES.items():
                if not check_service(name, cfg):
                    restart_service(name, cfg)

            # 2. Mantenimiento WAL preventivo cada 40 ciclos (~10 min)
            cycle_count += 1
            if cycle_count >= 40:
                checkpoint_sqlite_wal()
                cycle_count = 0

        except KeyboardInterrupt:
            print("\n[DAEMON] Detenido por el usuario.")
            break
        except Exception as e:
            print(f"[DAEMON] Error inesperado en loop principal: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
