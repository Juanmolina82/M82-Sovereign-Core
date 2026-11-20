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
    'LSEG_MOBILE_RIC_BTC',
    'CRYPTO_LIQUIDITY_RISK',
    '[BTC_1Y_STRUCTURE_V60] RIC BTC= 1Y chart confirms Nov-18 anchor at $61,502.60 (down from ~$88k Oct peak & ~$98k Jan high); Nov-20 break to $59,610 tests July 2026 annual low (~$58k-$59.5k) above $56,000 floor | BUNKER 0.30x LOCK',
    1.74,
    'BUNKER_HOLD_030X',
    -0.80,
    '{"ric":"BTC=","nov18_close":61502.60,"nov20_spot":59610.0,"jan_high_band":98000,"oct_peak":88000,"july_low_band":[58000,59500],"structural_floor":56000,"governance":"BUNKER_030X_NO_TRADE"}',
    0.93
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'CRYPTO_PARITY_DESK',
    '[LSEG RIC BTC= 1Y] $61,502.60 (Nov 18) -> $59,610 (Nov 20) testing July annual low ~$58k-$59.5k | Floor $56k | Custodia Pasiva 0.30x LOCK',
    'VERIFIED',
    0.93,
    'CRYPTO_BTC_USD',
    'BTC_JULY_LOW_TEST_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, m82_tag, risk_score, alpha_score, substr(headline, 1, 74) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL
