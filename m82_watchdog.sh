#!/usr/bin/env bash
LOCKFILE="$HOME/M82/logs/m82_watchdog.pid"
mkdir -p "$HOME/M82/logs"

if [ -f "$LOCKFILE" ]; then
    OLD_PID=$(cat "$LOCKFILE" 2>/dev/null)
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null && [ "$OLD_PID" != "$$" ]; then
        exit 0
    fi
fi
echo "$$" > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT INT TERM

while true; do
    if [ -f "$HOME/M82/scripts/m82_refinitiv_realtime_bridge.py" ]; then
        if ! pgrep -f "m82_refinitiv_realtime_bridge.py" >/dev/null 2>&1; then
            setsid nohup nice -n 5 python3 -u "$HOME/M82/scripts/m82_refinitiv_realtime_bridge.py" >> "$HOME/M82/logs/m82_refinitiv_realtime_bridge.log" 2>&1 < /dev/null &
        fi
    fi
    if [ -f "$HOME/M82/orch.py" ]; then
        if ! pgrep -f "orch.py" >/dev/null 2>&1; then
            setsid nohup python3 -u "$HOME/M82/orch.py" >> "$HOME/M82/logs/orch.log" 2>&1 < /dev/null &
        fi
    fi
    sleep 30
done
