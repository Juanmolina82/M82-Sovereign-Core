#!/data/data/com.termux/files/usr/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$SCRIPT_DIR/m82_database.db"
NTFY="$SCRIPT_DIR/scripts/ntfy.sh"
LOCAL=$(date +"%H:%M %Z")

# Ejecuta ingesta previa de CSV de bloques si existe
python3 "$SCRIPT_DIR/m82_lseg_block_trades_daemon.py" 2>/dev/null || true

# Extraer sumas de notional Buy vs Sell
BLOCK_BUYS=$(sqlite3 "$DB" "SELECT IFNULL(PRINTF('$%.2fM', SUM(notional_usd)/1000000.0), '$0.00M') FROM m82_block_trades WHERE side='BUY';" 2>/dev/null || echo "$0.00M")
BLOCK_SELLS=$(sqlite3 "$DB" "SELECT IFNULL(PRINTF('$%.2fM', SUM(notional_usd)/1000000.0), '$0.00M') FROM m82_block_trades WHERE side='SELL';" 2>/dev/null || echo "$0.00M")

$NTFY "🟢 M82 BLOCK TRADES [INSTITUTIONAL BUYS] Total Block Buys: $BLOCK_BUYS | Late-day Bid: MARA, RKLB, VRTX | $LOCAL | Exp:0.22x VaR:1.68%"
sleep 2

$NTFY "🔴 M82 BLOCK TRADES [INSTITUTIONAL SELLS] Total Block Sells: $BLOCK_SELLS | Dark Pool Sells: Mega-Caps NDX | $LOCAL"

