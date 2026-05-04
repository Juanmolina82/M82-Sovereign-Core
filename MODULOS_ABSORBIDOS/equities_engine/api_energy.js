const express = require('express');
const { runEngine } = require('./equities_energy');

const app = express();
const port = 3000;

app.get('/energy', async (req, res) => {
  try {
    const results = await runEngine(true);
    res.json({ ok: true, data: results });
  } catch (e) {
    console.error('Error en /energy:', e);
    res.status(500).json({ ok: false, error: e.message });
  }
});

app.get('/', (req, res) => {
  res.send('Equities Engine API funcionando');
});

app.listen(port, () => {
  console.log(`API Energy escuchando en http://localhost:${port}`);
});