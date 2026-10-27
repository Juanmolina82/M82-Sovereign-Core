#!/data/data/com.termux/files/usr/bin/bash

LOG_FILE="$HOME/M82/data/m82_daemon.log"
mkdir -p "$HOME/M82/data"

echo "[+] Iniciando Daemon M82 Automation (Intervalo: 60s)..." >> "$LOG_FILE"

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$TIMESTAMP] Executing M82 Real-Time Stream & Earnings..." >> "$LOG_FILE"
    
    # 1. Ejecutar Ingesta e Informe LSEG Realtime
    python $HOME/M82/scripts/lseg_live_ingest.py >> "$LOG_FILE" 2>&1
    
    # 2. Ejecutar Stream de Earnings Bancarios
    python $HOME/M82/scripts/m82_bank_stream.py >> "$LOG_FILE" 2>&1
    
    # 3. Disparar notificaciones a Telegram
    python $HOME/M82/scripts/m82_telegram_sender.py >> "$LOG_FILE" 2>&1
    
    echo "[$TIMESTAMP] Ciclo completado. Esperando 60 segundos..." >> "$LOG_FILE"
    sleep 60
done
