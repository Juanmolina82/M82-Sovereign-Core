#!/bin/bash
echo "=== INICIANDO NODO CHARALLAVE: HIGH_PERFORMANCE_LITE ==="
while true; do
    # Monitoreo de temperatura Termux
    TEMP=$(termux-battery-status | jq '.temperature' 2>/dev/null || echo "38")
    
    # Check si supera barrera térmica de 41°C
    if (( $(echo "$TEMP >= 41.0" | bc -l 2>/dev/null || echo 0) )); then
        echo "[!] ALERTA TÉRMICA: ${TEMP}°C. Reduciendo polling a 15s..."
        SLEEP_TIME=15
    else
        SLEEP_TIME=5
    fi

    # Disparo de estado de daemons
    sqlite3 ~/M82/m82_database.db "SELECT id, name, category, status FROM m82_daemons_registry;"
    sleep $SLEEP_TIME
done
