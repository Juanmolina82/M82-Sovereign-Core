#!/usr/bin/env bash
# M82 SWARM AUDIT - Anti-silencio, sin set -e
DB="$HOME/M82/m82_database.db"
DB_FAMILIA="$HOME/M82/sqlite/m82_familia.db"

echo "=============================================================================="
echo " M82 SWARM AUDIT :: CENSO 163 DAEMONS"
echo " Timestamp : $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo "=============================================================================="

echo ""
echo "1. PERSISTENCIA WAL:"
[ -f "$DB" ] && sqlite3 "$DB" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(TRUNCATE);" || echo "  DB principal NO EXISTE"

echo ""
echo "2. CENSO EN DB:"
sqlite3 "$DB" "SELECT '  Registrados: ' || count(*) FROM m82_daemons_registry;" 2>&1 || echo "  Tabla m82_daemons_registry NO EXISTE - Censo es por archivos, no por DB"

echo ""
echo "3. ARCHIVOS EN FILESYSTEM:"
CORE_FILES=$(ls -1 ~/M82/m82_*.py 2>/dev/null | wc -l)
DESK_FILES=$(ls -1 ~/M82/desks/*.py 2>/dev/null | wc -l)
DYNASTY_FILES=$(ls -1 ~/M82/scripts/m82_familia_*.py 2>/dev/null | wc -l)
echo "  Core: $CORE_FILES | Desks: $DESK_FILES | Dynasty: $DYNASTY_FILES | Total: $((CORE_FILES+DESK_FILES+DYNASTY_FILES))"

echo ""
echo "4. PROCESOS VIVOS EN KERNEL:"
ps aux | grep -E "python3|m82|orch|supervisor|familia" | grep -v grep | head -n 25
echo "  Total vivos: $(ps aux | grep -E "python3|m82|orch|supervisor|familia" | grep -v grep | wc -l)"

echo ""
echo "=============================================================================="
echo " GOBERNANZA: BUNKER MODE 0.30x LOCK | Exp ~0.22x | VaR 1.68% | Warsh +102.0 bps"
echo "=============================================================================="
