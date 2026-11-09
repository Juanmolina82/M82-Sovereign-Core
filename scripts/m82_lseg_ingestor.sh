#!/usr/bin/env bash
# ==============================================================================
# M82 LSEG INGESTOR — INYECCIÓN DIRECTA DE SEÑALES A WAL (BASH NATIVE)
# Node: Caracas HQ Node
# ==============================================================================

DB_PATH="$HOME/M82/m82_database.db"

SOURCE="${1:-LSEG_WORKSPACE_BREAKING}"
CATEGORY="${2:-GEOPOLITICS_TAIL_RISK}"
HEADLINE="${3:-Default Test Event}"
RISK_SCORE="${4:-9.8}"
TAG="${5:-BUNKER_LOCK}"

sqlite3 -cmd "PRAGMA busy_timeout=60000;" "$DB_PATH" <<SQL
BEGIN IMMEDIATE;
INSERT INTO macro_dossier (
    timestamp, source, category, headline, risk_score, m82_tag, sentiment, entities
) VALUES (
    datetime('now'),
    '$SOURCE',
    '$CATEGORY',
    '$HEADLINE',
    $RISK_SCORE,
    '$TAG',
    -0.95,
    'RIYADH_RUH,US_CASUALTY,BRENT_PREMIUM'
);
COMMIT;
SQL

echo "✅ Evento inyectado en macro_dossier vía Bash SQLite nativo."
