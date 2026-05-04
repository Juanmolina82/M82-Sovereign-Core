const http = require('http');

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
            <h1>🚀 M82 GLOBAL HUB</h1>
            <p>CONEXIÓN DIRECTA ESTABLECIDA</p>
            <script>setTimeout(() => { location.reload(); }, 5000);</script>
        </body>
    `);
});

// El 0.0.0.0 permite que el otro teléfono te vea en el Wi-Fi
server.listen(3000, '0.0.0.0', () => {
    console.log("✅ SISTEMA REINICIADO Y LISTO");
    console.log("🔗 Entra en el otro cel a: http://TU_IP:3000");
});
0

