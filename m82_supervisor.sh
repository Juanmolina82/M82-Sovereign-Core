#!/bin/bash
cd ~/M82
DAEMONS=("m82_master_dossier.py" "m82_refinitiv_realtime_bridge.py" "m82_fusion_engine.py" "m82_api_server.py" "orch.py" "m82_quantum_bigdata_bridge.py")
while true; do
  for s in "${DAEMONS[@]}"; do
    if [ -f "$s" ] && ! pgrep -f "$s" > /dev/null; then
      nohup python3 -u "$s" > "${s%.py}.log" 2>&1 &
    fi
  done
  for d in ~/M82/desks/*.py; do
    [ -f "$d" ] || continue
    base=$(basename "$d")
    if ! pgrep -f "$base" > /dev/null; then
      nohup python3 -u "$d" > ~/M82/desks/${base%.py}.log 2>&1 &
    fi
  done
  sleep 15
done
