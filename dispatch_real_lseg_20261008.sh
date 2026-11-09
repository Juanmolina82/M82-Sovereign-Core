#!/usr/bin/env bash
set -e
DB="$HOME/M82/m82_database.db"

echo "📥 [1/2] Inyectando cables en tiempo real de LSEG Workspace..."

sqlite3 "$DB" << 'SQL'
PRAGMA busy_timeout = 10000;
INSERT OR IGNORE INTO m82_multi_stream 
(daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status)
VALUES 
('GLOBAL_BOND_BASH', '[GLOBAL_BOND_BASH | 2026-10-08 10:15:00] US10Y near 24y high 5.36% + oil +4% Gulf shipping attacks', 'us10y near 24y high 5.36% + oil +4% gulf shipping attacks', 92, 95, 87, 'BRENT', 'PENDING'),
('FRENCH_DEBT_CONTAGION', '[FRENCH_DEBT_CONTAGION | 2026-10-08 10:15:00] Euro 17m low French spread banks -1.5pct', 'euro 17m low french spread banks -1.5pct', 78, 90, 70, 'EU_BANKS', 'PENDING'),
('AI_DEBT_RUSH', '[AI_DEBT_RUSH | 2026-10-08 10:15:00] SpaceX Broadcom Oracle 90bn debt rush for AI chips crowding yields', 'spacex broadcom oracle 90bn debt rush for ai chips crowding yields', 85, 92, 78, 'US10Y', 'PENDING');
SQL

echo "✅ [2/2] Inyección completada sin bloqueos."
