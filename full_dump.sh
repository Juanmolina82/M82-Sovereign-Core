#!/bin/bash
set -e
BASE=$HOME/M82
DB=$BASE/m82_database.db

echo "=== M82 FULL DUMP — $(date) — BUNKER 0.30x ==="
echo ""
echo "--- [1] WAL STATE ---"
sqlite3 $DB "PRAGMA busy_timeout=120000; PRAGMA wal_checkpoint(TRUNCATE); PRAGMA journal_mode; PRAGMA wal_checkpoint;"
echo ""
echo "--- [2] macro_dossier FULL — LAST 25 ---"
sqlite3 $DB <<'SQL'
.headers on
.mode column
PRAGMA busy_timeout=120000;
SELECT id, m82_tag, risk_score, alpha_score, category, substr(headline,1,80) as headline FROM macro_dossier ORDER BY id DESC LIMIT 25;
SQL
echo ""
echo "--- [3] m82_multi_stream FULL — LAST 25 ---"
sqlite3 $DB <<'SQL'
.headers on
.mode column
PRAGMA busy_timeout=120000;
SELECT id, timestamp, daemon_source, alpha_score, event_trigger, substr(headline,1,100) as headline FROM m82_multi_stream ORDER BY id DESC LIMIT 25;
SQL
echo ""
echo "--- [4] banking_ai_risk + oil_gulf_tracker ---"
sqlite3 $DB <<'SQL'
.headers on
.mode column
PRAGMA busy_timeout=120000;
SELECT * FROM banking_ai_risk ORDER BY id DESC LIMIT 10 2>/dev/null || echo "banking_ai_risk empty or uninitialized";
SELECT * FROM oil_gulf_tracker ORDER BY id DESC LIMIT 10 2>/dev/null || echo "oil_gulf_tracker empty or uninitialized";
SQL
echo ""
echo "--- [5] DAEMONS COUNT ---"
pgrep -f daemon | wc -l
echo "PIDs:"
pgrep -f daemon | head -20
echo ""
echo "--- [6] SUPERVISOR + LSEG WEBSOCKET + PWA + WSGI ---"
ps aux | grep -E "supervisor|orch.py|pwa_server|lseg_websocket|wsgi_api" | grep -v grep
echo ""
echo "--- [7] LOGS TAIL 30 LINES ---"
ls -lh $BASE/logs/ 2>/dev/null | tail -20 || true
echo "--- lseg_websocket.log ---"
tail -30 $BASE/lseg_websocket.log 2>/dev/null || echo "no log"
echo ""
echo "--- [8] ALIAS + ENV ---"
alias | grep m82 || true
env | grep -i termux || true
ulimit -n
echo ""
echo "--- [9] GIT STATUS JUANMOLINA82/M82 ---"
cd $BASE && git status --short && git log --oneline -5
echo ""
echo "--- [10] FULL COUNT ---"
sqlite3 $DB "PRAGMA busy_timeout=120000; SELECT 'macro_dossier' as tbl, count(*) FROM macro_dossier UNION ALL SELECT 'multi_stream', count(*) FROM m82_multi_stream;"
echo ""
echo "=== END FULL DUMP — WAL 0/0/0 — BUNKER 0.30x LOCK ==="
