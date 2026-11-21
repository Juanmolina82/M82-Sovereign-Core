#!/data/data/com.termux/files/usr/bin/bash
export PATH=/data/data/com.termux/files/usr/bin:$PATH
BASE_DIR="/data/data/com.termux/files/home/M82"
LOG_FILE="$BASE_DIR/logs/watchdog.log"

mkdir -p "$BASE_DIR/logs"
cd "$BASE_DIR" || exit 1

# Mantener CPU despierta
termux-wake-lock 2>/dev/null || true

# 1) Vigilar orch.py
if ! pgrep -f "python3.*orch.py" > /dev/null 2>&1; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ⚠️ orch.py caído. Reiniciando..." >> "$LOG_FILE"
    nohup python3 -u "$BASE_DIR/orch.py" >> "$BASE_DIR/logs/orch.log" 2>&1 &
fi

# 2) Vigilar m82_macro200_engine.py
if [ -f "$BASE_DIR/m82_macro200_engine.py" ] && ! pgrep -f "m82_macro200_engine.py" > /dev/null 2>&1; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ⚠️ macro200_engine caído. Reiniciando..." >> "$LOG_FILE"
    nohup python3 -O "$BASE_DIR/m82_macro200_engine.py" >> "$BASE_DIR/logs/macro200_boot.log" 2>&1 &
fi

# 3) Vigilar 40 Daemons Lite Wake-Lock
if [ -f "$BASE_DIR/m82_run_40_daemons_lite.py" ] && ! pgrep -f "m82_run_40_daemons_lite.py --daemon" > /dev/null 2>&1; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ⚠️ 40 Daemons Lite caído. Reiniciando..." >> "$LOG_FILE"
    nohup python3 -O "$BASE_DIR/m82_run_40_daemons_lite.py" --daemon >> "$BASE_DIR/logs/wakelock_40_lite.log" 2>&1 &
fi

# 4) Vigilar Bot Telegram & Renderizador HUD
if [ -f "$BASE_DIR/m82_telegram_bot.py" ] && ! pgrep -f "m82_telegram_bot.py --daemon" > /dev/null 2>&1; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ⚠️ Telegram Bot caído. Reiniciando..." >> "$LOG_FILE"
    nohup python3 -O "$BASE_DIR/m82_telegram_bot.py" --daemon >> "$BASE_DIR/logs/telegram_bot.log" 2>&1 &
fi

# 5) Vigilar Servidor HTTP PWA (:8080)
if ! pgrep -f "http.server 8080" > /dev/null 2>&1; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ⚠️ HTTP :8080 caído. Reiniciando..." >> "$LOG_FILE"
    nohup python3 -m http.server 8080 --bind 127.0.0.1 --directory "$BASE_DIR" >> "$BASE_DIR/logs/http_8080.log" 2>&1 &
fi

# 6) Vigilar Conector LSEG NewsMon (DJN/WSJ/BRN/MKTW/IBD/FNL/PENS/WSJP)
if [ -f "$BASE_DIR/m82_lseg_newsmon_ingestor.py" ] && ! pgrep -f "m82_lseg_newsmon_ingestor.py --daemon" > /dev/null 2>&1; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ⚠️ LSEG NewsMon caído. Reiniciando..." >> "$LOG_FILE"
    nohup python3 -O "$BASE_DIR/m82_lseg_newsmon_ingestor.py" --daemon >> "$BASE_DIR/logs/lseg_newsmon.log" 2>&1 &
fi
