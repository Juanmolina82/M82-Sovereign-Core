// Captura de Tickers Clave desde su Watchlist activa
let marketData = {
    nasdaq: document.querySelector('span[symbol="COMP"] .price').innerText,
    dow: document.querySelector('span[symbol="DJIA"] .price').innerText,
    oil: document.querySelector('span[symbol="CL.1"] .price').innerText,
    timestamp: new Date().toISOString()
};
console.log("M82 Intelligence Feed:", marketData);
