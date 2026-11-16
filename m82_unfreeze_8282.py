#!/usr/bin/env python3
import re
import time
import shutil
import py_compile
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
GW_FILE = BASE_DIR / "orchestrator" / "m82_mobile_gateway.py"
BAK_V5 = BASE_DIR / ".local_backups" / "m82_mobile_gateway.py.bak_v5"
LOGS_DIR = BASE_DIR / "logs"
WD_SCRIPT = BASE_DIR / "m82_port8282_watchdog.sh"

# 1. Matar todos los procesos previos que puedan tener el puerto o sockets guindados
for pat in ("m82_port8282_watchdog.sh", "m82_8282_instant_proxy.py", "run_gateway_8283.py", "m82_mobile_gateway.py"):
    subprocess.run(["pkill", "-9", "-f", pat], stderr=subprocess.DEVNULL)
time.sleep(1)

# 2. Restaurar bak_v5 limpio y anadir cabecera segura (sin proxy intermedio que guinde la app)
if BAK_V5.exists():
    shutil.copy2(BAK_V5, GW_FILE)

raw_src = GW_FILE.read_text(encoding="utf-8", errors="ignore")

SAFE_PRELUDE = """# -*- coding: utf-8 -*-
import sqlite3 as _m82_sq
from http.server import BaseHTTPRequestHandler, HTTPServer
try:
    from http.server import ThreadingHTTPServer
except ImportError:
    from socketserver import ThreadingMixIn
    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True

ThreadingHTTPServer.allow_reuse_address = True
BaseHTTPRequestHandler.address_string = lambda self: self.client_address[0]

_orig_sq_connect = _m82_sq.connect
def _m82_nonblocking_connect(db, *args, **kwargs):
    kwargs.setdefault("timeout", 30.0)
    con = _orig_sq_connect(db, *args, **kwargs)
    try:
        con.execute("PRAGMA busy_timeout = 30000;")
    except Exception:
        pass
    return con
_m82_sq.connect = _m82_nonblocking_connect
"""

if "SAFE_PRELUDE_M82" not in raw_src:
    GW_FILE.write_text("# SAFE_PRELUDE_M82\n" + SAFE_PRELUDE + "\n" + raw_src, encoding="utf-8")

# 3. Validar compilacion sintactica antes de ejecutar
try:
    py_compile.compile(str(GW_FILE), doraise=True)
    print("[+] Sintaxis de orchestrator/m82_mobile_gateway.py verificada OK.")
except Exception as e:
    print(f"[!] Error de sintaxis detectado: {e}")
    raise SystemExit(1)

# 4. Actualizar watchdog limpio apuntando DIRECTO a orchestrator/m82_mobile_gateway.py en 8282
WD_SCRIPT.write_text(f"""#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
export PYTHONUNBUFFERED=1
while true; do
    if ! python3 -c "import socket; s=socket.create_connection(('127.0.0.1',8282),1.5); s.close()" 2>/dev/null; then
        pkill -9 -f "m82_mobile_gateway.py" 2>/dev/null || true
        sleep 1
        nohup python3 -u "{GW_FILE}" >> "{LOGS_DIR}/server_8282.log" 2>&1 &
        sleep 3
    fi
    sleep 5
done
""", encoding="utf-8")
WD_SCRIPT.chmod(0o755)

# 5. Arrancar watchdog y verificar respuesta real en 127.0.0.1:8282
subprocess.Popen(["nohup", "bash", str(WD_SCRIPT)], stdout=open(LOGS_DIR / "watchdog_8282.log", "a"), stderr=subprocess.STDOUT, start_new_session=True)
time.sleep(3)

try:
    t0 = time.perf_counter()
    with urllib.request.urlopen("http://127.0.0.1:8282/", timeout=10) as r:
        body = r.read()
        ms = (time.perf_counter() - t0) * 1000.0
        print(f"[+] PUERTO 127.0.0.1:8282 DESBLOQUEADO Y EN VIVO | HTTP {r.getcode()} | {len(body):,} bytes | {ms:.1f} ms")
except Exception as e:
    print(f"[!] Aviso al conectar: {e}")
    log_txt = (LOGS_DIR / "server_8282.log").read_text(errors="ignore")
    print("--- ULTIMAS 15 LINEAS DE server_8282.log ---")
    print("\n".join(log_txt.splitlines()[-15:]))
