const baseEnergyWeight = 0.05;  // 5% peso neutral en energía
const maxOverWeight    = 0.05;  // +5% máximo por shock => hasta 10%

let   wtiHigh  = 119;    // máximo reciente del WTI
const wtiPrice = 97.96;  // precio actual del WTI

if (wtiPrice > wtiHigh) {
  wtiHigh = wtiPrice;
}

const drawdown = (wtiHigh - wtiPrice) / wtiHigh;  // d_t

let energyWeight;
if (drawdown < 0.10) {
  energyWeight = baseEnergyWeight + maxOverWeight;
} else if (drawdown < 0.20) {
  const factor = (0.20 - drawdown) / 0.10; // de 1 a 0
  energyWeight = baseEnergyWeight + maxOverWeight * factor;
} else {
  energyWeight = baseEnergyWeight;
}

console.log('WTI high:', wtiHigh);
console.log('WTI price:', wtiPrice);
console.log('Drawdown:', (drawdown * 100).toFixed(2) + '%');
console.log('Target energy weight:', (energyWeight * 100).toFixed(2) + '%');

// === PARTE 2: NAV y XLE ===

const nav      = 162000;  // NAV total del fondo en USD
const xlePrice = 44;      // precio de XLE

const targetEnergyValue = nav * energyWeight;
const targetShares      = Math.floor(targetEnergyValue / xlePrice);

const currentXleValue = 10000;        // valor actual en XLE
const currentShares   = currentXleValue / 44;

const sharesToTrade = targetShares - currentShares;

console.log('NAV:', nav);
console.log('Target energy value:', targetEnergyValue.toFixed(2));
console.log('Target XLE shares:', targetShares);
console.log('Current XLE shares:', currentShares.toFixed(2));
console.log('Shares to trade (buy+ / sell-):', sharesToTrade.toFixed(2));
