#!/bin/bash
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$HOME/M82_BACKUPS"
BUNDLE_NAME="M82_TOTAL_SHIELD_NIGHT_LOCK_${TIMESTAMP}"
TARGET_TAR="${BACKUP_DIR}/${BUNDLE_NAME}.tar.gz"
SYS_INFO="${HOME}/M82/system_state_${TIMESTAMP}.txt"

echo "=========================================================================="
echo "      M82 CHARALLAVE EDGE (L4) — TOTAL SHIELD & EXTRACTION ENGINE"
echo "=========================================================================="

mkdir -p "$BACKUP_DIR"

echo "[1/6] Sincronizando SQLite WAL Journal y verificando integridad..."
sqlite3 $HOME/M82/m82_database.db "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(FULL); PRAGMA integrity_check;"

echo "[2/6] Congelando instantánea de procesos, Daemons y entorno Termux..."
{
  echo "=== SNAPSHOT DE PROCESOS (PID 14423 & SWARM) ==="
  ps aux | grep -E "python|orch|sqlite3|termux" || true
  echo -e "\n=== CRONTAB Y TAREAS PROGRAMADAS ==="
  crontab -l 2>/dev/null || echo "No crontab active"
  echo -e "\n=== TABLA DE RED Y CONEXIONES SECTORIALES ==="
  ss -tulpn 2>/dev/null || netstat -tulpn 2>/dev/null || true
  echo -e "\n=== LTIMOS 50 REGISTROS DE ORCH.LOG ==="
  tail -n 50 $HOME/M82/orch.log 2>/dev/null || true
} > "$SYS_INFO"

echo "[3/6] Exportando Dumps SQL estructurados (Raw + Schema)..."
sqlite3 $HOME/M82/m82_database.db .dump > $HOME/M82/m82_database_full_dump_${TIMESTAMP}.sql

echo "[4/6] Empaquetando M82 + Entorno Termux + Dotfiles..."
tar -czvf "$TARGET_TAR" \
    -C $HOME \
    M82/ \
    .bashrc \
    .termux/ \
    2>/dev/null || \
tar -czvf "$TARGET_TAR" \
    -C $HOME \
    M82/

echo "[5/6] Generando Hash de Verificación Criptográfica (SHA-256)..."
sha256sum "$TARGET_TAR" > "${TARGET_TAR}.sha256"

echo "[6/6] Asentando el evento de blindaje en la Base de Datos..."
sqlite3 $HOME/M82/m82_database.db << SQL_EOF
PRAGMA busy_timeout=60000;
INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
  'SYSTEM_GOVERNANCE',
  '[TOTAL INFRASTRUCTURE EXPORTED] Complete Termux system + 60+ Daemons + WAL snapshot sealed in ${BUNDLE_NAME}.tar.gz',
  'COMPLETED',
  1.00,
  'SYSTEM_WIDE'
);
SQL_EOF

echo "=========================================================================="
echo "✅ INFRAESTRUCTURA M82 TOTALMENTE EXPULSADA, BLINDADA Y CERRADA:"
echo "📦 PAQUETE COMPLETO  : ${TARGET_TAR}"
echo "🔒 HASH SHA-256     : $(cat ${TARGET_TAR}.sha256 | cut -d' ' -f1)"
echo "📊 TAMAÑO DEL BUNDLE: $(du -sh ${TARGET_TAR} | cut -f1)"
echo "=========================================================================="
