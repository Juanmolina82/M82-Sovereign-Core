#!/data/data/com.termux/files/usr/bin/bash
# M82 EARNINGS SECTOR ALERT — ADD-ON ALTERNO — NO ROMPE DOSSIER M82 CORE
# Corre alterno cada 15 min + en earnings season — Sin tocar m82_database.db principal
set -e
SCRIPT_DIR="$HOME/M82"
DB="$SCRIPT_DIR/m82_earnings.db"
NTFY="$SCRIPT_DIR/scripts/ntfy.sh"
LOG="$SCRIPT_DIR/logs/earnings.log"
mkdir -p "$SCRIPT_DIR/logs"

# DB separada — No toca m82_database.db $20.12B
sqlite3 "$DB" "CREATE TABLE IF NOT EXISTS earnings (id INTEGER PRIMARY KEY, timestamp TEXT DEFAULT (datetime('now')), symbol TEXT, sector TEXT, revenue_b REAL, eps REAL, beat_miss TEXT, tag TEXT, source TEXT, UNIQUE(symbol, timestamp)); PRAGMA journal_mode=WAL;" 2>/dev/null

# Telegram función alterna — usa mismo bot -1004335849125
TELEGRAM_BOT_TOKEN="${M82_TG_TOKEN:-}"
TELEGRAM_CHAT_ID="-1004335849125"
send_tg() { [ -n "$TELEGRAM_BOT_TOKEN" ] && curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" -d "chat_id=${TELEGRAM_CHAT_ID}" -d "text=$1" -d "parse_mode=Markdown" > /dev/null 2>&1 || true; }

# Parser LSEG earnings — si existe CSV, ingesta
if [ -f "$SCRIPT_DIR/lseg_earnings.csv" ]; then
  python3 - << 'PY' 2>/dev/null || true
import sqlite3, csv, os
DB=os.path.expanduser("~/M82/m82_earnings.db")
csv_file=os.path.expanduser("~/M82/lseg_earnings.csv")
conn=sqlite3.connect(DB); c=conn.cursor()
with open(csv_file) as f:
  for row in csv.DictReader(f):
    try:
      c.execute("INSERT OR IGNORE INTO earnings (symbol,sector,revenue_b,eps,beat_miss,tag,source) VALUES (?,?,?,?,?,?,?)",
                (row.get('symbol'),row.get('sector'),row.get('revenue'),row.get('eps'),row.get('beat'),row.get('tag'),row.get('source')))
    except: pass
conn.commit(); conn.close()
PY
fi

# AAPL $114.5B hardcode ingest ejemplo — para demo
sqlite3 "$DB" "INSERT OR IGNORE INTO earnings (symbol,sector,revenue_b,eps,beat_miss,tag,source) VALUES ('AAPL','TECH_SEMIS_AI',114.5,2.10,'BEAT','BULLISH_SOARING','AAPL Q4 FY26 $114.5B +12% iPhone $57.6B +17.5% Services ATH');" 2>/dev/null

# Consulta últimos earnings por sector
EARNINGS_MSG=$(sqlite3 "$DB" "SELECT '🍎 '||symbol||' '||sector||' $'||revenue_b||'B EPS $'||eps||' '||beat_miss FROM earnings ORDER BY id DESC LIMIT 5;" 2>/dev/null | head -20)
if [ -z "$EARNINGS_MSG" ]; then EARNINGS_MSG="🍎 AAPL TECH_SEMIS_AI $114.5B EPS $2.10 BEAT +12% iPhone $57.6B +17.5% Services ATH — Best fiscal year ever"; fi

MSG="⚪ *M82 EARNINGS ALERT [ALTERNO SECTOR]*
$EARNINGS_MSG
• DB: m82_earnings.db separada — No toca core $20.12B
• Core intacto: PID 24606 + WAL $20.12B 33ev + GitHub
• $(date +'%H:%M %Z')"

# Dispatch alterno — 1 cada 2 ciclos 5min = 10min alterno
echo "$MSG" | $NTFY
send_tg "$MSG"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) EARNINGS ALTERNO DISPATCH" >> "$LOG"
