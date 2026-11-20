#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;
PRAGMA synchronous=NORMAL;

INSERT OR IGNORE INTO macro_dossier (
    source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score
) VALUES (
    'POLYGON_QUANT_AUDIT',
    'MACRO_EQUITIES_SEASONALITY',
    '[SPY_QQQ_FRIDAY_LOW_V60] SPY last Friday dip >=5% bottomed 2026-06-26 (-5.8%, 716.58 -> ATH 5.5w; prior Nov-21-2025 -5.6% -> ATH 4.5w); QQQ last Friday bottom 2024-04-19 (-8.1%, 26d) | BUNKER 0.30x LOCK',
    1.45,
    'BUNKER_HOLD_030X',
    0.15,
    '{"spy_last_friday_bottom":"2026-06-26","spy_dip_pct":-5.8,"spy_recovery_weeks":5.5,"spy_nov_analog":"2025-11-21","qqq_last_friday_bottom":"2024-04-19","qqq_dip_pct":-8.1,"qqq_recovery_days":26,"governance":"BUNKER_030X_NO_TRADE"}',
    0.86
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'MACRO_EQUITIES_DESK',
    '[SPY/QQQ SEASONALITY] Nov 20 Friday Window Audit: SPY Nov-21-2025 analog (-5.6% -> 4.5w ATH) vs QQQ beta lag | Custodia Pasiva 0.30x LOCK',
    'VERIFIED',
    0.86,
    'EQUITIES_SPY_QQQ',
    'FRIDAY_LOW_AUDIT_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, m82_tag, substr(headline, 1, 74) AS snippet FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL
