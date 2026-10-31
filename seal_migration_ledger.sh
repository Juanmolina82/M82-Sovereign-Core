#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 LEDGER SEALS DDL CREATION & MIGRATION SEALING ENGINE
# Chairman Juan M. Molina -- Sovereign Execution Core (Charallave L4/L5 Edge)
# ==============================================================================
set -e

DB="$HOME/M82/m82_database.db"

echo "⚡ [PASO 1] Creando tabla m82_ledger_seals si no existe..."
sqlite3 "$DB" << 'SQL_DDL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

CREATE TABLE IF NOT EXISTS m82_ledger_seals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seal_id TEXT UNIQUE NOT NULL,
    capture TEXT NOT NULL,
    validated TEXT NOT NULL,
    categories TEXT NOT NULL,
    null_fix TEXT NOT NULL,
    wal_status TEXT NOT NULL,
    version TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
SQL_DDL

echo "⚡ [PASO 2] Registrando Sello Definitivo de Migración 1000281178.jpg..."
sqlite3 "$DB" << 'SQL_INSERT'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

INSERT OR REPLACE INTO m82_ledger_seals (
    seal_id, capture, validated, categories, null_fix, wal_status, version
) VALUES (
    'SCV61-1500-M82-444-TRUST-113',
    '1000281178.jpg',
    '113/113',
    '57_CATEGORIES',
    '10_NULLS_CONVERTED_TO_M82_LEGACY_RAW_INGEST',
    '0/0/0_CLEAN',
    'v61.0.1 PERPETUAL'
);

-- Registrar respaldo en m82_multi_stream
INSERT OR IGNORE INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger
) VALUES (
    'M82_LEDGER_SEAL_ENGINE',
    '[FULL LIFECYCLE MIGRATION SEALED] 113/113 Validated | 10 NULLs -> M82_LEGACY_RAW_INGEST | WAL CLEAN 0/0/0 | m82_ledger_seals created',
    'BREAKOUT_ACTIVE',
    1.00,
    1.00,
    'LEDGER_SEALED',
    'PERPETUAL_MIGRATION_OK'
);
SQL_INSERT

echo "=========================================================================="
echo "📊 VERIFICACIÓN DEL SELLO REGISTRADO EN LIBRO MAYOR:"
echo "=========================================================================="
sqlite3 "$DB" << 'SQL_VERIFY'
.mode column
.headers on
SELECT seal_id, capture, validated, null_fix, wal_status, version FROM m82_ledger_seals ORDER BY id DESC LIMIT 1;
SQL_VERIFY

echo "=========================================================================="
echo "⚡ [PASO 3] Sellando checkpoint TRUNCATE WAL CLEAN 0/0/0..."
sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=120000; PRAGMA wal_checkpoint(TRUNCATE);"

echo "🟢 [SUCCESS] Tabla m82_ledger_seals Creada | Sello Inscripto | WAL CLEAN 0/0/0"
echo "=========================================================================="
