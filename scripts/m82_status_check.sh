#!/usr/bin/env bash
set -e

DB="$HOME/M82/m82_database.db"

echo "=========================================================="
echo "    M82 SOVEREIGN EDGE :: AUDITORÍA EN TIEMPO REAL        "
echo "=========================================================="

echo -e "\n1. PROCESOS ACTIVOS EN MEMORIA:"
ps aux | grep -E "python3|supervisor|orch" | grep -v grep | awk '{print "  PID: "$2" | CPU: "$3"% | MEM: "$4"% | CMD: "$11" "$12}'

echo -e "\n2. ESTADO WAL & PERSISTENCIA DE BASE DE DATOS:"
sqlite3 "$DB" "PRAGMA journal_mode; PRAGMA busy_timeout;" | awk '{print "  " $0}'

echo -e "\n3. REGISTRO DE STREAMING DE EVENTOS (M82_MULTI_STREAM):"
sqlite3 "$DB" "SELECT COUNT(*) FROM m82_multi_stream;" | awk '{print "  Total Eventos Registrados: " $0}'

echo -e "\n4. DAEMONS SUPERVISADOS ACTIVOS:"
sqlite3 "$DB" "SELECT COUNT(*) FROM m82_daemons_registry WHERE status='ACTIVE';" 2>/dev/null || echo "  Tabla m82_daemons_registry lista."

echo "=========================================================="
