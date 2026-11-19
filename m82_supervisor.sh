#!/usr/bin/env bash
cd ~/M82 || exit 1

CORE_DAEMONS=(
  "m82_master_dossier.py"
  "m82_refinitiv_realtime_bridge.py"
  "m82_fusion_engine.py"
  "m82_api_server.py"
  "m82_workspace_hub.py"
  "m82_workspace_sync.py"
  "orch.py"
)

while true; do
  batch_count=0

  for s in "${CORE_DAEMONS[@]}"; do
    if [ -f "$HOME/M82/$s" ] && ! pgrep -f "$s" > /dev/null; then
      nohup python3 -u "$HOME/M82/$s" > "$HOME/M82/logs/${s%.py}.log" 2>&1 &
      batch_count=$((batch_count + 1))
      if [ $((batch_count % 5)) -eq 0 ]; then
        sleep 2.5
      fi
    fi
  done

  for d in "$HOME/M82/desks/"*.py; do
    [ -f "$d" ] || continue
    base=$(basename "$d")
    if ! pgrep -f "$base" > /dev/null; then
      nohup python3 -u "$d" > "$HOME/M82/logs/${base%.py}.log" 2>&1 &
      batch_count=$((batch_count + 1))
      if [ $((batch_count % 5)) -eq 0 ]; then
        sleep 2.5
      fi
    fi
  done

  sleep 15
done
