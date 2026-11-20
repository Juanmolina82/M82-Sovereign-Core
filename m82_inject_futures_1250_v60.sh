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
    'US_FUTURES_FEED_1250',
    'EQUITIES_INDEX_SELLOFF',
    '[FUTURES_1250_V60] US Stock Futures extend intraday selloff: NASDAQ=F 25,583.70 (-3.52%), SP500=F 7,041.70 (-1.87%), RUSSELL2000=F 2,617.00 (-1.43%), DOWJONES=F 48,877.60 (-0.45%) | BUNKER 0.30x LOCK',
    1.89,
    'BUNKER_HOLD_030X',
    -0.90,
    '{"ts_feed":"12:50_PM","dow_f":48877.60,"dow_pct":-0.45,"sp500_f":7041.70,"sp500_pct":-1.87,"nasdaq_f":25583.70,"nasdaq_pct":-3.52,"russell_f":2617.00,"russell_pct":-1.43,"governance":"BUNKER_030X_NO_TRADE"}',
    0.97
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'MACRO_EQUITIES_DESK',
    '[FUTURES 12:50 PM] NASDAQ=F -3.52% (25,583.70) | SP500=F -1.87% (7,041.70) | RTY -1.43% | YM -0.45% | Custodia Pasiva 0.30x LOCK',
    'VERIFIED',
    0.97,
    'US_EQUITY_FUTURES',
    'NASDAQ_F_MINUS_352_SELLOFF_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, m82_tag, risk_score, alpha_score, substr(headline, 1, 74) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL
