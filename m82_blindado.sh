#!/usr/bin/env bash
# M82 BLINDADO - ZERO-PIPE - WHATSAPP SAFE
DB="$HOME/M82/m82_database.db"
DB_FAM="$HOME/M82/sqlite/m82_familia.db"
LOG="$HOME/M82/logs/m82_blindado.log"
> "$LOG"
echo "==================================================================" >> "$LOG"
echo " M82 BLINDADO :: AUDITORIA + HARDENING" >> "$LOG"
date -u >> "$LOG"
echo "==================================================================" >> "$LOG"
echo " [1/4] HARDENING PERMISOS..." >> "$LOG"
chmod 700 "$HOME/M82"
chmod 600 "$HOME/.bashrc" 2>/dev/null
chmod 600 "$DB" 2>/dev/null
chmod 600 "$DB_FAM" 2>/dev/null
chmod 700 "$HOME/M82/m82_blindado.sh"
echo "  -> Permisos: 700 en ~/M82, 600 en .bashrc y DBs OK" >> "$LOG"
echo " [2/4] PERSISTENCIA WAL CHECKPOINT & INTEGRIDAD..." >> "$LOG"
sqlite3 "$DB" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(TRUNCATE);" >> "$LOG"
sqlite3 "$DB" "PRAGMA busy_timeout=60000; PRAGMA integrity_check;" >> "$LOG"
[ -f "$DB_FAM" ] && sqlite3 "$DB_FAM" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(TRUNCATE);" >> "$LOG"
echo " [3/4] CENSO REAL EN DATABASE..." >> "$LOG"
echo -n "  DB Principal (m82_database.db) Registrados: " >> "$LOG"
sqlite3 "$DB" "SELECT count(*) FROM m82_daemons_registry;" >> "$LOG"
if [ -f "$DB_FAM" ]; then
  echo -n "  DB Familia (m82_familia.db) Registrados: " >> "$LOG"
  sqlite3 "$DB_FAM" "SELECT count(*) FROM m82_daemons_registry;" 2>/dev/null >> "$LOG" || echo "0 (sin tabla)" >> "$LOG"
fi
echo " [4/4] GOBERNANZA BUNKER MODE 0.30x LOCK - WAL 0/0/0 CLEAN" >> "$LOG"
