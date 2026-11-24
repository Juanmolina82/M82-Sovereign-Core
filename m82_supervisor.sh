#!/usr/bin/env bash
cd "$HOME/M82"
termux-wake-lock 2>/dev/null || true

DAEMONS=(
    "m82_master_dossier.py"
    "orch.py"
    "m82_api_server.py"
    "scripts/m82_nivel11_hjb.py"
    "scripts/m82_familia_daemons.py"
    "scripts/m82_refinitiv_realtime_bridge.py"
)

while true; do
    for script in "${DAEMONS[@]}"; do
        if [ -f "$HOME/M82/$script" ] && ! pgrep -f "$script" > /dev/null; then
            nohup nice -n 10 python3 -u "$HOME/M82/$script" >> "$HOME/M82/logs/$(basename "${script%.py}").log" 2>&1 &
            sleep 1
        fi
    done

    if [ -f "$HOME/M82/m82_unified_core.py" ] && ! pgrep -f "m82_unified_core.py" > /dev/null; then
        nohup nice -n 10 python3 -u "$HOME/M82/m82_unified_core.py" >> "$HOME/M82/logs/unified_core.log" 2>&1 &
        sleep 1
    fi

    if [ -f "$HOME/M82/.env.cf" ] && ! pgrep -f "cloudflared tunnel run" > /dev/null; then
        CF_TOKEN=$(cut -d '=' -f2- "$HOME/M82/.env.cf" | tr -d '"' | tr -d "'" | xargs)
        if [ -n "$CF_TOKEN" ]; then
            nohup nice -n 10 cloudflared tunnel run --token "$CF_TOKEN" >> "$HOME/M82/logs/cf_tunnel.log" 2>&1 &
            sleep 1
        fi
    fi

    sleep 15
done
