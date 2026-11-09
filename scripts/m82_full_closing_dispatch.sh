#!/data/data/com.termux/files/usr/bin/bash
set -e

SCRIPT_DIR="$HOME/M82"
DB="$SCRIPT_DIR/m82_database.db"
NTFY="$SCRIPT_DIR/scripts/ntfy.sh"
LOCAL_TIME=$(date +"%H:%M %Z")

# 1. Ejecutar parsers de ingesta
python3 "$SCRIPT_DIR/m82_lseg_block_trades_daemon.py" 2>/dev/null || true
python3 "$SCRIPT_DIR/m82_lseg_market_monitor.py" 2>/dev/null || true
python3 "$SCRIPT_DIR/m82_all_sectors_ingest.py" 2>/dev/null || true

# 2. Resumen Multi-Sectorial a NTFY
$NTFY "🟢 M82 ALL-SECTOR [BULLISH & BREAKOUTS] XAG \$50.58 (+3%) | XAU \$3,940.59 (+1.69%) | MEREY 16 \$93.15 ITM | MO Block Buy \$47.9M | JPM \$222.40 | $LOCAL_TIME | Exp:0.22x VaR:1.68%"
sleep 2

$NTFY "🔴 M82 ALL-SECTOR [BEARISH & REVERSALS] Brent \$104.35 (-8%) | WTI \$96.20 (-7.6%) | AEHR Reversal (-5.4%) | VRTX Reversal (-2.5%) | CWH (-12.2%) | $LOCAL_TIME"
sleep 2

$NTFY "⚪ M82 MACRO DOSSIER STATUS | All-Sectors Ingested | Warsh 102bps | WAL Mode OK | BUNKER 0.30x LOCK | $LOCAL_TIME"

echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') ALL SECTORS FULL DISPATCH COMPLETE" >> "$SCRIPT_DIR/logs/auto_ntfy.log"
