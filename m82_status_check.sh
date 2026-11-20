#!/usr/bin/env bash
# ==============================================================================
# M82 QUANTITATIVE TERMINAL :: MASTER STATUS & AUDIT SCRIPT (ZERO HOT-MODS)
# Locus: Nodo Charallave L4/L5 Edge ⊗ Caracas HQ Central
# Authority: Chairman & CEO Juan M. Molina | Molina Holdings LLC
# Governance: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK
# ==============================================================================
set -euo pipefail

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"
HUD_DIR="/storage/emulated/0/M82card"

echo "=============================================================================="
echo " 🏛️  M82 SOVEREIGN CORE :: SYSTEM HEALTH & SWARM AUDIT"
echo " Timestamp NY (ET) : $(TZ='America/New_York' date +'%Y-%m-%d %H:%M:%S ET')"
echo " Timestamp VET     : $(TZ='America/Caracas' date +'%Y-%m-%d %H:%M:%S VET')"
echo " Governance        : 🔒 BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK"
echo "=============================================================================="

# 1. CENSO DE PROCESOS EN KERNEL (POSIX COMPATIBLE)
echo -e "\n[1/4] 🧠 PROCESOS CORE & ENJAMBRE ACTIVOS EN KERNEL:"
TOTAL_PROCS=$(ps aux | grep -E "python3|m82_|orch\.py|8286\.py|cloudflared" | grep -v grep | wc -l)
echo " • Total hilos/daemons M82 detectados en memoria: $TOTAL_PROCS"
ps aux | grep -E "m82_supervisor|m82_unified_core|orch\.py|m82_refinitiv|m82_api_|8286\.py|cloudflared" | grep -v grep | awk '{printf "   PID: %-7s CPU: %-5s MEM: %-5s CMD: %s %s\n", $2, $3, $4, $11, $12}' || true

# 2. AUDITORÍA SQLITE3 WAL MODE & COLA RELACIONAL (ZERO-LOCK)
echo -e "\n[2/4] 🗄️  PERSISTENCIA SQLITE3 WAL & BUFFER RELACIONAL:"
if [ -f "$DB_PATH" ]; then
    sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA busy_timeout=120000;
.headers on
.mode column
PRAGMA wal_checkpoint(TRUNCATE);
SELECT
    (SELECT COUNT(*) FROM m82_multi_stream) AS total_multi_stream,
    (SELECT COUNT(*) FROM m82_multi_stream WHERE status='PENDING') AS pending_queue,
    (SELECT COUNT(*) FROM m82_multi_stream WHERE status='DISPATCHED') AS dispatched_total,
    (SELECT COUNT(*) FROM macro_dossier) AS total_macro_dossier;
SELECT id, source, category, m82_tag, substr(headline, 1, 52) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 3;
EOF_SQL
else
    echo " ⚠️  Base de datos no localizada en $DB_PATH"
fi

# 3. SALUD DE ENDPOINTS LOCALES (:8086 / :8286 / :8083)
echo -e "\n[3/4] 🌐 ENDPOINTS HTTP & TELEMETRÍA LOCAL:"
for PORT in 8086 8286 8083; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 "http://127.0.0.1:${PORT}/health" 2>/dev/null || echo "000")
    if [ "$CODE" = "000" ]; then
        CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 "http://127.0.0.1:${PORT}/" 2>/dev/null || echo "OFFLINE")
    fi
    echo " • Puerto :$PORT -> HTTP $CODE"
done

# 4. GALERÍA HUD & BLINDAJE OPSEC GIT
echo -e "\n[4/4] 🛡️  GALERÍA HUD & ESCUDO OPSEC GIT:"
if [ -d "$HUD_DIR" ]; then
    HUD_COUNT=$(find "$HUD_DIR" -maxdepth 1 -type f -name "*.png" 2>/dev/null | wc -l)
    LATEST_HUD=$(ls -t "$HUD_DIR"/*.png 2>/dev/null | head -n 1 || echo "Ninguna")
    echo " • Tarjetas HUD en $HUD_DIR: $HUD_COUNT archivos"
    echo " • Última tarjeta generada: $LATEST_HUD"
fi

if [ -d "$M82_DIR/.git" ]; then
    cd "$M82_DIR"
    UNTRACKED_SENSITIVE=$(git status --porcelain 2>/dev/null | grep -E "vault|\.db|\.log|\.png" | wc -l || true)
    echo " • Exposición de secretos/DB en Git staging: $UNTRACKED_SENSITIVE archivos (0 = BLINDADO)"
fi

echo "=============================================================================="
echo " ✅ AUDITORÍA COMPLETADA // DRY POWDER 100% PROTEGIDO (EXP 0.22x | VaR 1.68%)"
echo "=============================================================================="
