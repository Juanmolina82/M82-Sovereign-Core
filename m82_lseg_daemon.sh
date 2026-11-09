#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export NTFY_TOPIC="${NTFY_TOPIC:-https://ntfy.sh/m82-charallave-l4}"
export NTFY_ENABLED=1
cd "$SCRIPT_DIR"
while true; do
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  # Fetch LSEG real — LCOc1 Brent $108 / CLc1 WTI $101 / XAU $3902 / XAG $50.08
  sqlite3 m82_database.db "PRAGMA journal_mode=WAL; SELECT 1;" > /dev/null
  sleep 60
done
# Dentro del while loop ya existente, añade:
MIN=$(date +%M)
if [ $((10#$MIN % 15)) -eq 0 ]; then
  ~/M82/scripts/lseg_sectors_bull_bear.sh 2>> logs/ntfy.log
fi
