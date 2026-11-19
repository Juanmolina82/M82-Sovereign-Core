#!/usr/bin/env bash
M82_ROOT="$HOME/M82"
DB_PATH="$M82_ROOT/m82_database.db"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S VET")

echo "════════════════════════════════════════════════════════════════════════"
echo " M82 SWARM AUDIT — $TIMESTAMP"
echo " Caracas HQ → Governance | Charallave L4/L5 Edge → Execution"
echo "════════════════════════════════════════════════════════════════════════"

echo -e "\n=== 1. SQLite WAL & Registry ==="
if [ -f "$DB_PATH" ]; then
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA journal_mode=WAL;" | grep -qi wal && echo "[OK] WAL MODE"
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT COUNT(*) || ' Daemons Registrados' FROM m82_daemons_registry;" 2>/dev/null || echo "[--] Tabla registry pendiente"
else
  echo "[WARN] DB no encontrada en $DB_PATH"
fi

echo -e "\n=== 2. Procesos Activos en Kernel ==="
ps aux | grep -E "m82|orch.py" | grep -v grep

echo -e "\n=== 3. Motores Master ==="
for e in m82_supervisor.sh orch.py m82_master_dossier.py m82_api_server.py m82_fusion_engine.py m82_refinitiv_realtime_bridge.py; do
  if ls "$M82_ROOT/$e" "$M82_ROOT/desks/$e" 2>/dev/null | grep -q .; then
    echo "[OK] $e"
  else
    echo "[--] $e"
  fi
done
echo "════════════════════════════════════════════════════════════════════════"
