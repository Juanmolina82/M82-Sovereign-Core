#!/usr/bin/env bash
while true; do
    if ! ps aux | grep m82_bot_telegram | grep -v grep > /dev/null; then
        echo "[$(date -u)] ⚠️ Bot inactivo detectado por Centinela. Reactivando PID..." >> ~/M82/watchdog.log
        nohup python3 -u ~/M82/m82_bot_telegram.py > ~/M82/telegram_dispatch.log 2>&1 &
        sleep 2
    fi
    sqlite3 ~/M82/m82_database.db "PRAGMA wal_checkpoint(TRUNCATE);" 2>/dev/null || true
    sleep 60  # Verificación ligera cada 60 segundos
done
