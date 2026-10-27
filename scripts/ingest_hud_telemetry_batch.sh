#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Inserción en m82_multi_stream (Tabla Multicanal)
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES 
('IMF_GULF', '[IMF_GULF | 2026-10-19 13:20:48] IMF cuts Gulf -3.3% to -16% heavy premium validation', 'PENDING', 0.85, 'MEREY'),
('COREWEAVE_AI', '[COREWEAVE_AI | 2026-10-19 13:20:09] CoreWeave 240MW Mumbai AdaniConneX CAPEX AI infra', 'PENDING', 0.95, 'AI_INFRA'),
('CITGO_OFAC_DESK', '[CITGO_OFAC_DESK | 2026-10-19 13:19:35] OFAC GL 5Z Citgo auction Delaware docket update', 'PENDING', 0.80, 'PDVSA26'),
('HARDWARE_ABSTRACTION', '[HARDWARE_ABSTRACTION | 2026-10-19 13:19:32] Hardware abstraction layer verified: agnostic VLA routing ready', 'PENDING', 0.90, 'ROBOTICS'),
('ORINOCO_CRUDE', '[ORINOCO_CRUDE | 2026-10-19 13:18:49] Jose Terminal Faja heavy loading schedule', 'PENDING', 0.85, 'MEREY'),
('LSEG_REFINITIV', '[IMF_GROWTH_CUT] IMF cuts Growth FX forecast for first time since May on Middle East supply fears', 'PENDING', 0.88, 'MACRO'),
('LSEG_REFINITIV', '[GOLD_REAL_YIELDS] Gold edges lower as firm dollar, elevated yields weigh', 'PENDING', -0.50, 'XAUUSD'),
('LSEG_REFINITIV', '[LATAM_MEXICO_PE] LatAm PE edge higher with focus on Mexico polls', 'PENDING', 0.82, 'LATAM_PE');

-- Inserción en macro_dossier (Tabla Dossier Sanitizada)
INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag)
VALUES 
('SOVEREIGN_EXECUTION_CORE', 'TELEMETRY_BATCH', '[HUD_CARD_BATCH | 2026-10-19] 8 HUD Cards verified — OFAC GL 5Z, IMF Gulf Premium & CoreWeave 240MW ingested', 1.68, 'BUNKER_HOLD_030X');

SELECT 'M82 BBDD INGEST OK — ' || count(*) || ' STREAM RECORDS PENDING' FROM m82_multi_stream WHERE status='PENDING';
SQL

sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE); SELECT 'WAL CLEAN OK — BUNKER SAFE';"
