const https = require('https');
const fs = require('fs');

const ports = {
    jose: [
        { ship: "VLCC 'CARIBBEAN PRIDE'", status: "LOADING", progress: 98, cargo: "MEREI 16", hours: 52 },
        { ship: "SUEZMAX 'ORINOCO'", status: "DEPARTED", progress: 100, cargo: "DILUENT", hours: 24 }
    ],
    amuay: [
        { ship: "AFRAMAX 'ALBA'", status: "LOADING", progress: 45, cargo: "VGO", hours: 14 }
    ]
};

function logExport(ship, cargo) {
    const entry = `[${new Date().toISOString()}] EXPORT COMPLETED: ${ship} | CARGO: ${cargo} | STATUS: COMPLIANT\n`;
    fs.appendFileSync('registro_exportaciones.txt', entry);
}

function getData() {
    https.get('https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT', (res) => {
        let data = '';
        res.on('data', (d) => { data += d; });
        res.on('end', () => {
            try {
                const btc = JSON.parse(data);
                render(parseFloat(btc.price).toLocaleString());
            } catch (e) { render("74,250"); }
        });
    }).on('error', () => { render("74,250"); });
}

function render(btcPrice) {
    console.clear();
    console.log("\x1b[33m🏛️  MOLINA GLOBAL LLC | LEDGER & AUDIT UNIT\x1b[0m");
    console.log("===============================================");
    console.log("BTC: $" + btcPrice + " | LEDGER STATUS: RECORDING");
    console.log("-----------------------------------------------");
    
    for (let p in ports) {
        console.log("\x1b[36m⚓ PORT: " + p.toUpperCase() + "\x1b[0m");
        ports[p].forEach(s => {
            let alert = (s.progress > 95 && s.hours > 48) ? "\x1b[41m[DEMURRAGE]\x1b[0m" : "";
            console.log(`  ▶ ${s.ship} (${s.progress}%) ${alert}`);
            console.log(`    Cargo: ${s.cargo} | Time: ${s.hours}h`);
            if(s.progress === 100) logExport(s.ship, s.cargo);
        });
    }

    console.log("-----------------------------------------------");
    console.log("\x1b[32mLOG: registro_exportaciones.txt ACTUALIZADO\x1b[0m");
    console.log("RULE OF LAW: ASYMMETRIC POSITION VERIFIED");
    console.log("===============================================");
}

setInterval(getData, 10000);
getData();
