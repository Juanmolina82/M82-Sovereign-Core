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
    'LSEG_IFR_MOBILE_1237',
    'CROSS_ASSET_VOL_STRESS',
    '[LSEG_1237_SNAPSHOT_V60] VIX spikes +8.51% to 30.86; BTC= drops -3.39% to $59,418.08; IXIC -2.92% (23,181.82); SPX -1.67% (7,055.85); DJI -0.28% (48,960.68) | BUNKER 0.30x LOCK',
    1.85,
    'BUNKER_HOLD_030X',
    -0.88,
    '{"ts_feed":"12:37","btc_spot":59418.08,"btc_pct":-3.39,"vix":30.86,"vix_pct":8.51,"dji":48960.68,"dji_pct":-0.28,"ixic":23181.817,"ixic_pct":-2.92,"spx":7055.85,"spx_pct":-1.67,"governance":"BUNKER_030X_NO_TRADE"}',
    0.96
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'MACRO_VOL_DESK',
    '[LSEG 12:37] VIX 30.86 (+8.51%) | BTC= $59,418.08 (-3.39%) | IXIC -2.92% | SPX -1.67% | DJI -0.28% | Custodia Pasiva 0.30x LOCK',
    'VERIFIED',
    0.96,
    'CROSS_ASSET_TAIL_RISK',
    'VIX_ABOVE_30_INTRADAY_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, m82_tag, risk_score, alpha_score, substr(headline, 1, 74) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL
