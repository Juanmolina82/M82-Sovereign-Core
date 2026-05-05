const market = { asia_crack: 75, eu_crack: 45, us_crack: 30 };
const priority = Object.keys(market).reduce((a, b) => market[a] > market[b] ? a : b);

console.log('--- MOLINA HOLDINGS: PRIORIZACIÓN TEÓRICA ---');
console.log('MARCO: Utilidad Marginal del Destilado (Diésel)');
console.log('ESTATUS: El mercado con mayor dolor físico es ' + priority.toUpperCase());
console.log('DECISIÓN M82: Venezuela prioriza suministro a ' + priority.toUpperCase());
