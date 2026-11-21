#!/usr/bin/env bash
cd ~/M82
DAEMONS=("m82_master_dossier.py" "refinitiv_bridge.py" "price_feeder.py" "orch.py" "execution_engine.py")

while true; do
    for script in "${DAEMONS[@]}"; do
        if ! pgrep -f "$script" > /dev/null; then
            nohup python3 -u "$script" > "${script%.py}.log" 2>&1 &
            sleep 1
        fi
    done
    ~/M82/auto_cleanup.sh > /dev/null 2>&1 || true
    sleep 15
done
