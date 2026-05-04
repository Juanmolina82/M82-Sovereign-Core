const axios = require('axios');

const ALPHA_API_KEY = 'CH3RKYE8TCOX5MZ8';

const symbols = ['ENB', 'WMB', 'KMI', 'OKE', 'NEE'];

const currentPositions = {
  ENB: { shares: 0 },
  WMB: { shares: 0 },
  KMI: { shares: 0 },
  OKE: { shares: 0 },
  NEE: { shares: 0 },
};

const totalEquityWeight = 0.20;
const nav = 162000;

async function fetchFundamentals(symbol) {
  try {
    const overviewUrl = `https://www.alphavantage.co/query?function=OVERVIEW&symbol=${symbol}&apikey=${ALPHA_API_KEY}`;
    const quoteUrl = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${ALPHA_API_KEY}`;

    const [overviewResp, quoteResp] = await Promise.all([
      axios.get(overviewUrl),
      axios.get(quoteUrl),
    ]);

    const overview = overviewResp.data || {};
    const quote = quoteResp.data && quoteResp.data['Global Quote'] ? quoteResp.data['Global Quote'] : {};

    const price = parseFloat(quote['05. price']) || 0;
    const epsNow = parseFloat(overview.EPS) || 0;
    const profitMargin = parseFloat(overview.ProfitMargin) || 0;
    const peRatio = parseFloat(overview.PERatio) || 0;
    const revenueTTM = parseFloat(overview.RevenueTTM) || 0;

    return {
      symbol,
      price,
      revenueNow: revenueTTM,
      revenuePrev: revenueTTM * 0.9,
      epsNow,
      epsPrev: epsNow * 0.8,
      marginNow: profitMargin,
      pe: peRatio || 0,
    };
  } catch (err) {
    console.error('Error fetching fundamentals for', symbol, err.message);
    return {
      symbol,
      price: 0,
      revenueNow: 0,
      revenuePrev: 0,
      epsNow: 0,
      epsPrev: 0,
      marginNow: 0,
      pe: 0,
    };
  }
}

async function loadEquities() {
  const results = [];
  for (const s of symbols) {
    const data = await fetchFundamentals(s);
    results.push(data);
    await new Promise((res) => setTimeout(res, 15000));
  }
  return results;
}

// === 2) Calcular scores ===

function computeScores(stocks) {
  const valid = stocks.filter((s) => s.price > 0);
  if (valid.length === 0) return [];

  const peMean =
    valid.reduce((sum, s) => sum + s.pe, 0) / valid.length || 1;
  const peStd =
    Math.sqrt(
      valid.reduce((sum, s) => sum + (s.pe - peMean) ** 2, 0) /
        valid.length
    ) || 1;

  return valid.map((s) => {
    const gRev = s.revenuePrev > 0 ? s.revenueNow / s.revenuePrev - 1 : 0;
    const gEps = s.epsPrev > 0 ? s.epsNow / s.epsPrev - 1 : 0;
    const margin = s.marginNow;

    const zPe = peStd !== 0 ? (s.pe - peMean) / peStd : 0;

    const quality = 0.4 * gRev + 0.4 * gEps + 0.2 * margin;
    const value = -zPe;

    const score = 0.6 * quality + 0.4 * value;

    return { ...s, gRev, gEps, quality, value, score };
  });
}

// === 3) Scores -> pesos y acciones objetivo (top 3 mejores) ===

function computeWeights(scored) {
  if (scored.length === 0) return [];

  const sorted = [...scored].sort((a, b) => b.score - a.score);
  const top = sorted.slice(0, 3);

  const positives = top.map((s) => Math.max(s.score, 0));
  const sumPos = positives.reduce((a, b) => a + b, 0) || 1;

  const topWithWeights = top.map((s, i) => {
    const w = (positives[i] / sumPos) * totalEquityWeight;
    const targetValue = nav * w;
    const targetShares = s.price > 0 ? targetValue / s.price : 0;
    return { ...s, weight: w, targetValue, targetShares };
  });

  return scored.map((s) => {
    const found = topWithWeights.find((t) => t.symbol === s.symbol);
    if (!found) {
      return { ...s, weight: 0, targetValue: 0, targetShares: 0 };
    }
    return found;
  });
}

// === 4) Orquestar todo ===

async function runEngine() {
  console.log('Cargando infraestructura energía desde Alpha Vantage...');
  const equities = await loadEquities();

  const scored = computeScores(equities);
  const weighted = computeWeights(scored);

  console.log('Energy Infrastructure engine output:');
  weighted.forEach((s) => {
    const current = currentPositions[s.symbol]?.shares || 0;
    const sharesToTrade = s.targetShares - current;

    console.log(
      s.symbol,
      '| price:', s.price.toFixed(2),
      '| score:', s.score.toFixed(3),
      '| weight:', (s.weight * 100).toFixed(2) + '%',
      '| targetShares:', s.targetShares.toFixed(2),
      '| current:', current.toFixed(2),
      '| trade (buy+ / sell-):', sharesToTrade.toFixed(2)
    );
  });
}

runEngine();
