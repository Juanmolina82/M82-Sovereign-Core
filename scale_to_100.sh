#!/bin/bash
# M82 DAEMON SWARM SCALER — 100 DAEMONS FULL ROBUSTNESS
BASE=~/M82
echo "[$(date)] Launching Swarm Scale to 100 Daemons..."
for i in $(seq 1 100); do
    if ! pgrep -f "m82_daemon.py --id $i " > /dev/null; then
        nohup python3 -u $BASE/m82_daemon.py --id $i --mode LISTEN > $BASE/logs/daemon_$i.log 2>&1 &
    fi
done
echo "[$(date)] 100 Daemons operational."
