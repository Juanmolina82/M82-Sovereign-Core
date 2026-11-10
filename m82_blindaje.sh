#!/bin/bash
set -e
cd ~/M82
python3 ~/M82/m82_mythos_guard.py
python3 ~/M82/check.py
cp ~/M82/m82_database.db ~/M82/m82_database.db.bak.$(date +%Y%m%d_%H%M)
cp ~/M82/app/data.json ~/M82/app/data.json.bak.$(date +%Y%m%d_%H%M)
ls -t ~/M82/*.bak.* | tail -n +6 | xargs -r rm --
echo "[BLINDAJE OK] Guard + Check + Backup."
