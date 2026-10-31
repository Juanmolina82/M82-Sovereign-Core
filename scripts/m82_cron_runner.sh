#!/bin/bash
# M82 V60.7.1 PRIME DUAL CRON ORCHESTRATOR + MULTIMEDIA MATRIX DISPATCH

termux-wake-lock

LAST_PUSH=""

while true; do
  CURRENT_TIME=$(date +"%H:%M")
  
  # 1. Bucle continuo de daemons, UI, notificaciones y generación de tarjetas HD
  python3 ~/M82/m82_macro200_grid_deploy.py > /dev/null 2>&1 || true
  python3 ~/M82/m82_caracas_dashboard_v6033_builder.py > /dev/null 2>&1 || true
  python3 ~/M82/m82_daemon_notifier.py > /dev/null 2>&1 || true
  python3 ~/M82/m82_card_dispatch_engine.py > /dev/null 2>&1 || true
  
  # 2. Auto-push 08:00 VET (Apertura Matutina)
  if [ "$CURRENT_TIME" == "08:00" ] && [ "$LAST_PUSH" != "08:00" ]; then
    bash ~/M82/m82_daily_0800_scheduler.sh > /dev/null 2>&1 || true
    python3 -c "import sys; sys.path.append('$HOME/M82'); from m82_private_bot import dispatch_executive_summary; dispatch_executive_summary('MORNING OPENING DISPATCH')" > /dev/null 2>&1 || true
    LAST_PUSH="08:00"
  fi

  # 3. Auto-push 16:00 VET (Cierre de Mercado)
  if [ "$CURRENT_TIME" == "16:00" ] && [ "$LAST_PUSH" != "16:00" ]; then
    python3 ~/M82/m82_lpl_daily_reporter.py > /dev/null 2>&1 || true
    python3 -c "import sys; sys.path.append('$HOME/M82'); from m82_private_bot import dispatch_executive_summary; dispatch_executive_summary('MARKET CLOSE DISPATCH')" > /dev/null 2>&1 || true
    LAST_PUSH="16:00"
  fi

  sleep 300
done
