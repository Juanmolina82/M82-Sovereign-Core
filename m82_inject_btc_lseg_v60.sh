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
    'LSEG_REUTERS_URGENT',
    'CRYPTO_LIQUIDITY_RISK',
    '[BTC_BREAKDOWN_V60] Bitcoin falls below $60,000 ($59,610, -3.08%) for first time since July on AI valuation contagion & risk-off | BUNKER 0.30x LOCK',
    1.72,
    'BUNKER_HOLD_030X',
    -0.78,
    '{"asset":"BTC","price":59610.0,"pct_chg":-3.08,"threshold_broken":60000,"urn":"urn:newsml:newswire.refinitiv.com:20261120:nL2N4710M8","driver":"AI_VALUATION_RISK_OFF","governance":"BUNKER_030X_NO_TRADE"}',
    0.92
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'CRYPTO_PARITY_DESK',
    '[URGENT LSEG] BTC breaks $60,000 -> $59,610 (-3.08%) | AI valuation risk-off contagion | Custodia Pasiva 0.30x LOCK',
    'VERIFIED',
    0.92,
    'CRYPTO_BTC_USD',
    'BTC_SUB_60K_BREAKDOWN_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, category, m82_tag, risk_score, alpha_score, substr(headline, 1, 74) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL
