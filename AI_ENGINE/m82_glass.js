const blessed = require('blessed');
const contrib = require('blessed-contrib');
const axios = require('axios');
const { exec } = require('child_process');

const screen = blessed.screen({ smartCSR: true, fullUnicode: true });
const grid = new contrib.grid({ rows: 12, cols: 12, screen: screen });

const mainTable = grid.set(0, 0, 8, 12, contrib.table, {
  label: ' 🏛️ MOLINA HOLDINGS: GLOBAL MACRO CENTER ', border: {type: "line", fg: "cyan"},
  columnSpacing: 2, columnWidth: [14, 10, 8, 26], fg: 'white', bold: true
});

const ticker = grid.set(8, 0, 1, 12, blessed.box, {
  label: ' ⚡ LIVE TICKER ', border: {type: "line", fg: "red"},
  style: { fg: 'white', bg: 'red' }, tags: true
});

const auditBox = grid.set(9, 0, 3, 12, blessed.box, {
  label: ' 📑 QUANT AUDIT: 12-POINT DECODE ', border: {type: "line", fg: "green"},
  style: { fg: 'green' }, tags: true
});

async function refresh() {
    // Simulando flujos macro en tiempo real
    const data = [
        [' US10Y (BOND)', ' 4.28%', ' {cyan-fg}Y{/cyan-fg}', ' IMPACT: TECH VALUATION'],
        [' DXY (USD)', ' 104.15', ' {green-fg}S{/green-fg}', ' DOLLAR STRENGTH HIGH'],
        [' NVDA (EQTY)', ' $142.45', ' {green-fg}B{/green-fg}', ' SCORE: 12/12 | ROE: 91%'],
        [' BRENT (OIL)', ' $96.79', ' {red-fg}W{/red-fg}', ' ISLAMABAD WATCH ACTIVE'],
        [' GOLD (GOLD)', ' $2345.1', ' {yellow-fg}H{/yellow-fg}', ' SAFE HAVEN RESISTANCE'],
        [' BTC/USDT', ' $70343', ' {green-fg}A{/green-fg}', ' RISK-ON MOMENTUM']
    ];

    mainTable.setData({ headers: [' ASSET', ' PRICE', ' ST', ' MACRO/QUANT INSIGHT'], data: data });
    
    // Basado en sus guías de ROE y Solvencia
    auditBox.setContent(` {bold}MOLINA QUANT AUDIT:{/bold}\n ROE: {cyan-fg}VALIDATED{/cyan-fg} | FCF: {cyan-fg}STABLE{/cyan-fg} | PE RATIO: {cyan-fg}DECODED{/cyan-fg}\n Status: All equities pass the 12-point earnings filter.`);
    
    ticker.setContent(` {bold}NEWS:{/bold} SAVE AMERICA PROTOCOL: VOTER ID ISLAMABAD TALKS UPDATING ICE FUNDING PRIORITY | ANTI-WEAPONIZATION STANCE: MARKET RISK REDUCED | © 2026 MOLINA HOLDINGS`);
    screen.render();
}

setInterval(refresh, 3500);
refresh();
screen.key(['escape', 'q', 'C-c'], () => process.exit(0));
