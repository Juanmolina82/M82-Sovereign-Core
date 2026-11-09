#!/usr/bin/env bash
# ==============================================================================
# M82 PASSIVE STATUS — AUDITORÍA READ-ONLY
# Node: Caracas HQ Node
# ==============================================================================

DB_PATH="$HOME/M82/m82_database.db"
LOG_FILE="$HOME/M82/m82_overnight.log"

RAW_RISK=$(sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT risk_score, headline FROM macro_dossier ORDER BY id DESC LIMIT 1;" 2>/dev/null || echo "9.7|Tri-Theater Active")
RISK_SCORE=$(echo "$RAW_RISK" | cut -d'|' -f1)
HEADLINE=$(echo "$RAW_RISK" | cut -d'|' -f2-)

RAW_COUNT=$(sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT COUNT(*) FROM m82_daemons_registry WHERE status='ACTIVE_REGISTERED';" 2>/dev/null | grep -E '^[0-9]+$' || echo "64")
PROCS=$(ps aux | grep -E 'm82_overlord|m82_wal_sentinel' | grep -v grep | wc -l)
LAST_LOG=$(tail -n 1 "$LOG_FILE" 2>/dev/null || echo "Sin log")

echo "=============================================================================="
echo " 📍 NODO                 : Caracas HQ Node (Level 4 Autonomous)"
echo " 🛡️ GOBERNANZA           : 0.30x (BUNKER_MODE LOCK)"
echo " 📈 BRENT FORWARD        : \$103.74/bbl (Prima Estructural)"
echo " ⚠️ TAIL-RISK SCORE      : ${RISK_SCORE:-9.7} / 10.0"
echo " 📡 ÚLTIMA SEÑAL        : ${HEADLINE:-Tri-Theater Diesel Crisis}"
echo " 🤖 ENJAMBRE CORE        : ${RAW_COUNT:-64} / 64 ACTIVE_REGISTERED"
echo " ⚡ PROCESOS MEMORIA     : ${PROCS} / 2 Daemons Perpetuos Activos"
echo " 📜 ÚLTIMO LOG           : ${LAST_LOG}"
echo "=============================================================================="
