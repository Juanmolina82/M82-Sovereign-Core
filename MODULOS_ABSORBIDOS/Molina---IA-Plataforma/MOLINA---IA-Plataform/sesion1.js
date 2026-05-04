const axios = require('axios');

async function getPrices() {
    // Activos clave para la estrategia Molina
    const symbols = ['PAXGUSDT', 'BTCUSDT', 'ETHUSDT'];
    const results = {};
    
    try {
        for (let sym of symbols) {
            const res = await axios.get(`https://api.binance.com/api/v3/ticker/price?symbol=${sym}`, { timeout: 3000 });
            results[sym] = parseFloat(res.data.price).toFixed(2);
        }
        return results;
    } catch (e) { return null; }
}

async function engine() {
    const data = await getPrices();
    
    // Data de Mercado Real-Time (Ref: 10:02 AM)
    const brent = 96.79;   //
    const wti = 88.81;     //
    const natGas = 2.938;  //
    const gaso = 3.8934;   // RBOB Gasoline

    console.clear();
    console.log("\n--- 🏛️ M82 GLOBAL HUB | MOLINA HOLDINGS ---");
    console.log(`STATUS: OMAN DEAL PRICED IN | ${new Date().toLocaleTimeString()}`);
    console.log("-----------------------------------------------");
    
    console.log("🛢️  ENERGY COMPLEX:");
    console.log(`   BRENT CRUDE:  $${brent.toFixed(2)}  📉`);
    console.log(`   NYMEX WTI:    $${wti.toFixed(2)}   📉`);
    console.log(`   NATURAL GAS:  $${natGas.toFixed(3)}  📉`);
    console.log(`   GASOLINE:     $${gaso.toFixed(4)}`);
    
    console.log("\n✨ PRECIOUS METALS & RISK:");
    if (data) {
        console.log(`   GOLD (PAXG):  $${data['PAXGUSDT']}  ✅`);
        console.log(`   BITCOIN:      $${data['BTCUSDT']}  🚀`);
        console.log(`   ETHEREUM:     $${data['ETHUSDT']}`);
    } else {
        console.log("   📡 SINCRONIZANDO METALES...");
    }
    
    console.log("-----------------------------------------------");
    console.log("📢 TRUMP (09:47): 'ISRAEL ESTARÁ MUY FELIZ'");
    console.log("📊 DOW JONES: +1.96% (+892.38 pts)");
    console.log("-----------------------------------------------\n");
}

setInterval(engine, 4000);
engine();
