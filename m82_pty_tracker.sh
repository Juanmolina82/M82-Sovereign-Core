#!/data/data/com.termux/files/usr/bin/bash
DB="$HOME/M82/m82_database.db"
NTFY_URL="https://ntfy.sh/M82-Molina-Alerts-v2"

FLIGHT="PTY-CCS / PTY-CUR-CCS"
P8_ISR_ACTIVE=1
SCORE=90

INSERTED=$(sqlite3 "$DB" -cmd "PRAGMA busy_timeout=5000;" <<SQL
PRAGMA journal_mode=WAL;

INSERT INTO m82_multi_stream (daemon_source, headline, final_score, status, created_at)
SELECT 
  'ADS-B_PTY_MONITOR',
  'VECTOR ALTA CONVICCIÓN: P-8 ISR + Trayectoria $FLIGHT (MCM Pattern)',
  $SCORE,
  'ACTIVE_VECTOR',
  datetime('now')
WHERE $P8_ISR_ACTIVE = 1 
  AND NOT EXISTS (
    SELECT 1 FROM m82_multi_stream 
    WHERE daemon_source = 'ADS-B_PTY_MONITOR' 
      AND created_at >= datetime('now', '-1 hour')
  );

SELECT changes();
SQL
)

INSERTED_CLEAN=$(echo "$INSERTED" | tr -cd '0-9')
INSERTED_CLEAN=${INSERTED_CLEAN:-0}

if [ "$INSERTED_CLEAN" -gt 0 ]; then
  curl -s -H "Priority: max" -H "Title: 🚨 CORRELACIÓN P-8 + PTY DETECTADA" -d "[$SCORE] Traza confirmada con cobertura ISR -> Capa 1 ACTIVADA" "$NTFY_URL" > /dev/null
  echo "[$(date '+%H:%M:%S')] CORRELACIÓN P-8 + PTY INYECTADA $SCORE -> ntfy enviado."
fi
