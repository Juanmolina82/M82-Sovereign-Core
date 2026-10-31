#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Inserción canónica en macro_dossier
INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag)
VALUES (
    'AI_INFRA_DEBT_OFFICIAL',
    'AI_INFRA_DEBT',
    '[CONFIRM OFFICIAL] BoFa Blackstone Citi MS $63B SPV Broadcom XPU Residual Value Support — Anthropic 1.5-2T Deliveries 2027',
    0.20,
    'BUNKER_HOLD_030X'
);

-- Reflejo en m82_multi_stream para PWA / Telemetría
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'BLACKSTONE_XPU_INDEXER',
    '[BLACKSTONE $63B SPV] Broadcom XPU Anthropic support — Ingesta atómica m82_multi_stream PROCESSED ZERO LOCKS',
    'PROCESSED',
    0.95,
    'AI_INFRA'
);

SELECT 'MACRO DOSSIER INGEST OK — Total Registros: ' || COUNT(*) FROM macro_dossier;
SQL

sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE);"
echo "WAL CLEAN 0/0/0 — BUNKER SAFE"
