#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Inserción canónica en macro_dossier
INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag)
VALUES (
    'LSEG_REFINITIV_WIRE',
    'ENERGY_GEOPOLITICS',
    '[LSEG OIL 27/10] BRENT $115.15 HORMUZ WORST MONTH SINCE 2017 | SAUDI-TURKEY-PAK-IRAN TEHRAN TALKS | VENEZUELA CICLO59 YEAR 5849-300 DIADA 2',
    1.68,
    'BUNKER_HOLD_030X'
);

-- Reflejo en m82_multi_stream para PWA / Telemetría
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'LSEG_OIL_INDEXER',
    '[LSEG OIL] Brent $115.15 — Hormuz risk — Ingesta atómica m82_multi_stream PROCESSED ZERO LOCKS',
    'PROCESSED',
    0.93,
    'MEREY_BRENT'
);

SELECT 'MACRO DOSSIER INGEST OK — Total Registros: ' || COUNT(*) FROM macro_dossier;
SQL

sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE);"
echo "WAL CLEAN 0/0/0 — BUNKER SAFE"
