#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR_LOCAL="$HOME/M82_Backups/platform_snapshots"
BACKUP_DIR_SDCARD="/sdcard/Documents/M82_Platform_Backups"
ARCHIVE_NAME="M82_PLATFORM_FULL_SNAPSHOT_${TIMESTAMP}.tar.gz"

echo "=========================================================="
echo "🛡️ INICIANDO RESPALDO Y BLINDAJE INTEGRAL DE PLATAFORMA M82"
echo "=========================================================="

# 1. Crear directorios de destino
mkdir -p "$BACKUP_DIR_LOCAL"
mkdir -p "$BACKUP_DIR_SDCARD" 2>/dev/null || true

# 2. Forzar Checkpoint en SQLite3 para consolidar WAL en el archivo .db principal
echo "[M82 BACKUP] Consolidando base de datos SQLite3 WAL..."
sqlite3 $HOME/M82/m82_database.db "PRAGMA wal_checkpoint(FULL);"

# 3. Crear archivo comprimido tar.gz excluyendo logs pesados pero incluyendo todo el núcleo
echo "[M82 BACKUP] Empaquetando arquitectura M82, fuentes, vault y base de datos..."
tar -czf "$BACKUP_DIR_LOCAL/$ARCHIVE_NAME" \
    --exclude="*.log" \
    --exclude="dossier.log" \
    --exclude="orch.log" \
    -C $HOME \
    M82 \
    .termux/boot/m82-boot.sh

# 4. Copia redundante en la memoria física del dispositivo (/sdcard/)
if [ -d "$BACKUP_DIR_SDCARD" ]; then
    cp "$BACKUP_DIR_LOCAL/$ARCHIVE_NAME" "$BACKUP_DIR_SDCARD/"
    echo "[M82 BACKUP] 🟢 Copia redundante guardada en la SDCard: $BACKUP_DIR_SDCARD/$ARCHIVE_NAME"
fi

# 5. Generar Checksum SHA-256 para validación de integridad criptográfica
SHA256_HASH=$(sha256sum "$BACKUP_DIR_LOCAL/$ARCHIVE_NAME" | awk '{print $1}')
echo "$SHA256_HASH  $ARCHIVE_NAME" > "$BACKUP_DIR_LOCAL/${ARCHIVE_NAME}.sha256"

# 6. Exportar respaldo del Crontab actual
crontab -l > "$BACKUP_DIR_LOCAL/crontab_backup_${TIMESTAMP}.bak" 2>/dev/null || true

# 7. Asentar registro de congelación en la base de datos
sqlite3 $HOME/M82/m82_database.db << EOF_DB
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
  'SYSTEM_GOVERNANCE',
  '[FULL PLATFORM SEALED] Snapshot SHA256: ${SHA256_HASH:0:16}... | All Desks, Vault & HUD Backed Up',
  'COMPLETED',
  1.00,
  'SYSTEM_WIDE'
);
EOF_DB

echo "=========================================================="
echo "✅ RESPALDO COMPLETO REALIZADO CON ÉXITO"
echo "📦 Archivo Local  : $BACKUP_DIR_LOCAL/$ARCHIVE_NAME"
echo "🔑 Firma SHA-256  : $SHA256_HASH"
echo "=========================================================="
