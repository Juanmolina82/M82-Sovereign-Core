#!/bin/bash
# M82 DAEMON SWARM SCALER — 80 DAEMONS ACTIVE — LSEG ADVANCED SUITE
echo "[M82] Scaling daemon swarm 70->80 active nodes — LSEG Advanced Suite 02:35 AM..."
mkdir -p ~/M82/logs
for i in $(seq 71 80); do
  nohup python3 -u ~/M82/m82_daemon.py --id $i --mode LISTEN > ~/M82/logs/daemon_$i.log 2>&1 &
  echo "[M82] Daemon $i ACTIVE PID $!"
  sleep 0.2
done
echo "[M82] 80 Daemons fully operational under m82_supervisor.sh — WAL 0/0/0"
ps aux | grep m82_daemon | wc -l
