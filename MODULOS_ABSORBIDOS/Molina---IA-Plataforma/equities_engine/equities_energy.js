// === Equities Engine (orquestador principal) ===

const path = require('path');

function loadModule(modulePath, fallbackName) {
  try {
    const mod = require(modulePath);
    if (typeof mod.runEngine === 'function') return mod.runEngine;
    if (typeof mod.runEnergyEngine === 'function') return mod.runEnergyEngine;
    if (typeof mod.runEvEngine === 'function') return mod.runEvEngine;
    console.error(`Módulo ${modulePath} cargado pero sin función runner válida.`);
    return null;
  } catch (e) {
    console.error(`No se pudo cargar ${fallbackName} (${modulePath}):`, e.message);
    return null;
  }
}

const runEnergy = loadModule('./equities_energy', 'energy');
const runEv = loadModule('./equities_ev', 'ev');

async function main() {
  const arg = process.argv[2]; // 'energy', 'ev' o vacío

  if (!arg || arg === 'all') {
    console.log('=== Corriendo TODOS los engines (energy + ev) ===');
    if (runEnergy) await runEnergy();
    if (runEv) await runEv();
    return;
  }

  if (arg === 'energy') {
    console.log('=== Corriendo solo Energy Infrastructure Engine ===');
    if (runEnergy) await runEnergy();
    return;
  }

  if (arg === 'ev') {
    console.log('=== Corriendo solo EV Sector Engine ===');
    if (runEv) await runEv();
    return;
  }

  console.log('Uso:');
  console.log('  node equities_engine.js           # corre todos');
  console.log('  node equities_engine.js all       # corre todos');
  console.log('  node equities_engine.js energy    # solo energía');
  console.log('  node equities_engine.js ev        # solo EV');
}

main();