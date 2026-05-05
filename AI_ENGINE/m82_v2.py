import http.server
import socketserver

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background-color: #000; color: #eee; font-family: sans-serif; margin: 0; overflow: hidden; }
        .grid-master { display: grid; grid-template-columns: 1.5fr 1fr; height: 100vh; }
        .left-panel { border-right: 1px solid #333; display: flex; flex-direction: column; padding: 15px; }
        .brand-header { border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 15px; }
        .brand-name { font-size: 22px; font-weight: bold; color: #4aa3df; text-transform: uppercase; }
        .news-item { padding: 8px 0; border-bottom: 1px solid #1a1a1a; font-size: 14px; color: #ccc; }
        .news-item::before { content: "> "; color: #4CD964; }
        .right-panel { display: flex; flex-direction: column; background-color: #050505; }
        .main-index { padding: 20px; text-align: center; border-bottom: 1px solid #333; }
        .market-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background-color: #333; flex-grow: 1; }
        .item { background-color: #000; padding: 20px; display: flex; flex-direction: column; justify-content: center; border: 0.5px solid #1a1a1a; }
        .label { font-size: 11px; color: #888; text-transform: uppercase; }
        .value { font-size: 18px; font-weight: bold; margin-top: 5px; }
        .up { color: #4CD964; }
        .down { color: #FF3B30; }
        .footer-tag { background: #002244; color: #fff; padding: 10px; text-align: center; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="grid-master">
        <div class="left-panel">
            <div class="brand-header">
                <div class="brand-name">MOLINA HOLDINGS LLC</div>
                <div style="font-size: 11px; color: #888;" id="clock">CONECTANDO...</div>
            </div>
            <h4 style="color: #4CD964; margin: 5px 0;">TOP STORIES</h4>
            <div class="news-item">IA Generativa impulsa nuevos máximos en NVIDIA</div>
            <div class="news-item">Molina Holdings expande infraestructura de datos</div>
            <div class="news-item">Mercados asiáticos cierran con tendencia mixta</div>
            <div class="news-item">Actualización de flujo institucional activa</div>
        </div>
        <div class="right-panel">
            <div class="main-index">
                <div class="label">S&P 500 GLOBAL</div>
                <div class="value" id="main-val" style="font-size: 32px;">$5,221.40</div>
                <div class="up" style="font-size: 14px;">▲ +0.09%</div>
            </div>
            <div class="market-grid">
                <div class="item"><span class="label">DOW</span><span class="value down" id="val-0">38,461</span></div>
                <div class="item"><span class="label">NASDAQ</span><span class="value up" id="val-1">16,332</span></div>
                <div class="item"><span class="label">BTC/USD</span><span class="value down" id="val-2">63,120</span></div>
                <div class="item"><span class="label">GOLD</span><span class="value up" id="val-3">2,384</span></div>
                <div class="item"><span class="label">VIX</span><span class="value down" id="val-4">14.21</span></div>
                <div class="item"><span class="label">INDEX</span><span class="value" style="color:cyan">M82-OK</span></div>
            </div>
            <div class="footer-tag">PRÓXIMO: "EL CIERRE"</div>
        </div>
    </div>
    <script>
        function updateClock() { document.getElementById('clock').innerText = new Date().toLocaleString(); }
        setInterval(updateClock, 1000);
        function simulateMarket() {
            for(let i=0; i<5; i++) {
                let el = document.getElementById('val-' + i);
                let current = parseFloat(el.innerText.replace(',', ''));
                let change = (Math.random() - 0.5) * 10;
                el.innerText = (current + change).toFixed(2);
                el.className = change > 0 ? "value up" : "value down";
            }
        }
        setInterval(simulateMarket, 3000);
    </script>
</body>
</html>
"""

class Server(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))

print("[U82] SISTEMA RESTAURADO: http://localhost:8080")
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("0.0.0.0", 8080), Server)
httpd.serve_forever()
