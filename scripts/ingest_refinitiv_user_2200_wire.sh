#!/usr/bin/env bash
set -euo pipefail

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"

echo "📥 [M82 AGI] Extrayendo e ingiriendo flujo LSEG Refinitiv Workspace (22:00 ET Capture)..."

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Indexación en m82_multi_stream (Cola de Despacho PWA :8080 & Telegram)
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES
('REFINITIV_2200_WIRE', '[US_HEAVY_CRUDE] US Heavy Petroleum prices hold multi-month highs on USGC refining demand', 'PENDING', 0.95, 'MEREY_BRENT_SPREAD', 'REFINITIV_USER_SYNC'),
('REFINITIV_2200_WIRE', '[MARITIME_GULF_ADEN] Houthis widen strikes on bulk carriers and commercial shipping in Mideast corridors', 'PENDING', 0.94, 'VLCC_SUEZMAX_RATES', 'REFINITIV_USER_SYNC'),
('REFINITIV_2200_WIRE', '[US_CANADA_TARIFFS] Canada restores steel tariffs in domestic mill protection move', 'PENDING', 0.82, 'US_CAN_TRADE', 'REFINITIV_USER_SYNC'),
('REFINITIV_2200_WIRE', '[US_HOUSING_RATES] US housing starts fall to lowest level since May 2020 amid rate freeze', 'PENDING', 0.80, 'US10Y_HOUSING', 'REFINITIV_USER_SYNC'),
('REFINITIV_2200_WIRE', '[CHINA_STIMULUS] China economic support plan relies heavily on infrastructure and state spend', 'PENDING', 0.88, 'COMMODITIES_CHINA', 'REFINITIV_USER_SYNC');

-- 2. Compilación y Resguardo en macro_dossier
INSERT OR REPLACE INTO macro_dossier (topic, summary, risk_score, source, m82_tag, sentiment) VALUES
(
    'REFINITIV_WORKSPACE_USER_CAPTURE_2200',
    'Ingesta de cables Refinitiv Workspace (22:00 ET). Confirma firmeza del petróleo pesado en EE. UU., disrupciones de flete por ataques en el Golfo de Adén, caída de construcción en EE. UU. y nuevos estímulos en China. Respalda el arbitraje Merey 16 ($93.92 live) y la postura de Búnker.',
    1.68,
    'LSEG_REFINITIV_USER_SESSION',
    'BUNKER_HOLD_030X',
    0.93
);

-- 3. Confirmación de Transacción
SELECT '🟢 INGESTA OK — Registros agregados en multi_stream: ' || COUNT(*) FROM m82_multi_stream WHERE daemon_source='REFINITIV_2200_WIRE';
SELECT id, topic, updated_at FROM macro_dossier WHERE topic='REFINITIV_WORKSPACE_USER_CAPTURE_2200';
EOF_SQL

echo "🧹 [M82 AGI] Vaciando memoria WAL (PRAGMA wal_checkpoint(TRUNCATE))..."
sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE); SELECT 'WAL CLEAN 0/0/0 OK';"

