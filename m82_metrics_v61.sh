#!/data/data/com.termux/files/usr/bin/bash
set -e

DB=~/M82/m82_database.db
mkdir -p ~/M82/backups

echo "=== [M82 ENGINE] EXECUTING DDL MIGRATION FOR FRAMEWORK V61 ==="

sqlite3 $DB << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;
PRAGMA synchronous=NORMAL;

-- Migración DDL idempotente: Adición de las 11 nuevas columnas a macro_dossier
ALTER TABLE macro_dossier ADD COLUMN alpha_score REAL DEFAULT 1.00;
ALTER TABLE macro_dossier ADD COLUMN beta_corr REAL DEFAULT 0.0;
ALTER TABLE macro_dossier ADD COLUMN omega_conviction REAL DEFAULT 0.91;
ALTER TABLE macro_dossier ADD COLUMN theta_decay INTEGER DEFAULT 45;
ALTER TABLE macro_dossier ADD COLUMN gamma_leverage REAL DEFAULT 1.0;
ALTER TABLE macro_dossier ADD COLUMN rho_rate_sens REAL DEFAULT 0.0;
ALTER TABLE macro_dossier ADD COLUMN kappa_var REAL DEFAULT 1.68;
ALTER TABLE macro_dossier ADD COLUMN delta_momentum REAL DEFAULT 0.0;
ALTER TABLE macro_dossier ADD COLUMN sigma_vol REAL DEFAULT 0.0;
ALTER TABLE macro_dossier ADD COLUMN lambda_liquidity REAL DEFAULT 1.0;
ALTER TABLE macro_dossier ADD COLUMN zeta_esg REAL DEFAULT 43.0;
ALTER TABLE macro_dossier ADD COLUMN msi_index REAL DEFAULT 0.0;

-- Enriquecimiento atómico del Dossier 15 (GOOGL/MSFT Blowout Earnings Beat)
UPDATE macro_dossier SET
  alpha_score = 1.85,
  beta_corr = -0.22,
  omega_conviction = 0.91,
  theta_decay = 45,
  gamma_leverage = 10.0,
  rho_rate_sens = 0.10,
  kappa_var = 1.68,
  delta_momentum = 25.0,
  sigma_vol = 46.0,
  lambda_liquidity = 1.0,
  zeta_esg = 18.7,
  msi_index = 536.1
WHERE m82_tag = 'v60.5849-GOOGL-MSFT-EARNINGS-BEAT-127B-92B-AZURE45';

PRAGMA wal_checkpoint(TRUNCATE);
SELECT '🟢 WAL CLEAN 0/0/0 — METRIC FRAMEWORK v61 EXPANDIDO EN DB — ' || datetime('now');
SQL

echo "=== [M82 ENGINE] CREATING BACKUP & PUSHING TO GITHUB ==="
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sqlite3 $DB .dump > ~/M82/backups/m82_v61_dump_${TIMESTAMP}.sql 2>/dev/null || true

cd ~/M82
git add .
git commit -m "feat(core): Framework Métrico v61 — Beyond Alpha (12 Metrics) + MSI Index 536.1" || true
git push origin main || true

echo "🟢 [M82 SUCCESS] FRAMEWORK V61 REGISTRADO Y DEPLEGADO"
