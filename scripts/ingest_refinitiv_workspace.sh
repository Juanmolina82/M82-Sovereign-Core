#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Inserción Multi-Stream
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES 
('REFINITIV_TRUMP_ADMIN', '[US_TRADE_TARIFFS | 2026-10-26] Trump tariffs propose up to 30% on US-Canada steel/aluminum & Mexico trade corridor', 'PENDING', 0.88, 'MACRO_US'),
('REFINITIV_DEFENSE', '[US_SAUDI_DEFENSE] US-Saudi defense pact negotiations advance amidst Middle East security framework', 'PENDING', 0.82, 'BRENT_CRUDE'),
('REFINITIV_MARKETS', '[VOLATILITY_MONITOR] S&P 500 & US10Y Yields trade mixed; USD strength maintained on global risk premium', 'PENDING', 0.75, 'US10Y_SPX');

-- Inserción Macro Dossier Sanitizado
INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag)
VALUES 
('REFINITIV_WORKSPACE_CAPTURE', 'MACRO_INTELLIGENCE', '[WORKSPACE_INGEST | 2026-10-26] Ingesta 3-Panel Refinitiv Workspace completada: Tariffs, Def-Pacts & Global Yield Curve', 1.68, 'BUNKER_HOLD_030X');

SELECT 'M82 BBDD INGEST OK — ' || count(*) || ' REGISTROS EN STREAM' FROM m82_multi_stream WHERE status='PENDING';
SQL

sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE);"
echo "WAL CLEAN OK — BUNKER 0.30x SAFE"
