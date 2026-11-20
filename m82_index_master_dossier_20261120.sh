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
    'M82_SOVEREIGN_CORE_V60',
    'EXECUTIVE_MACRO_SYNTHESIS',
    '[M82_MASTER_DOSSIER_20261120] Cross-Asset Tail-Risk Synthesis: VIX 30.86 (+8.51%), IXIC 23,181.82 (-2.92%), SPX 7,055.85 (-1.67%), NVDA $138.18 (-5%), BTC= $59,418.08 (-3.39%), UST10Y 4.944% (UMBS30 wider, 1m10y +6bp), Gold GC1! $3,680.4 floor test, Silver SIc1 $52.240 Bear Flag -> $37.84-$39.60 | BUNKER MODE 0.30x LOCK (0.22x active, VaR 1.68%, Warsh +102bps)',
    1.88,
    'BUNKER_HOLD_030X',
    -0.85,
    '{"date":"2026-11-20","locus":"Charallave_L4L5_Caracas_HQ","vix":30.86,"ixic":23181.82,"spx":7055.85,"dji":48960.68,"nvda":138.18,"btc":59418.08,"ust10y":4.944,"gold_gc1":3680.4,"silver_sic1":52.240,"exposure":0.22,"lock_cap":0.30,"var_daily":0.0168,"warsh_spread_bp":102.0,"policy":"LOCKOUT_NO_TRADE"}',
    0.98
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'M82_UNIFIED_CORE_V60',
    '[MASTER DOSSIER SEALED] VIX 30.86 | IXIC -2.92% | BTC $59,418 | UST10Y 4.944% | GC1! $3,680.4 | SIc1 $52.240 | BUNKER 0.30x LOCK & Dry Powder 100% Shielded',
    'VERIFIED',
    0.98,
    'SOVEREIGN_MACRO_ARCHITECTURE',
    'MASTER_DOSSIER_CONSOLIDATION_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, m82_tag, risk_score, alpha_score, substr(headline, 1, 74) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 1;
EOF_SQL
