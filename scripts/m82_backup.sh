#!/bin/bash

# Directorio de respaldos en la memoria interna del dispositivo
BACKUP_DIR="/sdcard/M82_Backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_PATH="m82_database.db"

mkdir -p "$BACKUP_DIR"

# 1. Mantenimiento previo de la BD WAL
python3 -c "import sqlite3; conn=sqlite3.connect('$DB_PATH'); conn.execute('PRAGMA wal_checkpoint(FULL);'); conn.close();" 2>/dev/null

# 2. Respaldo directo de la base de datos
if [ -f "$DB_PATH" ]; then
    cp "$DB_PATH" "$BACKUP_DIR/m82_database_$TIMESTAMP.db"
    echo "✅ [PERSISTENCIA] Base de datos respaldada: $BACKUP_DIR/m82_database_$TIMESTAMP.db"
fi

# 3. Respaldo comprimido del código completo y scripts (~/M82)
tar -czf "$BACKUP_DIR/M82_FullCode_$TIMESTAMP.tar.gz" -C "$HOME" M82/ --exclude="*.log" 2>/dev/null
echo "📦 [CÓDIGO] Snapshot del entorno guardado: $BACKUP_DIR/M82_FullCode_$TIMESTAMP.tar.gz"

# 4. Rotación automática: conservar solo los últimos 10 respaldos para optimizar espacio
ls -dt $BACKUP_DIR/m82_database_*.db | tail -n +11 | xargs rm -f 2>/dev/null
ls -dt $BACKUP_DIR/M82_FullCode_*.tar.gz | tail -n +11 | xargs rm -f 2>/dev/null

