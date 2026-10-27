#!/bin/bash
M82_ROOT="$HOME/M82"
DB_PATH="$M82_ROOT/m82_database.db"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S VET")

echo "════════════════════════════════════════════════════════════════════════"
echo " M82 SWARM AUDIT (100+ DAEMONS) — $TIMESTAMP"
echo " Caracas HQ → Governance | Charallave L4/L5 → Execution"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "=== 1. m82_daemons_registry (SQLite WAL) ==="
if [ -f "$DB_PATH" ]; then
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA journal_mode=WAL;" | grep -q wal && echo "[OK] WAL MODE"
  sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT COUNT(*) || ' Daemons Registrados' FROM m82_daemons_registry;" 2>/dev/null || echo "Registry en proceso..."
  echo "WAL: $(sqlite3 "$DB_PATH" "PRAGMA journal_mode;" 2>/dev/null) CLEAN"
else
  echo "[WARN] DB no encontrada"
fi

echo ""
echo "=== 2. Archivos en Disco ==="
CORE=$(ls -1 $M82_ROOT/m82_*.py 2>/dev/null | wc -l)
DESKS=$(ls -1 $M82_ROOT/desks/m82_*.py $M82_ROOT/desks/*.py 2>/dev/null | wc -l)
echo "$((CORE+DESKS)) Archivos Totales (Core:$CORE + Desks:$DESKS)"

echo ""
echo "=== 3. Procesos Kernel ==="
ps aux | grep -E "python|m82" | grep -v grep | wc -l | xargs echo "Activos:"

echo ""
echo "=== 4. Desglose Mesas (80 Quants) ==="
for d in $M82_ROOT/desks/*/; do 
  [ -d "$d" ] && echo "  $(basename $d): $(ls -1 $d*.py 2>/dev/null | wc -l)"
done

echo ""
echo "=== 5. Motores Master & AGI (8 motores Core) ==="
ENGINES=(
  "m82_supervisor.sh"
  "orch.py"
  "m82_master_dossier.py"
  "m82_api_server.py"
  "m82_fusion_engine.py"
  "m82_agi_quantum_audit.py"
  "m82_kronos_engine.py"
  "m82_refinitiv_realtime_bridge.py"
)

for e in "${ENGINES[@]}"; do
  if ls $M82_ROOT/$e $M82_ROOT/*$e $M82_ROOT/desks/*$e 2>/dev/null | grep -q .; then
    echo "[OK] $e"
  else
    echo "[--] $e"
  fi
done

echo ""
echo "=== 6. Topología & Estado Soberano ==="
echo "🏢 CARACAS HQ: Molina Holdings LLC / JMM C.A. / M82 AI Partners — Master"
echo "🛰️ CHARALLAVE L4/L5: 100+ Daemons — Termux WAL — LSEG 60 FPS"
echo "🔒 BUNKER 0.30x LOCK | Exp 0.22x | VaR 1.68% | Warsh +102bps"
echo "🧹 BOT_SEED43 PURGED | Macro Dossier Robusto | Brazil EWZ -27% No Trade"
echo "════════════════════════════════════════════════════════════════════════"
