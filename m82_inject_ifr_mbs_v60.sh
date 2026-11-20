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
    'LSEG_IFR_CREDIT_RATES',
    'MACRO_RATES_MBS_TECH',
    '[IFR_MBS_V60] UMBS30 widens 2-3+ ticks vs 10Y (4.944%, low 4.938%) on swaption vol spike (1m10y +6bp); Nasdaq -2.3%, NVDA $138.18 (-5%), ANT +$3 IPO, VIX 29.92, IG CDX 63.5bp, Dec FOMC no-hike odds 5% | BUNKER 0.30x LOCK',
    1.78,
    'BUNKER_HOLD_030X',
    -0.82,
    '{"ust_10y_yield":4.944,"ust_10y_low":4.938,"ust_5y_yield":4.733,"curve_2s10s_bp":29.7,"curve_10s30s_bp":39.0,"swaption_1m10y_chg_bp":6.0,"fomc_dec_no_hike_prob":0.05,"nasdaq_pct":-2.3,"sp500_pct":-1.0,"dow_pct":0.2,"nvda_price":138.18,"ant_above_ipo":3.0,"vix":29.92,"ig_cdx_bp":63.5,"dxy":103.66,"wti_pct":-1.3,"brent_pct":-1.6,"urn":"urn:newsml:newswire.refinitiv.com:20261120:nIfp9vjLKS:3","governance":"BUNKER_030X_NO_TRADE"}',
    0.95
);

INSERT INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'MACRO_CREDIT_RATES_DESK',
    '[IFR CROSS-ASSET] UMBS30 wider, 1m10y vol +6bp, UST10Y 4.944%, NVDA $138.18 (-5%), ANT +$3 IPO, VIX 29.92 | Custodia Pasiva 0.30x LOCK',
    'VERIFIED',
    0.95,
    'RATES_MBS_TECH_VOL',
    'IFR_MBS_TECH_SELLOFF_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, category, m82_tag, risk_score, alpha_score, substr(headline, 1, 74) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL
