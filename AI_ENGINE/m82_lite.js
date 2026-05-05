const express = require('express');
const app = express();
app.get('/', (req, res) => {
    res.send(`<body style="background:#000;color:#D4AF37;font-family:monospace;padding:20px;">
        <h2>🏛️ M82 ARCHITECTURE - RESCUE MODE</h2>
        <hr border="1" color="#D4AF37">
        <p><b>ALGO REGIME (Rt):</b> ${Math.tanh(0.7).toFixed(4)}</p>
        <p><b>HORMUZ STRESS (Ht):</b> ${Math.tanh(2.1).toFixed(4)}</p>
        <p><b>STRATEGY:</b> JSOC IRAN / NUCLEAR MATERIAL OPS</p>
        <div style="background:#b00;color:#fff;padding:10px;"><b>ALERTA:</b> SISTEMA EN MODO ESTABLE</div>
    </body>`);
});
app.listen(3000, '127.0.0.1', () => console.log('SISTEMA RESCATADO EN http://127.0.0.1:3000'));
