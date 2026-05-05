const escenarios = [
  { nombre: "PAZ EN ORMUZ", asia_crack: 25, eu_crack: 35, us_crack: 20, desc: "Normalización." },
  { nombre: "INVIERNO ÁRTICO EN EUROPA", asia_crack: 40, eu_crack: 95, us_crack: 35, desc: "Crisis de calefacción." },
  { nombre: "BLOQUEO EN SUEZ", asia_crack: 85, eu_crack: 50, us_crack: 30, desc: "Pánico físico en Asia." }
];

console.log('--- M82: SIMULADOR DE ADAPTABILIDAD ---');

escenarios.forEach((esc, i) => {
  const priority = Object.keys(esc).filter(k => k !== 'nombre' && k !== 'desc')
                    .reduce((a, b) => esc[a] > esc[b] ? a : b);
  
  setTimeout(() => {
    console.log('\n-------------------------------------------');
    console.log('EVENTO: ' + esc.nombre);
    console.log('ANÁLISIS M82: Prioridad en ' + priority.toUpperCase() + ' ($' + esc[priority] + ')');
    console.log('ACCIÓN: Redirigir cargamentos de Venezuela a ' + priority.toUpperCase());
  }, i * 2500);
});
