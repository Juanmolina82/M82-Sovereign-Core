import http.server, socketserver
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { background:#000; color:#eee; font-family:monospace; margin:0; overflow:hidden; }
        .grid { display:grid; grid-template-columns: 1.5fr 1fr; height:100vh; }
        .left { border-right:1px solid #333; display:flex; flex-direction:column; }
        .obs { height:35vh; background:#0a0a0a; border-bottom:2px solid #0056b3; display:flex; align-items:center; justify-content:center; }
        .trades { flex:1; padding:10px; font-size:12px; overflow:hidden; }
        .buy { color:#0f0; } .sell { color:#f33; }
        .right { display:flex; flex-direction:column; background:#050505; }
        .item { padding:15px; border-bottom:1px solid #222; }
        .val { font-size:20px; font-weight:bold; }
    </style>
</head>
<body>
    <div class="grid">
        <div class="left">
            <div class="obs"><b style="color:red">LIVE OBS READY</b></div>
            <div class="trades"><b>BLOCK TRADES</b><div id="t"></div></div>
        </div>
        <div class="right">
            <div class="item">S&P 500<div class="val" id="v0">5221.40</div></div>
            <div class="item">DOW<div class="val" id="v1">38463.17</div></div>
            <div class="item">BTC<div class="val" id="v2">63117.85</div></div>
            <div class="item">M82 IDX<div class="val" style="color:cyan">ACTIVE</div></div>
        </div>
    </div>
    <script>
        setInterval(() => {
            for(let i=0; i<3; i++) {
                let e = document.getElementById('v'+i);
                let c = (Math.random()-0.5)*5;
                e.innerText = (parseFloat(e.innerText)+c).toFixed(2);
                e.style.color = c>0 ? "#0f0" : "#f33";
            }
            const tr = document.getElementById('t');
            const d = document.createElement('div');
            const ty = Math.random()>0.5?'BUY':'SELL';
            d.innerHTML = `<span class="${ty.toLowerCase()}">${ty}</span> VOL: ${(Math.random()*10).toFixed(1)}M`;
            tr.prepend(d); if(tr.children.length>15) tr.lastChild.remove();
        }, 1000);
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
print("SISTEMA ONLINE: http://localhost:8080")
httpd.serve_forever()
