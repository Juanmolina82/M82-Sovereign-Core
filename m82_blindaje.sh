#!/bin/bash
set -e
cd ~/M82
echo "[BLINDAJE] Verificando CORE..."
python3 ~/M82/check.py
echo "[BLINDAJE] Backup SQLite WAL..."
cp ~/M82/m82_database.db ~/M82/m82_database.db.bak.$(date +%Y%m%d_%H%M)
cp ~/M82/app/data.json ~/M82/app/data.json.bak.$(date +%Y%m%d_%H%M)
echo "[BLINDAJE] Limpieza backups viejos - quedan ultimos 5..."
ls -t ~/M82/*.bak.* | tail -n +6 | xargs -r rm --
echo "[BLINDAJE OK] Backup + Check completos."
