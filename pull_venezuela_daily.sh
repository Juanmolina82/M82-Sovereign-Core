#!/data/data/com.termux/files/usr/bin/bash
set -e
cd ~/M82
echo "=== M82 VENEZUELA BONDS DAILY PULL $(date) ==="
python3 pull_venezuela_bonds_full.py | tee -a logs/bonds.log
sqlite3 m82_database.db "PRAGMA busy_timeout=60000; PRAGMA journal_mode=WAL; PRAGMA wal_checkpoint(TRUNCATE);"
echo "WAL CLEAN 0/0/0 — $(date)"
