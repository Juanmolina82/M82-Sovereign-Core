#!/usr/bin/env bash
# ==============================================================================
# M82 RISK DESK — INFRASTRUCTURE STABILIZATION & PRODUCTION LAUNCH
# ==============================================================================

set -e
DB="$HOME/M82/m82_database.db"

echo "🧹 [1/4] Limpiando procesos antiguos en conflicto..."
pkill -9 -f "m82_master_dossier.py" || true
pkill -9 -f "orch.py" || true
sleep 1

echo "🔍 [2/4] Verificando integridad de SQLite WAL e Índices Únicos..."
sqlite3 "$DB" << 'SQL'
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 15000;
PRAGMA integrity_check;
.headers on
.mode column
SELECT count(*) as total_records, 
       sum(case when status='PENDING' then 1 else 0 end) as pending,
       sum(case when status LIKE 'APPROVED%' then 1 else 0 end) as approved,
       sum(case when status LIKE 'SKIPPED%' or status LIKE 'LOW_EV%' then 1 else 0 end) as filtered
FROM m82_multi_stream;
SQL

echo "🚀 [3/4] Lanzando Motor Maestro de Ingesta (60 Daemons Parallel)..."
nohup python3 -u "$HOME/M82/m82_master_dossier.py" > "$HOME/M82/m82_master_dossier.log" 2>&1 &

echo "🧠 [4/4] Lanzando Orquestador con Super Intelligence Layer..."
nohup python3 -u "$HOME/M82/orch.py" > "$HOME/M82/orch.log" 2>&1 &

sleep 2

echo "=============================================================================="
echo "🔥 M82 TRADING DESK OPERATIVO EN PRODUCCIÓN — INFRAESTRUCTURA OK"
echo "=============================================================================="
ps aux | grep python3 | grep -v grep
