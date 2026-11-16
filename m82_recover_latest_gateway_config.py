#!/usr/bin/env python3
import os
import re
import time
import shutil
import py_compile
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
GW_FILE = BASE_DIR / "orchestrator" / "m82_mobile_gateway.py"
LOGS_DIR = BASE_DIR / "logs"

print("=== [1/3] ESCANEANDO TODAS LAS VERSIONES Y RESPALDOS DEL GATEWAY 8282 ===")
candidates = []
for p in BASE_DIR.rglob("*mobile_gateway*"):
    if p.is_file() and p != GW_FILE:
        st = p.stat()
        candidates.append((st.st_mtime, st.st_size, p))

# Ordenar de mas reciente a mas antiguo
candidates.sort(key=lambda x: x[0], reverse=True)

for idx, (mtime, size, p) in enumerate(candidates[:10], 1):
    dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"  [{idx}] {dt} | {size:>7,} bytes | {p.relative_to(BASE_DIR)}")

# Buscar tambien scripts en ~/M82 que hayan modificado o inyectado configuracion en m82_mobile_gateway.py
patch_scripts = []
for py in BASE_DIR.rglob("*.py"):
    if "backups" in py.parts or py.name.startswith(("m82_fix_and_guard", "m82_turbo_8282", "m82_restore_and_accelerate", "m82_unfreeze_8282", "m82_recover_latest")):
        continue
    try:
        txt = py.read_text(encoding="utf-8", errors="ignore")
        if "m82_mobile_gateway.py" in txt:
            patch_scripts.append((py.stat().st_mtime, py))
    except Exception:
        pass

patch_scripts.sort(key=lambda x: x[0], reverse=True)
if patch_scripts:
    print("\n[+] Scripts de configuracion / Hot-Mods detectados que actualizan el gateway:")
    for mtime, py in patch_scripts[:5]:
        dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"    -> {dt} | {py.relative_to(BASE_DIR)}")

if not candidates:
    print("[!] No se hallaron archivos de respaldo adicionales.")
    raise SystemExit(1)

# Seleccionar el respaldo mas reciente (excluyendo bak_v5 si hay uno posterior)
latest_mtime, latest_size, latest_path = candidates[0]
print(f"\n=== [2/3] RESTAURANDO VERSION MAS RECIENTE: {latest_path.relative_to(BASE_DIR)} ({latest_size:,} bytes) ===")

src = latest_path.read_text(encoding="utf-8", errors="ignore")

# Limpiar cualquier rastro previo de inyecciones viejas si existiera
src = re.sub(r'# SAFE_PRELUDE_M82.*?_m82_sq\.connect = _m82_nonblocking_connect\n?', '', src, flags=re.DOTALL)
src = re.sub(r'# === M82 TURBO LOW-LATENCY LAYER.*?# === END M82 TURBO LAYER ===\n?', '', src, flags=re.DOTALL)

SAFE_PRELUDE = """# SAFE_PRELUDE_M82
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

GW_FILE.write_text(SAFE_PRELUDE + "\n" + src, encoding="utf-8")
py_compile.compile(str(GW_FILE), doraise=True)
print("[+] Compilacion sintactica OK sobre la ultima configuracion restaurada.")

print("\n=== [3/3] REINICIANDO GATEWAY 8282 CON LA ULTIMA CONFIGURACION ===")
subprocess.run(["pkill", "-9", "-f", "m82_mobile_gateway.py"], stderr=subprocess.DEVNULL)
time.sleep(2)

with urllib.request.urlopen("http://127.0.0.1:8282/", timeout=10) as r:
    data = r.read()
    print(f"[+] 127.0.0.1:8282 ACTIVO CON ULTIMA CONFIGURACION | HTTP {r.getcode()} | Payload={len(data):,} bytes")
