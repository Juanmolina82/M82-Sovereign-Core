#!/usr/bin/env bash

DB_PATH="$HOME/M82/m82_database.db"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=============================================================================="
echo "🛡️ AUDITORÍA DE FLOTA M82 // $TIMESTAMP"
echo "=============================================================================="

TOTAL_ACTIVE=$(sqlite3 "$DB_PATH" <<SQL
PRAGMA busy_timeout=60000;
SELECT COUNT(*) FROM m82_daemons_registry WHERE status='ACTIVE_REGISTERED';
SQL
| grep -E '^[0-9]+$' | tail -n 1)

if [ -z "$TOTAL_ACTIVE" ]; then
    TOTAL_ACTIVE="0"
fi

echo " 🤖 Daemons Registrados Activos: $TOTAL_ACTIVE / 64"
echo "------------------------------------------------------------------------------"
echo " 📋 Resumen por Mesa Macro (Desk):"

sqlite3 "$DB_PATH" <<SQL | grep '|' | while IFS='|' read -r DESK COUNT; do
PRAGMA busy_timeout=60000;
SELECT desk_category, COUNT(*) FROM m82_daemons_registry GROUP BY desk_category;
SQL
    printf "  ├─> %-25s : %2d vectores\n" "$DESK" "$COUNT"
done

echo "=============================================================================="
