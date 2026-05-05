// ALGORITMO DE SOLVENCIA - MOLINA HOLDINGS
function calculateZScore(workingCap, totalAssets, retainedEarnings, ebit, marketCap, totalLiabilities, sales) {
    // Pesos estándar de Wall Street para empresas públicas
    const A = (workingCap / totalAssets) * 1.2;
    const B = (retainedEarnings / totalAssets) * 1.4;
    const C = (ebit / totalAssets) * 3.3;
    const D = (marketCap / totalLiabilities) * 0.6;
    const E = (sales / totalAssets) * 1.0;
    
    return (A + B + C + D + E).toFixed(2);
}

const zScore = calculateZScore(30000, 60000, 15000, 25000, 3000000, 20000, 60000);

console.log(`🏛️ MOLINA HOLDINGS: SOLVENCY AUDIT`);
console.log(`> ASSET: NVDA | Z-SCORE: ${zScore}`);
console.log(`------------------------------------------`);

if (zScore > 2.99) {
    console.log("🟢 VERDICT: SAFE ZONE - SOLVENCY GUARANTEED");
} else if (zScore >= 1.81) {
    console.log("🟡 VERDICT: GREY ZONE - CAUTION ADVISED");
} else {
    console.log("🔴 VERDICT: DISTRESS ZONE - HIGH RISK OF BANKRUPTCY");
}
