#!/usr/bin/env python3
import re
import time
import shutil
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
GW_FILE = BASE_DIR / "orchestrator" / "m82_mobile_gateway.py"
LOGS_DIR = BASE_DIR / "logs"
WD_SCRIPT = BASE_DIR / "m82_port8282_watchdog.sh"

# 1. Restaurar respaldo limpio si existe, o purgar los bloques inyectados previamente
backups = sorted(BASE_DIR.rglob("*m82_mobile_gateway*.py*"))
bak_candidates = [b for b in backups if "backup" in str(b).lower() or b.suffix in (".bak", ".orig")]
if bak_candidates:
    shutil.copy2(bak_candidates[-1], GW_FILE)
    print(f"[+] Restaurado desde respaldo limpio: {bak_candidates[-1]}")
else:
    src = GW_FILE.read_text(encoding="utf-8", errors="ignore")
    # Eliminar bloque TURBO LAYER y wrapper _orig_do_GET manteniendo solo el import seguro de ThreadingHTTPServer
    src = re.sub(r'# === M82 TURBO LOW-LATENCY LAYER.*?# === END M82 TURBO LAYER ===\n?', '', src, flags=re.DOTALL)
    src = re.sub(
        r'    def do_GET\(self\):\n        _now = _m82_time\.monotonic\(\).*?    def _orig_do_GET\(self\):',
        '    def do_GET(self):',
        src,
        flags=re.DOTALL
    )
    src = re.sub(
        r'    def finish\(self\):\n        try:\n            super\(\)\.finish\(\)\n        except Exception:\n            pass\n\n',
        '',
        src
    )
    # Restaurar timeouts de configuracion a 10.0s para que cargue toda la config completa
    src = src.replace("timeout=2.0", "timeout=10.0")
    GW_FILE.write_text(src, encoding="utf-8")
    print("[+] Configuracion y handlers originales de m82_mobile_gateway.py restaurados al 100%.")

# 2. Crear Proxy de Cache en RAM en segundo plano (8282 -> 8283) para respuesta <20ms sin truncar datos
PROXY_FILE = BASE_DIR / "orchestrator" / "m82_8282_instant_proxy.py"
PROXY_FILE.write_text('''#!/usr/bin/env python3
import time
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BACKEND = "http://127.0.0.1:8283"
CACHE = {}
LOCK = threading.Lock()
WARM_PATHS = ["/", "/api/status", "/api/state", "/api/config", "/api/dossier", "/api/telemetry", "/dashboard"]

def fetch_backend(path, method="GET", body=None, headers=None):
    url = BACKEND + path
    req_headers = {}
    if headers:
        for k, v in headers.items():
            if k.lower() not in ("host", "connection", "content-length", "accept-encoding"):
                req_headers[k] = v
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=20.0) as resp:
        data = resp.read()
        hdrs = [(k, v) for k, v in resp.getheaders() if k.lower() not in ("transfer-encoding", "connection", "server", "date")]
        return resp.getcode(), hdrs, data

def background_refresher():
    while True:
        with LOCK:
            keys = list(set(WARM_PATHS + list(CACHE.keys())))
        for p in keys:
            try:
                code, hdrs, data = fetch_backend(p)
                if code == 200 and len(data) > 0:
                    with LOCK:
                        CACHE[p] = (time.monotonic(), code, hdrs, data)
            except Exception:
                pass
        time.sleep(5.0)

class InstantM82Handler(BaseHTTPRequestHandler):
    def address_string(self):
        return self.client_address[0]
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        with LOCK:
            hit = CACHE.get(self.path)
        if hit and (time.monotonic() - hit[0]) < 30.0:
            self.send_response(hit[1])
            for k, v in hit[2]:
                self.send_header(k, v)
            self.send_header("X-M82-Cache", "INSTANT-RAM-HIT")
            self.end_headers()
            self.wfile.write(hit[3])
            return
        try:
            code, hdrs, data = fetch_backend(self.path, "GET", None, dict(self.headers))
            if code == 200 and len(data) > 0:
                with LOCK:
                    CACHE[self.path] = (time.monotonic(), code, hdrs, data)
            self.send_response(code)
            for k, v in hdrs:
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"M82 Gateway Warming Up: {e}".encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length > 0 else None
        try:
            code, hdrs, data = fetch_backend(self.path, "POST", body, dict(self.headers))
            with LOCK:
                CACHE.clear()
            self.send_response(code)
            for k, v in hdrs:
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(str(e).encode())

if __name__ == "__main__":
    t = threading.Thread(target=background_refresher, daemon=True)
    t.start()
    ThreadingHTTPServer.allow_reuse_address = True
    srv = ThreadingHTTPServer(("0.0.0.0", 8282), InstantM82Handler)
    srv.serve_forever()
''', encoding="utf-8")
PROXY_FILE.chmod(0o755)

# 3. Preparar lanzador interno en puerto 8283 y actualizar watchdog perpetuo para ambos
BACKEND_RUNNER = BASE_DIR / "orchestrator" / "run_gateway_8283.py"
BACKEND_RUNNER.write_text(f'''#!/usr/bin/env python3
from pathlib import Path
src = Path("{GW_FILE}").read_text(encoding="utf-8", errors="ignore")
src = src.replace("8282", "8283")
exec(compile(src, "{GW_FILE}", "exec"), {{"__name__": "__main__", "__file__": "{GW_FILE}"}})
''', encoding="utf-8")
BACKEND_RUNNER.chmod(0o755)

WD_SCRIPT.write_text(f"""#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
export PYTHONUNBUFFERED=1
while true; do
    if ! python3 -c "import socket; s=socket.create_connection(('127.0.0.1',8283),1); s.close()" 2>/dev/null; then
        pkill -f "run_gateway_8283.py" 2>/dev/null || true
        sleep 1
        nohup python3 -u "{BACKEND_RUNNER}" >> "{LOGS_DIR}/server_8283.log" 2>&1 &
        sleep 2
    fi
    if ! python3 -c "import socket; s=socket.create_connection(('127.0.0.1',8282),1); s.close()" 2>/dev/null; then
        pkill -f "m82_8282_instant_proxy.py" 2>/dev/null || true
        sleep 1
        nohup python3 -u "{PROXY_FILE}" >> "{LOGS_DIR}/proxy_8282.log" 2>&1 &
        sleep 2
    fi
    sleep 5
done
""", encoding="utf-8")
WD_SCRIPT.chmod(0o755)

# 4. Reiniciar todo y medir latencia y tamano completo de respuesta
subprocess.run(["pkill", "-f", "m82_port8282_watchdog.sh"], stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", "m82_mobile_gateway.py"], stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", "run_gateway_8283.py"], stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", "m82_8282_instant_proxy.py"], stderr=subprocess.DEVNULL)
time.sleep(1)

with open(LOGS_DIR / "watchdog_8282.log", "a") as wf:
    p = subprocess.Popen(["nohup", "bash", str(WD_SCRIPT)], stdout=wf, stderr=subprocess.STDOUT, start_new_session=True)

time.sleep(5)

for i in range(1, 3):
    t0 = time.perf_counter()
    with urllib.request.urlopen("http://127.0.0.1:8282/", timeout=15) as r:
        data = r.read()
        ms = (time.perf_counter() - t0) * 1000.0
        cache_hdr = r.headers.get("X-M82-Cache", "FIRST-WARM")
        print(f"[+] Prueba {i}: HTTP {r.getcode()} | Payload={len(data):,} bytes | Latencia={ms:.1f} ms | Mode={cache_hdr}")
