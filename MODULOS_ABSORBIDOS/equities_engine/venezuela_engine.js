const fs = require('fs');
const path = require('path');

function loadCsv(fileName) {
  const filePath = path.join(__dirname, fileName);
  const text = fs.readFileSync(filePath, 'utf8').trim();
  const lines = text.split('
');
  const text = fs.readFileSync(filePath, 'utf8').trim();
const lines = text.split('
');
const header = lines[0].split(',');    return row;
  });
}

function loadProduction() {
  const rows = loadCsv('data/venezuela/oil_production_ve.csv')
    .map(r => ({
      year: Number(r.year),
      production_bpd: Number(r.production_bpd),
      production_opec_bpd: Number(r.production_opec_bpd),
    }))
    .sort((a, b) => a.year - b.year);

  for (let i = 0; i < rows.length; i++) {
    if (i === 0) {
      rows[i].production_change_pct = null;
    } else {
      const prev = rows[i - 1].production_bpd;
      const cur = rows[i].production_bpd;
      rows[i].production_change_pct = prev ? ((cur - prev) / prev) * 100 : null;
    }
  }
  return rows;
}

const productionSeries = loadProduction();

function getVenezuelaOilProfile() {
  return productionSeries;
}

function getVenezuelaOilYear(year) {
  return productionSeries.find(r => r.year === year) || null;
}

module.exports = { getVenezuelaOilProfile, getVenezuelaOilYear };
