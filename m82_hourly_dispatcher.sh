#!/usr/bin/env bash
# M82 :: Dispatcher 37 * * * *
set -uo pipefail
cd ~/M82 || exit 1
python3 ~/M82/m82_inject_live_prices.py
python3 ~/M82/m82_gas_universe_monitor.py > /tmp/m82_payload.txt 2>&1 || true
bash ~/M82/m82_realtime_multichannel_dispatch.sh
sqlite3 ~/M82/m82_database.db "PRAGMA wal_checkpoint(TRUNCATE);"
echo "[M82 CRON DISPATCH OK] ✅ Reporte despachado a Bot Privado + NYFT ($(date +'%I:%M %p -04') / Cadencia 1H)"
