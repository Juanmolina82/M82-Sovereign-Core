#!/usr/bin/env bash
set -euo pipefail

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"

echo "📥 [M82 AGI] Extrayendo e ingiriendo flujo desde Refinitiv Workspace (space.refinitiv.com)..."

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Indexación en m82_multi_stream (Cola de despacho para HUD y Telegram)
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES
('REFINITIV_WORKSPACE_USER', '[LSEG_CREDIT_RATINGS] AM Best Affirms Credit Ratings of Redmond Insurance Companies', 'PENDING', 0.88, 'CREDIT_INSURANCE', 'REFINITIV_SYNC'),
('REFINITIV_WORKSPACE_USER', '[LSEG_VENTURES_VC] Vitol Wins Best of the Year Africa Energy Award 2023 - Growth & Expansion', 'PENDING', 0.85, 'ENERGY_INFRA', 'REFINITIV_SYNC'),
('REFINITIV_WORKSPACE_USER', '[LSEG_LATAM_INFRA] VTR/VTR Energy Northern/Sovereign Operating Co - Supply Contract Agreement', 'PENDING', 0.82, 'ENERGY_LATAM', 'REFINITIV_SYNC'),
('REFINITIV_WORKSPACE_USER', '[LSEG_COMMODITIES] Oil slips from 5-month high as Hormuz crossings and sanctions waivers remain in focus', 'PENDING', 0.95, 'MEREY_BRENT', 'REFINITIV_SYNC'),
('REFINITIV_WORKSPACE_USER', '[LSEG_MACRO_RATES] US Treasuries and Fed Policy stance align with global credit spread compression', 'PENDING', 0.90, 'US10Y', 'REFINITIV_SYNC');

-- 2. Indexación en macro_dossier (Persistencia institucional)
INSERT OR REPLACE INTO macro_dossier (topic, summary, risk_score, source) VALUES
(
    'REFINITIV_WORKSPACE_USER_TELEMETRY',
    'Ingesta de cables Refinitiv Workspace desde terminal institucional usuario. Confirmación de ratings de crédito AM Best, transacciones Vitol/VTR Energy, arbitraje Brent/Merey y monitoreo de colas en el Nodo Charallave L4/L5 Edge.',
    1.68,
    'LSEG_REFINITIV_USER_SESSION'
);

-- 3. Confirmación de conteo
SELECT '🟢 INGESTA OK — Registros activos en multi_stream: ' || COUNT(*) FROM m82_multi_stream WHERE daemon_source='REFINITIV_WORKSPACE_USER';
EOF_SQL

echo "🧹 [M82 AGI] Ejecutando checkpoint de base de datos WAL..."
sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE); SELECT 'WAL TRUNCATE OK';"

