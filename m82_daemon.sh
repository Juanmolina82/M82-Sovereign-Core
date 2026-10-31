#!/usr/bin/env bash
termux-wake-lock 2>/dev/null || true

while true; do
    if ! pgrep -f "m82_api_server.py" > /dev/null; then
        nohup python3 ~/M82/m82_api_server.py > ~/M82/api_server.log 2>&1 &
    fi
    sleep 5
done
