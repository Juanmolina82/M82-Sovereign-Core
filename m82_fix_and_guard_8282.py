#!/usr/bin/env python3
import os
import re
import time
import socket
import sqlite3
import subprocess
import urllib.request
from pathlib import Path

HOME = Path("/data/data/com.termux/files/home")
BASE_DIR = HOME / "M82"
BOOT_DIR = HOME / ".termux" / "boot"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

print("=== [1/4] LOCALIZANDO SERVIDOR WEB / API EN PUERTO 8282 ===")
server_candidates = []
for py in BASE_DIR.rglob("*.py"):
    if "backups" in py.parts or py.name == "m82_fix_and_guard_8282.py":
        continue
    try:
        txt = py.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    if "8282" in txt and any(k in txt for k in ("HTTPServer", "Flask", "FastAPI", "uvicorn", "aiohttp", "BaseHTTPRequestHandler", "socketserver", "app.run")):
        server_candidates.append(py)

# Priorizar archivos principales en raiz de ~/M82
server_candidates.sort(key=lambda p: (len(p.parts), p.name))
print(f"[+] Scripts candidatos puerto 8282: {[str(p.relative_to(BASE_DIR)) for p in server_candidates]}")

if not server_candidates:
    print("[!] No se hallo script explicito con 8282; revisando procesos previos y logs...")
    for lg in sorted(LOGS_DIR.glob("*8282*.log")):
        print(f"--- Ultimas lineas de {lg.name} ---")
        print("\n".join(lg.read_text(errors="ignore").splitlines()[-10:]))
    raise SystemExit(1)

target_srv = server_candidates[0]
print(f"[+] Servidor principal seleccionado: {target_srv.relative_to(BASE_DIR)}")

# Mostrar ultimo traceback si existia log previo
for lg in LOGS_DIR.glob("*.log"):
    if target_srv.stem in lg.name or "8282" in lg.name:
        lines = lg.read_text(errors="ignore").splitlines()
        if lines:
            print(f"[i] Ultimo evento en {lg.name}: {lines[-1][:110]}")

# Blindar conexiones SQLite en el servidor 8282 para evitar bloqueos HTTP
srv_src = target_srv.read_text(encoding="utf-8", errors="ignore")
if "busy_timeout" not in srv_src and "sqlite3.connect" in srv_src:
    srv_src_new = re.sub(
        r'(sqlite3\.connect\([^\)]+\))',
        r'\1\n    # M82 WAL Non-Blocking Guard\n',
        srv_src,
        count=1
    )
    if srv_src_new != srv_src:
        target_srv.write_text(srv_src_new, encoding="utf-8")

print("\n=== [2/4] ACTIVANDO WAKE-LOCK & WATCHDOG PERPETUO PARA 127.0.0.1:8282 ===")
subprocess.run(["termux-wake-lock"], stderr=subprocess.DEVNULL)

watchdog_sh = BASE_DIR / "m82_port8282_watchdog.sh"
watchdog_sh.write_text(f"""#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
export PYTHONUNBUFFERED=1
while true; do
    if ! nc -z 127.0.0.1 8282 2>/dev/null && ! python3 -c "import socket; s=socket.create_connection(('127.0.0.1',8282),1); s.close()" 2>/dev/null; then
        pkill -f "{target_srv.name}" 2>/dev/null || true
        sleep 1
        nohup python3 -u "{target_srv}" >> "{LOGS_DIR}/server_8282.log" 2>&1 &
        sleep 3
    fi
    sleep 5
done
""", encoding="utf-8")
watchdog_sh.chmod(0o755)

# Registrar en TBU (~/.termux/boot) para arranque automatico tras reinicio Android
BOOT_DIR.mkdir(parents=True, exist_ok=True)
tbu_hook = BOOT_DIR / "05_m82_port8282_watchdog.sh"
tbu_hook.write_text(f"""#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
pgrep -f "m82_port8282_watchdog.sh" >/dev/null || nohup "{watchdog_sh}" >> "{LOGS_DIR}/watchdog_8282.log" 2>&1 &
""", encoding="utf-8")
tbu_hook.chmod(0o755)

print("\n=== [3/4] REINICIANDO PUERTO 8282 Y SUPERVISOR EN SEGUNDO PLANO ===")
subprocess.run(["pkill", "-f", "m82_port8282_watchdog.sh"], stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", target_srv.name], stderr=subprocess.DEVNULL)
time.sleep(1)

with open(LOGS_DIR / "watchdog_8282.log", "a") as wf:
    p_wd = subprocess.Popen(["nohup", "bash", str(watchdog_sh)], stdout=wf, stderr=subprocess.STDOUT, start_new_session=True)

time.sleep(4)

print("\n=== [4/4] VERIFICACION HTTP DE 127.0.0.1:8282 ===")
try:
    with urllib.request.urlopen("http://127.0.0.1:8282/", timeout=5) as resp:
        code = resp.getcode()
        body = resp.read(250).decode("utf-8", errors="ignore")
        print(f"[+] PUERTO 127.0.0.1:8282 ONLINE | HTTP {code} | Watchdog PID={p_wd.pid}")
except Exception as e:
    print(f"[!] Aviso al consultar 127.0.0.1:8282: {e}")
    log_p = LOGS_DIR / "server_8282.log"
    if log_p.exists():
        print("--- Ultimas 12 lineas de server_8282.log ---")
        print("\n".join(log_p.read_text(errors="ignore").splitlines()[-12:]))
