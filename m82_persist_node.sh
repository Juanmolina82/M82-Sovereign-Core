#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/sdcard/M82_Backups"
ROOT_BACKUP="/sdcard/M82_EMERGENCY_RESTORE"

mkdir -p "$BACKUP_DIR"
mkdir -p "$ROOT_BACKUP"

echo "📦 Empaquetando Nodo Caracas (M82) Soberano..."
tar --exclude='*.log' --exclude='__pycache__' -czf "$BACKUP_DIR/M82_MASTER_$TIMESTAMP.tar.gz" -C ~ M82

echo "💾 Guardando copia de restauración rápida..."
cp "$BACKUP_DIR/M82_MASTER_$TIMESTAMP.tar.gz" "$ROOT_BACKUP/M82_latest.tar.gz"

echo "✅ PERSISTENCIA COMPLETADA CON ÉXITO."
