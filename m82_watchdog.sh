#!/data/data/com.termux/files/usr/bin/bash
# === M82 SINGLETON PID LOCK ===
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
# ================================
export PATH=/data/data/com.termux/files/usr/bin:$PATH
B="/data/data/com.termux/files/home/M82"
mkdir -p "$B/logs"
termux-wake-lock 2>/dev/null || true
pgrep -f "python3.*orch.py" >/dev/null || nohup python3 -u "$B/orch.py" >> "$B/logs/orch.log" 2>&1 &
pgrep -f "m82_macro200_engine.py" >/dev/null || nohup python3 -O "$B/m82_macro200_engine.py" >> "$B/logs/macro200_boot.log" 2>&1 &
pgrep -f "m82_run_40_daemons_lite.py --daemon" >/dev/null || nohup python3 -O "$B/m82_run_40_daemons_lite.py" --daemon >> "$B/logs/wakelock_40_lite.log" 2>&1 &
pgrep -f "m82_telegram_bot.py --daemon" >/dev/null || nohup python3 -O "$B/m82_telegram_bot.py" --daemon >> "$B/logs/telegram_bot.log" 2>&1 &
pgrep -f "http.server 8080" >/dev/null || nohup python3 -m http.server 8080 --bind 127.0.0.1 --directory "$B" >> "$B/logs/http_8080.log" 2>&1 &
