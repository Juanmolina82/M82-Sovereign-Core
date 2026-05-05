const axios = require('axios');

// --- Lógica del Chairman ---
function isJump(movePct, thresh = 5) {
  return Math.abs(movePct) >= thresh;
}

const pctMove = (current, initial) => ((current / initial) - 1) * 100;

async function m82_quant_live() {
    try {
        const res = await axios.get('https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT', { timeout: 5000 });
        const gold = parseFloat(res.data.price);
        
        const brent0 = 112.89; // Precio pre-conflicto
        const brent = 96.79;   // Precio actual de su última captura
        const brentMove = pctMove(brent, brent0);

        console.clear();
        console.log("\n--- 🏛️ M82 QUANT-CORE | MOLINA HOLDINGS ---");
        console.log("STATUS: MONITOR DE SALTOS ACTIVO | " + new Date().toLocaleTimeString());
        console.log("-------------------------------------------------");
        console.log(`🛢️ BRENT CRUDE:   $${brent.toFixed(2)}`);
        console.log(`📉 VARIACIÓN:      ${brentMove.toFixed(2)}%`);
        console.log(`✨ ORO (PAXG):    $${gold.toFixed(2)}`);
        console.log("-------------------------------------------------");

        if (isJump(brentMove, 10)) {
            console.log("⚡ EVENTO DE SALTO DETECTADO EN BRENT");
            console.log("📢 ESCENARIO: CAPITULACIÓN POR ACUERDO EN OMAN");
        }

        console.log("-------------------------------------------------\n");

    } catch (e) {
        process.stdout.write("📡 Sincronizando con la red... ");
    }
}

setInterval(m82_quant_live, 4000);
m82_quant_live();
