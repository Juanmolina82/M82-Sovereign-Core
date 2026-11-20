#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;
PRAGMA synchronous=NORMAL;

INSERT OR IGNORE INTO macro_dossier (
    source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score
) VALUES (
    'LSEG_REUTERS_LIVE_1446',
    'EQUITY_AI_CAPITULATION_FED',
    '[LSEG_1446_SHOCK] VIX surges +12.38% to 31.96 | SOX -8.69% (7M low), NVDA -7%, ANT.O -12.32% ($85.20), NBIS -18.14%, INTU -8.7% | SPX 7,013.92 (-2.26%), IXIC 22,995.95 (-3.70%), DJI 48,753.78 (-0.70% testing Fib 48,757) | Fed Cook hawkish -> 98.2% Dec hike odds | BUNKER 0.30x LOCK',
    1.85,
    'BUNKER_HOLD_030X',
    -0.88,
    '{"ts":"2026-11-20T14:46:00","vix":31.96,"spx":7013.92,"ixic":22995.95,"dji":48753.78,"sox":8601.48,"ant_o":85.197,"nbis":78.45,"fed_dec_hike_prob":98.2,"governance":"BUNKER_030X_NO_TRADE"}',
    0.99
);

INSERT OR IGNORE INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'LSEG_REUTERS_WIRE_JMMP',
    '[LSEG 14:46 CAPITULATION] VIX 31.96 (+12.38%) | SOX -8.69% | ANT.O -12.32% | NBIS -18.14% | DJI 48,753.78 (Fib Test) | Fed Cook -> 98.2% Dec Hike Odds | BUNKER 0.30x LOCK',
    'VERIFIED',
    0.99,
    'EQUITY_VOLATILITY_FED_SHOCK',
    'AI_CORRECTION_VIX_32_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
EOF_SQL

# Renderizar tarjeta HUD inmediata en /storage/emulated/0/M82card y escanear Galería
python3 - << 'EOF_PY'
import os, sys
sys.path.insert(0, os.path.expanduser("~/M82"))
if os.path.exists(os.path.expanduser("~/M82/m82_hud_gallery_daemon.py")):
    import m82_hud_gallery_daemon as hud
    hud.process_queue(initial_backfill=False)
EOF_PY
