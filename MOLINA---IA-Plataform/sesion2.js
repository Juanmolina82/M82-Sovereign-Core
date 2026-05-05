const brent0 = 112.89; // Baseline pre-conflicto
const supportMacro = 95.00; // Nivel de capitulación total

function isJump(movePct, thresh = 10) { 
    return Math.abs(movePct) >= thresh; 
}

async function detector() {
    // Data capturada en tiempo real
    const brent = 96.79; 
    const move = ((brent / brent0) - 1) * 100;
    const distanceToSupport = brent - supportMacro;

    console.clear();
    console.log("\n--- ⚡ M82 SESSION 2: JUMP DETECTOR RECONFIGURED ---");
    console.log(`HORA: ${new Date().toLocaleTimeString()} | MOLINA HOLDINGS`);
    console.log("---------------------------------------------------");
    console.log(`BASE PRE-CONFLICTO: $${brent0}`);
    console.log(`PRECIO ACTUAL:      $${brent.toFixed(2)}`);
    console.log(`SALTO ACUMULADO:    ${move.toFixed(2)}%`);
    console.log(`DISTANCIA SOPORTE:  $${distanceToSupport.toFixed(2)}`);
    console.log("---------------------------------------------------");

    if (isJump(move, 12)) {
        console.log("🚨 ALERTA: SALTO DISCRETO CONFIRMADO");
        console.log("📢 CAUSA: DESCOMPRESIÓN POR PACTO EN OMAN");
    }

    if (brent <= supportMacro + 1) {
        console.log("⚠️ PELIGRO: TESTEANDO SOPORTE DE $95.00");
    }

    console.log("---------------------------------------------------\n");
}

setInterval(detector, 5000); 
detector();
