const axios = require('axios');

const endpoints = [
    { name: 'GLOBAL', url: 'https://api.binance.com/api/v3/ping' },
    { name: 'US-MIRROR', url: 'https://api.binance.us/api/v3/ping' },
    { name: 'EURO-NODE', url: 'https://api1.binance.com/api/v3/ping' }
];

async function checkConnectivity() {
    console.clear();
    console.log("\n--- 🛰️ M82 SESSION 3: NETWORK REDUNDANCY ---");
    console.log(`WATCHDOG STATUS: ACTIVE | ${new Date().toLocaleTimeString()}`);
    console.log("-----------------------------------------------");

    for (let node of endpoints) {
        const t1 = Date.now();
        try {
            await axios.get(node.url, { timeout: 2500 });
            const lat = Date.now() - t1;
            let status = lat < 500 ? "🟢 EXCELENTE" : "🟡 LATENCIA ALTA";
            console.log(`[${node.name}] ${status}: ${lat}ms`);
        } catch (e) {
            console.log(`[${node.name}] 🔴 BLOQUEO / TIMEOUT`);
        }
    }

    console.log("-----------------------------------------------");
    console.log("🛠️ TIP: Si todos fallan, active VPN o DNS.Google");
    console.log("📊 TRAFFIC: High Volatility (OMAN DEAL NEWS)");
    console.log("-----------------------------------------------\n");
}

setInterval(checkConnectivity, 3000);
checkConnectivity();
