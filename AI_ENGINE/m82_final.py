import http.server, socketserver

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { background:#000; color:#eee; font-family:monospace; margin:0; overflow:hidden; border:2px solid #333; }
        .grid-master { display: grid; grid-template-columns: 1.2fr 1fr; grid-template-rows: 1fr 1fr; height: 100vh; gap: 2px; background: #333; }
        .block { background: #000; padding: 15px; display: flex; flex-direction: column; justify-content: center; }
        
        /* Bloque Superior Izquierdo: Identidad */
        .id-block { border-bottom: 1px solid #333; }
        .brand { color: #4aa3df; font-size: 20px; font-weight: bold; }
        .slogan { color: #888; font-size: 12px; margin-bottom: 10px; }
        
        /* Bloque Inferior Izquierdo: Noticias */
        .news-block { border-top: 1px solid #333; justify-content: flex-start; }
        .news-item { font-size: 12px; margin: 5px 0; color: #ccc; }
        .news-item:before { content: "> "; color: #0f0; }

        /* Bloque Superior Derecho: Indice Global */
        .index-block { text-align: center; }
        .global-val { font-size: 28px; font-weight: bold; color: #eee; }
        
        /* Bloque Inferior Derecho: Activos y Footer */
        .assets-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 12px; }
        .up { color: #0f0; } .down { color: #f33; }
        .footer { margin-top: 10px; padding-top: 10px; border-top: 1px dashed #333; font-size: 11px; text-align: center; }
    </style>
</head>
<body>
    <div class="grid-master">
        <div class="block id-block">
            <div class="brand">🏛️ NUESTRO PROYECTO</div>
            <div class="slogan">"Inteligencia en Vivo"</div>
            <div style="font-size: 14px; color: #4aa3df;" id="clock">12:58 PM | ABR 15, 2026</div>
        </div>
        
        <div class="block index-block">
            <div style="font-size: 10px; color: #888;">INDICE GLOBAL (GRÁFICO)</div>
            <div class="global-val" id="g-val">8978.69</div>
            <div class="up" id="g-pct">▲ +0.09%</div>
        </div>

        <div class="block news-block">
            <b style="color: #0f0; margin-bottom: 5px;">TOP STORIES</b>
            <div class="news-item">Innovación en IA impulsa mercados</div>
            <div class="news-item">Mercado se estabiliza tras apertura</div>
            <div class="news-item">Nueva política tech en revisión</div>
        </div>

        <div class="block">
            <div class="assets-grid">
                <div>
                    <b style="color:#4aa3df">MÁS ACTIVOS</b><br>
                    Accion A<br>Accion B<br>Accion C
                </div>
                <div style="text-align: right;">
                    DOW <span class="down">▼</span><br>
                    S&P <span class="up">▲</span><br>
                    NASDAQ <span class="up">▲</span>
                </div>
            </div>
            <div class="footer">
                <b style="color:cyan">PRÓXIMO: "El Cierre"</b><br>
                [ABR 15, 2026]
            </div>
        </div>
    </div>
    <script>
        function update() {
            const g = document.getElementById('g-val');
            let val = parseFloat(g.innerText);
            let change = (Math.random() - 0.48) * 2;
            g.innerText = (val + change).toFixed(2);
            document.getElementById('clock').innerText = new Date().toLocaleString();
        }
        setInterval(update, 2000);
    </script>
</body>
</html>
"""

class S(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("0.0.0.0", 8080), S)
print("SISTEMA M82 INTEGRADO: http://localhost:8080")
httpd.serve_forever()
