#!/usr/bin/env bash
BACKUP_DIR=~/M82_Backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE="$BACKUP_DIR/M82_Master_Dossier_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "📦 Empaquetando la Suite M82 de 40 Daemons + Base de Datos WAL..."
tar -czvf "$ARCHIVE" -C ~ M82/

echo "✅ Backup completado con éxito:"
ls -lh "$ARCHIVE"
