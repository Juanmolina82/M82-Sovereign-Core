#!/data/data/com.termux/files/usr/bin/bash

# Asegurar CPU activa
termux-wake-lock

# 1. Verificar si el Orquestador Principal está corriendo
if ! pgrep -f "m82_cron_runner.sh" > /dev/null; then
    echo "[$(date)] ⚠️ Orchestrator caído. Reviviendo M82 Citadel Prime..." >> ~/M82/watchdog.log
    cd ~/M82
    nohup bash ~/M82/m82_cron_runner.sh > ~/M82/cron_prime.log 2>&1 &
fi

# 2. Mantener activo el Servidor HTTP de Dashboard (:8080)
if ! pgrep -f "http.server 8080" > /dev/null; then
    cd ~/M82/dashboard && nohup python3 -m http.server 8080 --bind 0.0.0.0 > /dev/null 2>&1 &
fi
