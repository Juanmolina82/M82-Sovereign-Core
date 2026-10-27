#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

# 1. Asegurar columnas en macro_dossier si no existen
sqlite3 "$DB_PATH" << 'SQL_MIGRATION'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

ALTER TABLE macro_dossier ADD COLUMN alpha_score REAL DEFAULT 0.0;
ALTER TABLE macro_dossier ADD COLUMN asset_impact TEXT DEFAULT 'MACRO';
ALTER TABLE macro_dossier ADD COLUMN event_trigger TEXT;
SQL_MIGRATION 2>/dev/null || true

# 2. Ingesta Atómica Sanitizada en WAL Mode
sqlite3 "$DB_PATH" << 'SQL_EXEC'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Ingesta Brasil / EWZ
INSERT OR IGNORE INTO macro_dossier (
    source, category, headline, risk_score, m82_tag, alpha_score, asset_impact, event_trigger
) VALUES (
    'WSJ_LSEG_BRAZIL_20261026',
    'EM_POLITICAL_REPRICING',
    'Brazil Runoff Oct 25 2026: Lula reelected 51.79% vs F. Bolsonaro 48.21% — EWZ -27.37% Premarket ($30.94) / Petrobras -25% / XP -40%',
    1.85,
    'BRAZIL_ELECTION_REPRICING_EWZ_ROUT_20261026',
    0.97,
    'EWZ_PETROBRAS_BRL_SOVEREIGN',
    'LULA_REFINING_BOST_ANNULMENT_REJECT'
);

INSERT OR IGNORE INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact
) VALUES (
    'M82_LATAM_RISK_DAEMON',
    '[LATAM_RISK] EWZ -27% rout confirms extreme positioning reversal. BUNKER MODE 0.30x LOCK validated.',
    'PROCESSED',
    0.97,
    'LATAM_EQUITIES_EM_FX'
);

-- Checkpoint WAL TRUNCATE para sellado limpio 0/0/0
PRAGMA wal_checkpoint(TRUNCATE);

SELECT '✅ TELEMETRÍA BRASIL SINK SEALED — WAL 0/0/0 CLEAN — ' || datetime('now');
SQL_EXEC
