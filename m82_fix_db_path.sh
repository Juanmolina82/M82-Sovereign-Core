#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE_DIR="$HOME/M82"
DB_FILE="$BASE_DIR/m82_database.db"
DB_SUBDIR="$BASE_DIR/db"

echo "⚡ [M82 PATH FIX] Enlazando ruta canónica ~/M82/db/m82_database.db..."

# 1. Crear subdirectorio db si no existe
mkdir -p "$DB_SUBDIR"

# 2. Crear enlace simbólico forzado
ln -sf "$DB_FILE" "$DB_SUBDIR/m82_database.db"

# 3. Verificación de lectura atómica
sqlite3 "$DB_SUBDIR/m82_database.db" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;
SELECT '🟢 [HOTFIX OK] LECTURA EXITOSA DESDE SUBDIRECTORIO /db/: ' || COUNT(*) || ' registros MCM' 
FROM m82_multi_stream WHERE daemon_source LIKE '%MCM%';
SQL

echo "✅ [SUCCESS] Symlink ~/M82/db/m82_database.db -> ~/M82/m82_database.db establecido."
