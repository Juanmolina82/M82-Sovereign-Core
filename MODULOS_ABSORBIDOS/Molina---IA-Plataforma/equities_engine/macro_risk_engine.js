// macro_risk_engine.js
// Macro risk overlay para Molina Holdings LLC

// Parámetros editables (0 a 1)
const params = {
  legacy_oil_cartel_power: 0.7,      // poder histórico de carteles tipo Rockefeller
  corporate_collaboration_risk: 0.6, // riesgo de colusión empresas–regímenes
  iran_nuclear_risk: 0.8,
  venezuela_sanctions_risk: 0.9,
  great_power_tension: 0.85,         // EEUU–China–Rusia
};

// Ponderaciones por bloque de activos
const weights = {
  us_energy_infra: { base: 0.25 },
  global_oil_majors: { base: 0.25 },
  venezuela_exposed: { base: 0.10 },
  uranium_nukes: { base: 0.10 },
  renewables_clean: { base: 0.20 },
  cash_gold_defensive: { base: 0.10 },
};

function computeAdjustments(p = params) {
  const {
    legacy_oil_cartel_power,
    corporate_collaboration_risk,
    iran_nuclear_risk,
    venezuela_sanctions_risk,
    great_power_tension,
  } = p;

  // Riesgo sistémico energía fósil
  const fossilSystemicRisk =
    0.4 * legacy_oil_cartel_power +
    0.2 * corporate_collaboration_risk +
    0.2 * iran_nuclear_risk +
    0.2 * great_power_tension;

  // Riesgo Venezuela específico
  const venezuelaRisk =
    0.6 * venezuela_sanctions_risk +
    0.2 * great_power_tension +
    0.2 * corporate_collaboration_risk;

  // Ajustes simples a pesos (clamp entre 0 y 1)
  function clamp(x, min = 0, max = 1) {
    return Math.min(max, Math.max(min, x));
  }

  const adj = { ...weights };

  // Menos peso en oil fósil si el riesgo sistémico es alto
  adj.us_energy_infra.target =
    weights.us_energy_infra.base * (1 - 0.4 * fossilSystemicRisk);
  adj.global_oil_majors.target =
    weights.global_oil_majors.base * (1 - 0.5 * fossilSystemicRisk);

  // Corte fuerte a Venezuela según riesgo
  adj.venezuela_exposed.target =
    weights.venezuela_exposed.base * (1 - 0.8 * venezuelaRisk);

  // Más peso a renovables y defensivos cuando el riesgo es alto
  adj.renewables_clean.target =
    weights.renewables_clean.base * (1 + 0.6 * fossilSystemicRisk);
  adj.cash_gold_defensive.target =
    weights.cash_gold_defensive.base * (1 + 0.5 * great_power_tension);

  // Uranio/nuclear sube con iran_nuclear_risk pero con tope
  adj.uranium_nukes.target =
    weights.uranium_nukes.base * (1 + 0.4 * iran_nuclear_risk);

  // Normalizar a que sumen 1
  let sum = 0;
  for (const k of Object.keys(adj)) {
    adj[k].target = clamp(adj[k].target);
    sum += adj[k].target;
  }
  for (const k of Object.keys(adj)) {
    adj[k].normWeight = adj[k].target / sum;
  }

  return {
    params: p,
    fossilSystemicRisk,
    venezuelaRisk,
    allocations: adj,
  };
}

function runMacroEngine(customParams) {
  const result = computeAdjustments(customParams || params);

  console.log('=== Molina Holdings – Macro Risk Overlay ===');
  console.log('Fossil systemic risk:', result.fossilSystemicRisk.toFixed(2));
  console.log('Venezuela risk     :', result.venezuelaRisk.toFixed(2));
  console.log('
Target normalized weights:');
  for (const [k, v] of Object.entries(result.allocations)) {
    console.log(
      k,
      '->',
      (v.normWeight * 100).toFixed(1) + '%'
    );
  }

  return result;
}

module.exports = { runMacroEngine, computeAdjustments, params, weights };

if (require.main === module) {
  runMacroEngine();
}
