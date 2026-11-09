#!/bin/bash
### ┌────────────────────────────────────────────────────────────────────────┐
### │ M82 SOVEREIGN EXECUTION CORE :: AUDITORÍA UNIFICADA 100+ DAEMONS      │
### │ NODO CENTRAL: Caracas HQ — Governance Master                          │
### │ NODO EDGE: Charallave L4/L5 — Alta densidad — Termux / SQLite WAL     │
### └────────────────────────────────────────────────────────────────────────┘
set -e
M82_ROOT="$HOME/M82"
DB_PATH="$M82_ROOT/m82_database.db"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S VET")

echo "════════════════════════════════════════════════════════════════════════"
echo " M82 SWARM AUDIT (100+ DAEMONS) — $TIMESTAMP"
echo " Caracas HQ → Governance | Charallave L4/L5 → Execution"
echo "════════════════════════════════════════════════════════════════════════"

# 1. DB Registry
echo -e "\n=== 1. m82_daemons_registry (SQLite WAL) ==="
if [ -f "$DB_PATH" ]; then
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA journal_mode=WAL;" | grep -q wal && echo "[OK] WAL MODE"
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT COUNT(*) || ' Daemons Registrados en DB' FROM m82_daemons_registry;" 2>/dev/null || echo "Registry en proceso..."
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(TRUNCATE);" 2>/dev/null
  echo "WAL Status: $(sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA journal_mode;" 2>/dev/null) — CLEAN"
else
  echo "[WARN] DB no encontrada en $DB_PATH"
fi

# 2. Conteo archivos en disco
echo -e "\n=== 2. Archivos Python Daemons en Disco ==="
CORE_COUNT=$(ls -1 $M82_ROOT/m82_*.py 2>/dev/null | wc -l)
DESKS_COUNT=$(ls -1 $M82_ROOT/desks/m82_*.py $M82_ROOT/desks/*.py 2>/dev/null | wc -l)
TOTAL_FILES=$((CORE_COUNT + DESKS_COUNT))
echo "$TOTAL_FILES Archivos Python Totales (Core: $CORE_COUNT + Desks: $DESKS_COUNT)"

# 3. Procesos activos
echo -e "\n=== 3. Procesos Activos Kernel ==="
ACTIVE=$(ps aux | grep -E "python|m82" | grep -v grep | wc -l)
echo "$ACTIVE Procesos Activos en Kernel"
ps aux | grep -E "python|m82" | grep -v grep | head -n 20

# 4. Desglose por mesas
echo -e "\n=== 4. Desglose por Mesas en ~/M82/desks/ ==="
for desk in $M82_ROOT/desks/*/; do
  [ -d "$desk" ] || continue
  COUNT=$(ls -1 "$desk"*.py 2>/dev/null | wc -l)
  echo "  $(basename $desk): $COUNT daemons"
done

# 5. Motores Master
echo -e "\n=== 5. Motores Master & AGI ==="
for engine in m82_supervisor.sh orch.py m82_master_dossier.py m82_api_server.py m82_fusion_engine.py m82_agi_quantum_audit.py m82_kronos_engine.py m82_refinitiv_realtime_bridge.py; do
  if ls $M82_ROOT/$engine $M82_ROOT/desks/$engine 2>/dev/null | grep -q .; then
    echo "[OK] $engine"
  else
    echo "[--] $engine (no encontrado)"
  fi
done
echo "════════════════════════════════════════════════════════════════════════"
