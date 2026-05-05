import http.server, socketserver

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background:#000; color:#eee; font-family: 'Courier New', monospace; margin:0; overflow:hidden; }
        .grid-master { display: grid; grid-template-columns: 1.5fr 1fr; grid-template-rows: 150px 1fr 1fr; height: 100vh; gap: 1px; background: #222; }
        .block { background: #000; padding: 15px; display: flex; flex-direction: column; justify-content: center; }
        
        /* BLOQUE IDENTIDAD: Basado en tu logo actual */
        .brand { color: #4aa3df; font-size: 18px; font-weight: bold; text-transform: uppercase; }
        .slogan { color: #888; font-size: 10px; margin: 4px 0; }
        .id-time { color: #4aa3df; font-size: 12px; margin-top: 8px; border-top: 1px solid #222; padding-top: 4px; }

        /* BLOQUE INDICES: El layout profesional */
        .market-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: right; }
        .up { color: #0f0; } .down { color: #f33; }
        .idx-label { font-size: 11px; color: #888; text-transform: uppercase; }
        .idx-val { font-size: 18px; font-weight: bold; }

        /* BLOQUE BLOCK TRADES: El flujo dinámico que querías */
        .trade-title-buys { color: #0f0; font-size: 12px; font-weight: bold; border-bottom: 1px solid #0f0; }
        .trade-title-sells { color: #f33; font-size: 12px; font-weight: bold; border-bottom: 1px solid #f33; }
        .trade-flow { font-size: 11px; overflow: hidden; }
        .trade-item { display: flex; justify-content: space-between; padding: 3px 0; animation: flash 0.3s; }

        @keyframes flash { from { background: #222; } to { background: transparent; } }
    </style>
</head>
<body>
    <div class="grid-master">
        <div class="block">
            <div class="brand">🏛️ MOLINA HOLDINGS</div>
            <div class="slogan">"Inteligencia en Vivo" | M82 Strategic</div>
            <div class="id-time">1:16 p. m. | ABR 15, 2026</div>
        </div>

        <div class="block">
            <div class="market-grid">
                <div><span class="idx-label">S&P 500 GLOBAL</span><div class="idx-val up">$5,221.40</div></div>
                <div><span class="idx-label">CBOE VIX</span><div class="idx-val down">17.94</div></div>
            </div>
        </div>

        <div class="block trade-flow" style="grid-column: 1 / span 2; border-top:1px solid #4aa3df;">
            <div class="market-grid">
                <div><div class="trade-title-buys">BLOCK BUYS (INSTITUTIONAL)</div><div id="buys"></div></div>
                <div><div class="trade-title-sells">BLOCK SELLS (INSTITUTIONAL)</div><div id="sells"></div></div>
            </div>
        </div>

        <div class="block" style="grid-column: 1 / span 2; border-top:1px solid #333;">
            <div class="market-grid" style="grid-template-columns: repeat(4, 1fr);">
                <div><span class="idx-label">DOW</span><div class="idx-val up">38463</div></div>
                <div><span class="idx-label">NASDAQ</span><div class="idx-val down">16328</div></div>
                <div><span class="idx-label">BTC/USD</span><span class="idx-val down">63117</span></div>
                <div><span class="idx-label">M82-OK</span><span class="idx-val" style="color:cyan">ACTIVE</span></div>
            </div>
        </div>
    </div>

    <script>
        const symbols = ['AAPL', 'TSLA', 'BTC', 'NVDA', 'MSFT', 'AMZN'];
        
        function addTrade(containerId, type) {
            const container = document.getElementById(containerId);
            const asset = symbols[Math.floor(Math.random() * symbols.length)];
            const vol = (Math.random() * 40).toFixed(2) + "M";
            
            const div = document.createElement('div');
            div.className = 'trade-item';
            div.innerHTML = `<span>${asset}</span><span class="${type.toLowerCase()}">${type}</span><span>${vol}</span>`;
            
            container.prepend(div);
            if(container.children.length > 8) container.lastChild.remove();
        }

        // Generar trades dinámicos
        setInterval(() => { addTrade('buys', 'BUY'); }, 1500);
        setInterval(() => { addTrade('sells', 'SELL'); }, 2000);
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
print("[M82] SISTEMA UNIFICADO OPERATIVO: http://localhost:8080")
httpd.serve_forever()
