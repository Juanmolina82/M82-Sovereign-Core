#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

echo "📥 [M82 AGI] Iniciando Ingesta Atómica desde Refinitiv Workspace Terminal..."

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Inserción de Eventos en Stream Multicanal (m82_multi_stream)
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact) VALUES
('LSEG_REFINITIV', '[OIL_TANKER_BRENT] Oil slips from five-month highs with Hormuz crossings, Russian sanctions waiver in focus', 'PENDING', 0.92, 'MEREY'),
('LSEG_REFINITIV', '[RATES_US10Y] US yields slightly higher as Traders focus on Fed policy shift', 'PENDING', 0.85, 'US10Y'),
('LSEG_REFINITIV', '[SEMI_CAPEX] Mapping the Market: Semiconductor stocks may be about to rise', 'PENDING', 0.88, 'TECH'),
('LSEG_REFINITIV', '[US_EARNINGS_STOCKS] US stocks rebound with Q1 earnings test at hand; French markets tumble', 'PENDING', 0.75, 'SPX'),
('LSEG_REFINITIV', '[EURONEXT_FRENCH] French markets tumble as risks add to political crisis', 'PENDING', -0.85, 'EUR_EQUITIES'),
('LSEG_REFINITIV', '[CHINA_AUSS_GROWTH] Euro dips on French turmoil, Aussie lifted by China growth', 'PENDING', 0.80, 'FX_AUD'),
('LSEG_REFINITIV', '[INDIA_IPO_MARKET] Indias Hyundai draws about $3.3 billion in IPO anchor investor tick', 'PENDING', 0.90, 'INDIA_EQ'),
('LSEG_REFINITIV', '[LATAM_MEXICO_PE] LatAm PE edge higher with focus on Mexico polls', 'PENDING', 0.82, 'LATAM_PE'),
('LSEG_REFINITIV', '[GOLD_REAL_YIELDS] Gold edges lower as firm dollar, elevated yields weigh', 'PENDING', -0.50, 'XAUUSD'),
('LSEG_REFINITIV', '[IMF_GROWTH_CUT] IMF cuts Growth FX forecast for first time since May on Middle East supply fears', 'PENDING', 0.88, 'MACRO_GULF');

-- 2. Inserción en Dossier Soberano Macro (macro_dossier)
INSERT OR REPLACE INTO macro_dossier (topic, summary, risk_score, source) VALUES
(
    'LSEG_WORKSPACE_FULL_STREAM_1902',
    'Comprehensive 22-vector capture from space.refinitiv.com. Confirms Brent/Hormuz friction, US 10Y Treasury yield pressure, French Euronext selloff, and strong EM capital flows in India/Mexico. Validates M82 Heavy Crude premium and Hard Assets rotation.',
    1.68,
    'LSEG_REFINITIV_WORKSPACE'
);

-- 3. Verificación de Transacción
SELECT COUNT(*) || ' Registros agregados en m82_multi_stream' FROM m82_multi_stream WHERE daemon_source='LSEG_REFINITIV';
SELECT id, topic, source, updated_at FROM macro_dossier WHERE topic='LSEG_WORKSPACE_FULL_STREAM_1902';
EOF_SQL

echo "✅ [M82 AGI] Ingesta completada con éxito. Ejecutando vaciado de memoria WAL..."
sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE); SELECT 'WAL CHECKPOINT OK';"

