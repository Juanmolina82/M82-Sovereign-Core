#!/usr/bin/env bash
# ==============================================================================
# M82 OVERLORD DAEMON — GOBERNANZA & POLLING AUTÓNOMO (120s)
# Node: Caracas HQ Node
# ==============================================================================

DB_PATH="$HOME/M82/m82_database.db"
LOG_FILE="$HOME/M82/m82_overnight.log"

termux-wake-lock 2>/dev/null || true

# Iniciar Sentinel en paralelo si no está corriendo
if ! pgrep -f "m82_wal_sentinel.sh" > /dev/null; then
    nohup bash "$HOME/M82/m82_wal_sentinel.sh" >/dev/null 2>&1 &
fi

while true; do
    TIMESTAMP=$(date -Iseconds)
    
    # Lectura de último Risk Score y Headline
    RAW_RISK=$(sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT risk_score, headline FROM macro_dossier ORDER BY id DESC LIMIT 1;" 2>/dev/null || echo "9.7|Tri-Theater Diesel Crisis")
    RISK_SCORE=$(echo "$RAW_RISK" | cut -d'|' -f1)
    HEADLINE=$(echo "$RAW_RISK" | cut -d'|' -f2-)
    
    # Actualizar heartbeat de los 64 vectores
    sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; UPDATE m82_daemons_registry SET last_ping=datetime('now') WHERE status='ACTIVE_REGISTERED';" 2>/dev/null

    # Registro de ciclo en Bitácora Nocturna
    echo "--- ${TIMESTAMP} BUNKER 0.30x LOCK | RISK: ${RISK_SCORE:-9.7} | SIGNAL: ${HEADLINE:-Tri-Theater Active} ---" >> "$LOG_FILE"
    
    sleep 120
done
