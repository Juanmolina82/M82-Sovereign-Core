#!/usr/bin/env bash
DB_PATH="$HOME/M82/m82_database.db"
BACKUP_DIR="$HOME/M82/backups"
SDCARD_DIR="/sdcard/M82_BUNKER_BACKUP"

mkdir -p "$BACKUP_DIR" "$SDCARD_DIR" 2>/dev/null || true
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TARGET="$BACKUP_DIR/m82_db_$TIMESTAMP.sq3"

# Ejecutar .backup mediante stdin en sqlite3 (Sintaxis correcta)
sqlite3 "$DB_PATH" <<EOF
.timeout 5000
.backup '$TARGET'
EOF

if [ -f "$TARGET" ]; then
    echo "✅ Respaldo rápido completado: m82_db_$TIMESTAMP.sq3"
    cp "$TARGET" "$SDCARD_DIR/" 2>/dev/null && echo "🛡️ Copia replicada a SDCard ($SDCARD_DIR)"
else
    echo "❌ Error en respaldo"
fi
