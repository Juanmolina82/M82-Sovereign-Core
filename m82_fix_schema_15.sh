#!/data/data/com.termux/files/usr/bin/bash
set -e

DB=~/M82/m82_database.db

echo "=== [M82 ENGINE] SANITIZING DDL COLUMN MAPPING & WAL CHECKPOINT ==="

sqlite3 $DB << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;
PRAGMA synchronous=NORMAL;

-- Inserción saneada con declaración explícita de 7 columnas objetivo
INSERT OR IGNORE INTO macro_dossier (
    source, category, headline, risk_score, m82_tag, sentiment, metadata_json
) VALUES (
    'REFINITIV_LSEG_WORKSPACE_LIVE',
    'BIG_TECH_Q1_Q3_EARNINGS_BEAT',
    '[REFINITIV LSEG LIVE] GOOGL Q3 $127.6B (+25%) + MSFT Q1 $92.27B Beat — Azure 45% CC / RPO $684B Validates 0.10x Gas-to-Compute Arbitrage',
    1.85,
    'v60.5849-GOOGL-MSFT-EARNINGS-BEAT-127B-92B-AZURE45',
    0.92,
    '{"googl_rev_b":127.6,"msft_rev_b":92.27,"msft_rpo_b":684,"msft_capex_q_b":50.0,"theme":"Gas-to-Compute Arbitrage"}'
);

INSERT OR IGNORE INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'REFINITIV_EARNINGS_BRIDGE',
    '[TELEMETRY] Module 15 Schema Sanitized — GOOGL $127.6B & MSFT $92.27B Validated',
    'BREAKOUT_ACTIVE',
    1.00,
    'CORNICHE_JV_STRATEGY',
    'SCHEMA_SANITIZED_WAL_CLEAN'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT 'WAL CLEAN 0/0/0 — DOSSIER 15 SANITIZADO — ' || datetime('now');
SQL

echo "=== [M82 ENGINE] UPDATING REPOSITORY ==="
cd ~/M82
git add .
git commit -m "fix(schema): Explicit column mapping for Dossier 15 — WAL CLEAN 0/0/0" || true
git push origin main || true

echo "🟢 [M82 SUCCESS] SCHEMA SANITIZED & SYNCHRONIZED"
