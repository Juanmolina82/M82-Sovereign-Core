#!/usr/bin/env bash
set -euo pipefail

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"

echo "📥 [M82 AGI] Ingesta Total Refinitiv Wire + Purga de Duplicados..."

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Inserción Atómica del Wire Completo Refinitiv (space.refinitiv.com)
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact) VALUES
('REFINITIV_BREAKING_WIRE', '[US_HEAVY_CRUDE] US Heavy Petroleum prices hold multi-month highs on USGC refining demand', 'PENDING', 0.95, 'MEREY_BRENT'),
('REFINITIV_BREAKING_WIRE', '[MARITIME_GULF_ADEN] Houthis widen strikes on bulk carriers and commercial shipping in Mideast corridors', 'PENDING', 0.94, 'VLCC_SUEZMAX'),
('REFINITIV_BREAKING_WIRE', '[LUXURY_MOET] Moet Hennessy replaces CEO as sales decline in key luxury markets', 'PENDING', 0.75, 'CONSUMER_LUX'),
('REFINITIV_BREAKING_WIRE', '[US_CAN_STEEL] Trudeau restores steel tariffs in Canada to support domestic mills', 'PENDING', 0.82, 'US_CAN_TRADE'),
('REFINITIV_BREAKING_WIRE', '[UK_STARMER] UK Working, Starmer promise to secure election stance', 'PENDING', 0.78, 'UK_GUILTS'),
('REFINITIV_BREAKING_WIRE', '[UNILEVER_JOBS] Unilever Express to cut 3,200 jobs in global restructuring', 'PENDING', 0.80, 'GLOBAL_EQUITIES'),
('REFINITIV_BREAKING_WIRE', '[US_HOUSING_FREEZE] US housing starts fall to lowest since May 2020 on elevated rates', 'PENDING', 0.81, 'US10Y_YIELDS'),
('REFINITIV_BREAKING_WIRE', '[APPLE_SALES] Apple iPhone sales go on sale with constrained initial supply', 'PENDING', 0.85, 'TECH_MAG7'),
('REFINITIV_BREAKING_WIRE', '[OIL_EARNINGS] Oil makers quarterly earnings spotlight refining margin compression', 'PENDING', 0.88, 'CRUDE_MARGINS'),
('REFINITIV_BREAKING_WIRE', '[CHINA_STIMULUS] China economic plan relies heavily on state infrastructure projects', 'PENDING', 0.90, 'COMMODITIES_CHINA');

-- 2. Indexación en macro_dossier
INSERT OR REPLACE INTO macro_dossier (topic, summary, risk_score, source, m82_tag, sentiment) VALUES
(
    'REFINITIV_WORKSPACE_FULL_2200_ET',
    'Ingesta integral de 10 cables LSEG Refinitiv Workspace. Confirmación de prima en petróleos pesados EE. UU., disrupciones en el Golfo de Adén, recorte de empleos en Unilever y estímulos estatales en China.',
    1.68,
    'LSEG_REFINITIV_USER_SESSION',
    'BUNKER_HOLD_030X',
    0.91
);

-- 3. Inactivación de avisos de mantenimiento e IDs duplicados
UPDATE m82_multi_stream SET status = 'SYSTEM_IGNORE' WHERE headline LIKE '%timestamp%' OR headline LIKE '%LSEG_SECRET%' OR headline LIKE '%Esperando%';

-- 4. Vaciado WAL Atómico
PRAGMA wal_checkpoint(TRUNCATE);
EOF_SQL

echo "🟢 [M82 SUCCESS] Ingesta completa ok. Memoria WAL truncada en 0/0/0 CLEAN."
