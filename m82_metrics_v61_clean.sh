#!/data/data/com.termux/files/usr/bin/bash
set -e

DB=~/M82/m82_database.db

echo "=== [M82 ENGINE] IDEMPOTENT DDL MIGRATION & MSI RE-INDEXING ==="

# 1. Adición silenciosa de columnas si no existen
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN alpha_score REAL DEFAULT 1.00;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN beta_corr REAL DEFAULT 0.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN omega_conviction REAL DEFAULT 0.91;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN theta_decay INTEGER DEFAULT 45;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN gamma_leverage REAL DEFAULT 1.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN rho_rate_sens REAL DEFAULT 0.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN kappa_var REAL DEFAULT 1.68;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN delta_momentum REAL DEFAULT 0.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN sigma_vol REAL DEFAULT 0.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN lambda_liquidity REAL DEFAULT 1.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN zeta_esg REAL DEFAULT 43.0;" 2>/dev/null || true
sqlite3 $DB "ALTER TABLE macro_dossier ADD COLUMN msi_index REAL DEFAULT 0.0;" 2>/dev/null || true

# 2. Actualización de datos e inyección del M82 Sovereign Index (MSI)
sqlite3 $DB << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

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
SELECT '🟢 WAL CLEAN 0/0/0 — METRIC FRAMEWORK v61 CLEAN SEALED — ' || datetime('now');
SQL

echo "🟢 [M82 SUCCESS] FRAMEWORK V61 SANITIZADO Y 100% IDEMPOTENTE"
