const ingresos_petroleros = 1000000000; // 1 Billón Base
const poblacion = 30000000;
const fondo_soberano = ingresos_petroleros * 0.40;
const dividendo_ciudadano = (ingresos_petroleros * 0.20) / poblacion;

console.log('--- MOLINA HOLDINGS: MODELO DE RIQUEZA CIUDADANA ---');
console.log('FONDO SOBERANO (Style: Norway): $' + fondo_soberano.toLocaleString());
console.log('DIVIDENDO ANUAL POR VENEZOLANO: $' + dividendo_ciudadano.toFixed(2));
console.log('ESTATUS M82: Transparencia total vía LAR activada.');
