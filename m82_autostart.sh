#!/usr/bin/env bash

BASE_DIR="$HOME/M82"
LOG_FILE="$BASE_DIR/m82_autostart.log"

echo "[$(date)] Iniciando secuencia de persistencia M82..." >> "$LOG_FILE"

# Activar wakelock de Termux para evitar que Android suspenda el proceso en segundo plano
termux-wake-lock

# Verificar que la base de datos exista
if [ ! -f "$BASE_DIR/m82_database.db" ]; then
    echo "[$(date)] Base de datos no encontrada. Creando instancia limpia..." >> "$LOG_FILE"
    sqlite3 "$BASE_DIR/m82_database.db" "VACUUM;"
fi

# Verificar si el demonio m82_macro_core.py ya está corriendo
if ! pgrep -f "m82_macro_core.py" > /dev/null; then
    echo "[$(date)] Lanzando m82_macro_core.py..." >> "$LOG_FILE"
    nohup python3 "$BASE_DIR/m82_macro_core.py" >> "$LOG_FILE" 2>&1 &
else
    echo "[$(date)] El proceso m82_macro_core.py ya está activo." >> "$LOG_FILE"
fi

