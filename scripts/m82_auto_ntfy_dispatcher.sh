#!/data/data/com.termux/files/usr/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$SCRIPT_DIR/m82_database.db"
NTFY="$SCRIPT_DIR/scripts/ntfy.sh"
LOG="$SCRIPT_DIR/logs/auto_ntfy.log"
mkdir -p "$SCRIPT_DIR/logs"
get_sentiment() { sqlite3 "$DB" "SELECT entity || ': ' || status || ' (Score: ' || sentiment_score || ')' FROM m82_refinitiv_sentiment ORDER BY rowid DESC LIMIT 1;" 2>/dev/null || echo "No Data"; }
get_precious() { sqlite3 "$DB" "SELECT 'XAU $' || xau || ' | XAG $' || xag FROM m82_precious_flash ORDER BY rowid DESC LIMIT 1;" 2>/dev/null || echo "XAU $3902.03 | XAG $50.08"; }
get_global() { sqlite3 "$DB" "SELECT 'Brent $' || brent || ' | STOXX ' || stox || '%' FROM m82_global_markets ORDER BY rowid DESC LIMIT 1;" 2>/dev/null || echo "Brent $108.00 | STOXX -0.10%"; }
LOCAL=$(date +"%H:%M %Z")
SENTIMENT=$(get_sentiment)
PRECIOUS=$(get_precious)
GLOBAL=$(get_global)
$NTFY "🟢 M82 MACRO DOSSIER [BULLISH & PRECIOUS] $PRECIOUS | MEREY 16 \$93.15 ITM | YPF Vaca Muerta +50-75% | Anthropic \$16.96B | $LOCAL | Exp:0.22x VaR:1.68%"
sleep 2
$NTFY "🔴 M82 MACRO DOSSIER [BEARISH & RISKS] $GLOBAL | Gasoline Crack \$9.17 (-82%) | EWZ -27.37% | Tech Capex Caution | $LOCAL"
sleep 2
$NTFY "⚪ M82 MACRO DOSSIER [STATUS & SENTIMENT] $SENTIMENT | Warsh 102bps | BUNKER 0.30x LOCK | $LOCAL"
echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') DISPATCH AUTO NTFY OK" >> "$LOG"
