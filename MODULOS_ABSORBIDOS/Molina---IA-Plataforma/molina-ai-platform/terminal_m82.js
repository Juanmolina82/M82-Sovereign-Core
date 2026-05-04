const express = require('express');
const fs = require('fs');
const app = express();

app.get('/', (req, res) => {
    try {
        const data = fs.readFileSync('live_data.json', 'utf8');
        const s = JSON.parse(data);
        res.send(`
            <body style="background:#000;color:#D4AF37;font-family:monospace;padding:20px;">
                <style>
                    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
                    .ticker { background: #b00; color: #fff; padding: 15px; border: 2px solid #fff; animation: blink 1s infinite; font-size: 1.2em; }
                </style>
                <h1>🏛️ MOLINA HOLDINGS | M82 V56</h1>
                <div style="border:1px solid #D4AF37; padding:15px; background:#111;">
                    <p>RISK: <span style="color:red;">${s.risk_index}</span> | SCORE: ${s.fase3_score}</p>
                </div>
                <div class="ticker"><marquee>${s.hormuz_alert}</marquee></div>
                <script>setTimeout(()=>location.reload(), 8080)</script>
            </body>`);
    } catch (e) {
        res.send("<body style='background:#000;color:#D4AF37;'><h1>SYNCING M82...</h1><script>setTimeout(()=>location.reload(),1000)</script></body>");
    }
});

// ESCUCHA EN TODAS LAS INTERFACES (0.0.0.0)
app.listen(8080, '0.0.0.0', () => {
    console.log('✅ DASHBOARD ONLINE EN http://localhost:8080');
});
