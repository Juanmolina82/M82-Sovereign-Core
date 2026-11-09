#!/usr/bin/env bash
pkill -f "m82_futures_bridge.py" 2>/dev/null || true
nohup python3 -u ~/M82/m82_futures_bridge.py > ~/M82/desks/refinitiv_bridge.log 2>&1 &
echo "[M82 DAEMON] Demonio de Futuros Activo en Background (PID: $!)."
