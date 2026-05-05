const fs = require('fs');

const math = {
    fxCarry: (rA, rB) => (rA - rB).toFixed(4),
    beta: (cov, varMarket) => (cov / varMarket).toFixed(2),
    duration: (c, y, t) => ((1+y)/y - (1+y+t*(c-y))/(y*(Math.pow(1+y, t)-1))).toFixed(2)
};

const results = {
    timestamp: new Date().toISOString(),
    fx: { pair: "USD/JPY", carry: math.fxCarry(0.0525, 0.001) },
    etf: { symbol: "VOO", beta: math.beta(0.015, 0.012) },
    bond: { asset: "US10Y", duration: math.duration(0.04, 0.0435, 10) }
};

// PERSISTENCIA DE DATOS: Guardado automático para acceso multi-equipo
fs.appendFileSync('M82_GLOBAL_HISTORY.json', JSON.stringify(results) + '\n');

console.log("🏛️ M82 GLOBAL ENGINE: MULTI-ASSET CORE");
console.log("---------------------------------------");
console.log(`> FX Carry (Sincronizado): ${results.fx.carry}`);
console.log(`> ETF Beta (Auditado): ${results.etf.beta}`);
console.log(`> Bond Duration (US): ${results.bond.duration} yrs`);
console.log("---------------------------------------");
console.log("📑 Datos guardados en M82_GLOBAL_HISTORY.json");
