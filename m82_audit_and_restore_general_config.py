#!/usr/bin/env python3
import os
import re
import json
import time
import shutil
import sqlite3
import py_compile
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
GW_FILE = BASE_DIR / "orchestrator" / "m82_mobile_gateway.py"
DB_PATH = BASE_DIR / "m82_database.db"

print("=== [1/4] AUDITORIA DE ARCHIVOS DE CONFIGURACION (JSON / ENV / YAML) ===")
cfg_files = []
for ext in ("*.json", "*.env", "*.yaml", "*.yml", "*.toml", "*.ini"):
    for f in BASE_DIR.rglob(ext):
        if any(skip in f.parts for skip in ("__pycache__", ".git", "node_modules")):
            continue
        st = f.stat()
        cfg_files.append((st.st_mtime, st.st_size, f))

cfg_files.sort(key=lambda x: x[0], reverse=True)
for mtime, size, f in cfg_files[:12]:
    dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"  [CFG] {dt} | {size:>7,} bytes | {f.relative_to(BASE_DIR)}")

print("\n=== [2/4] AUDITORIA DE VERSIONES DE GATEWAY Y SCRIPTS DE CONFIGURACION ===")
gw_versions = []
for f in BASE_DIR.rglob("*gateway*"):
    if f.is_file() and f != GW_FILE:
        st = f.stat()
        gw_versions.append((st.st_mtime, st.st_size, f))
gw_versions.sort(key=lambda x: x[0], reverse=True)

for idx, (mtime, size, f) in enumerate(gw_versions[:10], 1):
    dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"  [GW-{idx}] {dt} | {size:>7,} bytes | {f.relative_to(BASE_DIR)}")

# Detectar scripts recientes que construyen o configuran el dashboard/gateway/sistema
recent_scripts = []
for py in BASE_DIR.rglob("*.py"):
    if any(skip in py.parts for skip in ("__pycache__", ".local_backups", "backups")):
        continue
    if py.name.startswith(("m82_fix_and_guard", "m82_turbo_8282", "m82_restore_and_accelerate", "m82_unfreeze_8282", "m82_recover_latest", "m82_audit_and_restore")):
        continue
    st = py.stat()
    recent_scripts.append((st.st_mtime, st.st_size, py))

recent_scripts.sort(key=lambda x: x[0], reverse=True)
print("\n=== [3/4] ULTIMOS 12 SCRIPTS MODIFICADOS EN ~/M82 (HOT-MODS / CONFIG BUILDERS) ===")
for mtime, size, py in recent_scripts[:12]:
    dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"  [PY]  {dt} | {size:>7,} bytes | {py.relative_to(BASE_DIR)}")

print("\n=== [4/4] VERIFICANDO TABLAS DE CONFIGURACION EN m82_database.db ===")
if DB_PATH.exists():
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=15.0)
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()]
    cfg_tables = [t for t in tables if any(k in t.lower() for k in ("config", "setting", "gov", "state", "desk", "param", "mode", "portal", "ui"))]
    print(f"  [+] Tablas de configuracion/estado en DB: {cfg_tables}")
    for t in cfg_tables[:8]:
        cnt = con.execute(f"SELECT COUNT(*) FROM '{t}';").fetchone()[0]
        print(f"      -> {t}: {cnt} registros")
    con.close()

# Si existe una version de gateway mas reciente que bak_v5 (o mayor tamano con features completas), restaurarla
best_gw = None
for mtime, size, f in gw_versions:
    if f.suffix in (".py",) or "bak" in f.name:
        if f.name != "m82_mobile_gateway.py.bak_v5":
            best_gw = f
            break

if best_gw:
    print(f"\n[+] Encontrada version mas reciente que bak_v5: {best_gw.relative_to(BASE_DIR)} ({best_gw.stat().st_size:,} bytes)")
    src = best_gw.read_text(encoding="utf-8", errors="ignore")
    src = re.sub(r'# SAFE_PRELUDE_M82.*?_m82_sq\.connect = _m82_nonblocking_connect\n?', '', src, flags=re.DOTALL)
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
    subprocess.run(["pkill", "-9", "-f", "m82_mobile_gateway.py"], stderr=subprocess.DEVNULL)
    time.sleep(2)
    print(f"[+] Gateway actualizado y reiniciado con {best_gw.name}.")
else:
    print("\n[i] Revise la lista [PY] de los ultimos 12 scripts arriba para re-aplicar el script exacto de configuracion general.")
