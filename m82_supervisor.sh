#!/usr/bin/env bash
M82_DIR="$HOME/M82"
termux-wake-lock 2>/dev/null || true

while true; do
    # Vigilar Servidor Unificado :8286
    if ! pgrep -f "m82_unified_8286.py" > /dev/null; then
        nohup python3 "$M82_DIR/m82_unified_8286.py" >> "$M82_DIR/hub_8286.log" 2>&1 &
    fi

    # Vigilar Orquestador Core si existe
    if [ -f "$M82_DIR/m82_core_orchestrator.py" ] && ! pgrep -f "m82_core_orchestrator.py" > /dev/null; then
        nohup python3 "$M82_DIR/m82_core_orchestrator.py" >> "$M82_DIR/orch.log" 2>&1 &
    fi

    # Vigilar Puente Refinitiv si existe
    if [ -f "$M82_DIR/m82_refinitiv_realtime_bridge.py" ] && ! pgrep -f "m82_refinitiv_realtime_bridge.py" > /dev/null; then
        nohup python3 "$M82_DIR/m82_refinitiv_realtime_bridge.py" >> "$M82_DIR/refinitiv.log" 2>&1 &
    fi

    # Vigilar los 40 daemons de mesas en ~/M82/desks/
    if [ -d "$M82_DIR/desks" ]; then
        for d in "$M82_DIR/desks/"*.py; do
            [ -f "$d" ] || continue
            bname=$(basename "$d")
            if ! pgrep -f "$bname" > /dev/null; then
                nohup python3 "$d" >> "$M82_DIR/desks.log" 2>&1 &
            fi
        done
    fi

    sleep 15
done
pgrep -f "m82_quant_daemon.py" >/dev/null || nohup nice -n 10 python3 -O "$HOME/M82/m82_quant_daemon.py" >> "$HOME/M82/logs/quant_daemon.log" 2>&1 &
