#!/data/data/com.termux/files/usr/bin/bash
set -e

SCRIPT_DIR="$HOME/M82"
cd "$SCRIPT_DIR"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

while true; do
  # Executar Ingesta y Despacho Dual (Telegram + NTFY)
  bash "$SCRIPT_DIR/scripts/m82_dual_5min_dispatcher.sh" > /dev/null 2>&1 || true

  # Ventana de espera de 5 minutos (300 segundos)
  sleep 300
done
