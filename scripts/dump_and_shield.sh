#!/usr/bin/env bash
set -e

BACKUP_DIR="$HOME/M82/backups"
SDCARD_DIR="/sdcard/M82_BUNKER_BACKUP"

mkdir -p "$BACKUP_DIR"
mkdir -p "$SDCARD_DIR" 2>/dev/null || true

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_PATH="$HOME/M82/m82_database.db"

echo "[*] Iniciando protocolo Bunker Shield & Dump..."

# 1. Vacuum y backup SQLite
sqlite3 "$DB_PATH" "VACUUM;"
sqlite3 "$DB_PATH" ".backup '$BACKUP_DIR/m82_db_$TIMESTAMP.sq3'"

# 2. Respaldo a SDCard si existe acceso
if [ -d "$SDCARD_DIR" ]; then
    cp "$BACKUP_DIR/m82_db_$TIMESTAMP.sq3" "$SDCARD_DIR/"
    echo "[✓] Copia enviada a almacenamiento secundario ($SDCARD_DIR)."
fi

echo "[✓] Respaldo final completado: m82_db_$TIMESTAMP.sq3"
