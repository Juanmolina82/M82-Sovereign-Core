#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Inserción con el esquema canónico de macro_dossier
INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag)
VALUES (
    'M82_SOVEREIGN_CORE',
    'MONADA_59_MACRO',
    '[MONADA 59 | LUNA CAZADOR 5849] 26/10/2026=1 Triple Mónada 111 — 44x59=2596 Pitágoras 570 A.C — Siglo 59 Año 5849 Padre 8 Final — Base 444',
    1.68,
    'BUNKER_HOLD_030X'
);

-- Reflejo en m82_multi_stream para PWA / Telemetría
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'MONADA_59_INDEXER',
    '[MONADA 59] Artefacto 2026-10-26-MONADA-59-LUNA-CAZADOR-5849-5849.md ingresado y sincronizado.',
    'PROCESSED',
    0.95,
    'MACRO_CORE'
);

SELECT 'MACRO DOSSIER INGEST OK — Registros: ' || COUNT(*) FROM macro_dossier;
SQL

sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE);"
echo "WAL CLEAN 0/0/0 — BUNKER SAFE"
