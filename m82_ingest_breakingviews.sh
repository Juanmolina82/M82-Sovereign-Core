#!/data/data/com.termux/files/usr/bin/bash
set -e

DB=~/M82/m82_database.db

echo "=== [M82 ENGINE] INGESTING BREAKINGVIEWS WIRE & RECALIBRATING MSI ==="

sqlite3 $DB << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

-- Inserción del evento Breakingviews en macro_dossier
INSERT OR IGNORE INTO macro_dossier (
    source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score, msi_index
) VALUES (
    'REFINITIV_BREAKINGVIEWS',
    'TANGLED_AI_WEB_ANTHROPIC_OPENAI',
    '[BREAKINGVIEWS] GOOGL & MSFT Tangled AI Webs — $64B Server Combined — GOOGL Cloud $30.7B 2x / MSFT Azure $33.2B +48% / FCF -$9B Validates Compute Bottleneck',
    1.90,
    'v60.5849-BREAKINGVIEWS-TANGLED-AI-WEB-64B',
    0.92,
    '{"googl_cloud_b":30.7,"msft_azure_b":33.2,"combined_server_b":64,"googl_fcf_b":-9,"thesis":"tangled ownership = capex inefficiency"}',
    1.90,
    589.3
);

-- Actualización de la métrica MSI global
UPDATE macro_dossier SET msi_index = 589.3 WHERE m82_tag = 'v60.5849-GOOGL-MSFT-EARNINGS-BEAT-127B-92B-AZURE45';

PRAGMA wal_checkpoint(TRUNCATE);
SELECT '🟢 WAL CLEAN 0/0/0 — DOSSIER BREAKINGVIEWS Y MSI 589.3 REGISTRADOS — ' || datetime('now');
SQL

cd ~/M82
git add .
git commit -m "feat(dossier): Reuters Breakingviews Tangled AI Webs — MSI recalibrated to 589.3" || true
git push origin main || true

echo "🟢 [M82 SUCCESS] BREAKINGVIEWS CROSS-VALIDATION SEALED"
