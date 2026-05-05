import http.server, socketserver

# DATA ESTRATÉGICA VENEZUELA - 16 ABRIL 2026
d = {
    "MS": "191.62", 
    "INV_TARGET": "$80,000M", 
    "BTC": "75,233", 
    "OIL_PROD": "1.2M bpd", 
    "INFL_REAL": "600%", 
    "FASE": "FASE 2: TRANSICIÓN ADMINISTRADA"
}

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body { background:#000; color:#fff; font-family:sans-serif; margin:0; overflow:hidden; }
  .bar { background:#001a33; padding:15px; border-bottom:4px solid #4aa3df; font-weight:900; font-size:26px; }
  .status-tag { background:#cc0000; padding:4px 12px; font-size:14px; float:right; border-radius:3px; }
  .main { padding:40px; border-left:12px solid #4aa3df; margin:30px; }
  .alert { color:#f33; font-weight:bold; border:1px solid #f33; padding:5px 10px; display:inline-block; margin-bottom:15px; }
  .headline { font-size:48px; font-weight:bold; text-transform:uppercase; line-height:1.1; }
  .grid { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:20px; padding:20px; background:#050505; position:fixed; bottom:60px; width:100%%; }
  .footer { background:#001a33; padding:15px; position:fixed; bottom:0; width:100%%; font-weight:bold; font-size:18px; color:#4aa3df; }
</style>
</head><body>
  <div class="bar">M82 BUSINESS <span class="status-tag">%s</span></div>
  <div class="main">
    <div class="alert">ALERTA CRÍTICA: INFLACIÓN ACTUAL %s</div>
    <div class="headline">PLAN DE INVERSIÓN: %s<br>REESTRUCTURACIÓN DE ESTADO DE DERECHO</div>
    <p style="font-size:24px; color:#aaa;">Fase 2: Molina Holdings LLC monitoreando la reconstrucción nacional.</p>
  </div>
  <div class="grid">
    <div style="font-size:22px;">INFLACIÓN: <span style="color:#f33;">%s</span></div>
    <div style="font-size:22px;">PROD. PETRÓLEO: <span style="color:#0f0;">%s ▲</span></div>
    <div style="font-size:22px;">BITCOIN: <span style="color:#0f0;">$%s</span></div>
  </div>
  <div class="footer">
    SISTEMA M82 OPERATIVO | MS: %s | S&P 500: RECORD HIGH
  </div>
</body></html>
""" % (d["FASE"], d["INFL_REAL"], d["INV_TARGET"], d["INFL_REAL"], d["OIL_PROD"], d["BTC"], d["MS"])

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", 8080), H) as httpd:
    print("[M82] M82 BUSINESS TERMINAL ACTIVADO")
    httpd.serve_forever()
