#!/data/data/com.termux/files/usr/bin/bash

USER_REF="jmmp@molina82.com"
DB="$HOME/M82/m82_database.db"

HEADLINE="REFINITIV WORKSPACE LIVE ($USER_REF): 22 Bonos VE/PDVSA | Rally WTD +8.45% (Curva Normalizada)"
SCORE=0

sqlite3 "$DB" "PRAGMA busy_timeout=5000; PRAGMA journal_mode=WAL; INSERT INTO m82_multi_stream (daemon_source, headline, final_score, status, created_at) VALUES ('REFINITIV_BONDS_DESK', '$HEADLINE', $SCORE, 'PROCESSED', datetime('now'));" > /dev/null 2>&1

echo "[$(date '+%H:%M:%S')] Ingesta Refinitiv Workspace ($USER_REF) cargada a M82 | Capa 3: [$SCORE]"
