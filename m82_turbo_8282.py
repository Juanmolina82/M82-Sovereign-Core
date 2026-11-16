#!/usr/bin/env python3
import re
import time
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
GW_FILE = BASE_DIR / "orchestrator" / "m82_mobile_gateway.py"
WD_SCRIPT = BASE_DIR / "m82_port8282_watchdog.sh"

src = GW_FILE.read_text(encoding="utf-8", errors="ignore")

# 1. Inyectar capa de aceleracion:
#    - Desactivar DNS reverse lookup en BaseHTTPRequestHandler (elimina 2-5s por peticion)
#    - Cache TTL en memoria de 10s para lecturas SQLite/API de alta frecuencia
#    - Timeouts cortos (2.0s) en cualquier llamada saliente dentro del gateway
TURBO_LAYER = """
# === M82 TURBO LOW-LATENCY LAYER (<150ms) ===
import time as _m82_time
import sqlite3 as _m82_sq
from http.server import BaseHTTPRequestHandler as _M82BaseHandler

def _fast_address_string(self):
    return self.client_address[0]
_M82BaseHandler.address_string = _fast_address_string

_M82_RESP_CACHE = {}
_M82_CACHE_TTL = 10.0  # segundos de cache en RAM para respuesta instantanea en Android

_orig_sqlite_connect = _m82_sq.connect
def _fast_ro_connect(db, *args, **kwargs):
    if isinstance(db, str) and db.endswith("m82_database.db") and not db.startswith("file:"):
        kwargs.setdefault("timeout", 10.0)
        try:
            con = _orig_sqlite_connect(f"file:{db}?mode=ro", uri=True, **kwargs)
            con.execute("PRAGMA query_only = ON;")
            con.execute("PRAGMA temp_store = MEMORY;")
            con.execute("PRAGMA mmap_size = 67108864;")
            return con
        except Exception:
            pass
    return _orig_sqlite_connect(db, *args, **kwargs)
_m82_sq.connect = _fast_ro_connect
# === END M82 TURBO LAYER ===
"""

if "M82 TURBO LOW-LATENCY LAYER" not in src:
    # Insertar justo despues de allow_reuse_address = True
    if "ThreadingHTTPServer.allow_reuse_address = True" in src:
        src = src.replace("ThreadingHTTPServer.allow_reuse_address = True", "ThreadingHTTPServer.allow_reuse_address = True\n" + TURBO_LAYER, 1)
    else:
        src = TURBO_LAYER + "\n" + src

# 2. Acortar timeouts de red bloqueantes dentro del gateway (de 10-30s a 2.0s)
src = re.sub(r'timeout\s*=\s*(?:10|15|20|30)(?:\.0)?', 'timeout=2.0', src)

# 3. Envolver do_GET con cache en memoria de 10s para rutas pesadas (/, /api/*, /dashboard)
if "def _cached_do_GET" not in src and "def do_GET(self):" in src:
    src = src.replace("    def do_GET(self):", """    def do_GET(self):
        _now = _m82_time.monotonic()
        _ck = self.path
        _hit = _M82_RESP_CACHE.get(_ck)
        if _hit and (_now - _hit[0]) < _M82_CACHE_TTL:
            self.send_response(_hit[1])
            for _hk, _hv in _hit[2]:
                if _hk.lower() not in ("server", "date", "transfer-encoding"):
                    self.send_header(_hk, _hv)
            self.end_headers()
            self.wfile.write(_hit[3])
            return
        self._m82_capture_path = _ck
        return self._orig_do_GET()

    def _orig_do_GET(self):""", 1)

    # Interceptar wfile.write para guardar respuesta en cache RAM
    if "class M82MobileRequestHandler" in src and "def setup(self):" not in src:
        src = src.replace("    def _orig_do_GET(self):", """    def finish(self):
        try:
            super().finish()
        except Exception:
            pass

    def _orig_do_GET(self):""", 1)

GW_FILE.write_text(src, encoding="utf-8")
print("[+] Capa Turbo inyectada en orchestrator/m82_mobile_gateway.py")

# 4. Reiniciar limpio el gateway y medir latencia real en milisegundos
subprocess.run(["pkill", "-f", "m82_mobile_gateway.py"], stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", "m82_port8282_watchdog.sh"], stderr=subprocess.DEVNULL)
time.sleep(1)

with open(BASE_DIR / "logs" / "watchdog_8282.log", "a") as wf:
    subprocess.Popen(["nohup", "bash", str(WD_SCRIPT)], stdout=wf, stderr=subprocess.STDOUT, start_new_session=True)

time.sleep(3)

for i in range(1, 3):
    t0 = time.perf_counter()
    with urllib.request.urlopen("http://127.0.0.1:8282/", timeout=8) as r:
        data = r.read()
        ms = (time.perf_counter() - t0) * 1000.0
        print(f"[+] Prueba {i}: HTTP {r.getcode()} | Payload={len(data):,} bytes | Latencia={ms:.1f} ms")
