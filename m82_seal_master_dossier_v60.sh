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
    'M82_SOVEREIGN_MASTER_DOSSIER',
    'MACRO_GEOPOLITICS_VENEZUELA_V60',
    '[MASTER_DOSSIER_20261120] VIX 30.86 | Tech Rotation (Staples +1.57% vs InfoTech -1.35%) | Dow Fib 48,757 | AAII -8.9% | UMich 51.5 (1Y Infl 3.7%) | Trump-Iran Impasse Elevates PADD3 Heavy Crude Value -> Freeze CITGO Auction Pre-Dec 18, 15-25Y IMF Debt Swap & 2027 Election Roadmap (@MariaCorinaYA) | BUNKER 0.30x LOCK',
    1.68,
    'BUNKER_HOLD_030X',
    -0.30,
    '{"date":"2026-11-20","node":"Charallave_L4_L5_Edge","vix":30.86,"ust10y":4.944,"brent":90.70,"wti":82.27,"xau":3575.52,"btc":59418.08,"aaii_spread":-8.90,"umich":51.5,"citgo_deadline":"2026-12-18","governance":"BUNKER_030X_NO_TRADE"}',
    0.98
);

INSERT OR IGNORE INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'M82_MASTER_ORCHESTRATOR',
    '[MASTER MACRO DOSSIER V60] VIX 30.86 | Sector Rotation | Trump-Iran Impasse -> CITGO Dec-18 Freeze, 15-25Y IMF Debt Swap & 2027 Electoral Mandate | BUNKER 0.30x LOCK',
    'VERIFIED',
    0.98,
    'SOVEREIGN_MACRO_CITGO_V60',
    'MASTER_DOSSIER_SEAL_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
EOF_SQL

# Generar tarjeta HUD inmediata y refrescar Galería Android
python3 - << 'EOF_PY'
import os, sqlite3
if os.path.exists(os.path.expanduser("~/M82/m82_hud_gallery_daemon.py")):
    import sys
    sys.path.insert(0, os.path.expanduser("~/M82"))
    import m82_hud_gallery_daemon as hud
    hud.process_queue(initial_backfill=False)
EOF_PY
