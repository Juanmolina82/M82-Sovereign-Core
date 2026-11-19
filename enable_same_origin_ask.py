#!/usr/bin/env python3
import re
from pathlib import Path

GW = Path.home() / "M82" / "orchestrator" / "m82_mobile_gateway.py"
txt = GW.read_text(encoding="utf-8", errors="ignore")

# 1. Cambiar fetch absoluto :8285 por ruta relativa /ask (compatible con Cloudflare HTTPS)
txt = txt.replace('fetch("http://127.0.0.1:8285/ask"', 'fetch("/ask"')
txt = txt.replace("fetch('http://127.0.0.1:8285/ask'", "fetch('/ask'")

# 2. Agregar handler do_POST('/ask') en M82MobileRequestHandler hacia 127.0.0.1:8285
POST_HANDLER = '''
    def do_POST(self):
        if self.path == "/ask":
            import urllib.request
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                req = urllib.request.Request(
                    "http://127.0.0.1:8285/ask",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = resp.read()
                    self.send_response(resp.status)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as exc:
                err = ('{"error":"Proxy /ask -> :8285: ' + str(exc).replace('"', "'") + '"}').encode()
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(err)
            return
        self.send_error(404)
'''

if "def do_POST(self):" not in txt:
    txt = re.sub(
        r"(class\s+M82MobileRequestHandler\s*\([^)]+\)\s*:)",
        r"\1\n" + POST_HANDLER,
        txt,
        count=1
    )

compile(txt, str(GW), "exec")
GW.write_text(txt, encoding="utf-8")
print("[+] Same-Origin POST /ask -> :8285 habilitado en m82_mobile_gateway.py (:8286)")
