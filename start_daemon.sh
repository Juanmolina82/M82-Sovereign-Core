#!/bin/bash
termux-wake-lock

# Detener instancias previas
pkill -f m82_daemon.py 2>/dev/null
pkill -f m82_telegram_bot.py 2>/dev/null

# Arrancar Daemon Supervisor y Bot Interactivo
nohup python3 m82_daemon.py > m82_daemon.log 2>&1 &
nohup python3 m82_telegram_bot.py > m82_bot.log 2>&1 &

echo "✅ M82 Daemon y Bot Interactivo iniciados en segundo plano."
echo "📌 Logs Daemon: tail -f m82_daemon.log"
echo "📌 Logs Bot: tail -f m82_bot.log"
