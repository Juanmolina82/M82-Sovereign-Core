#!/data/data/com.termux/files/usr/bin/bash
DB=~/M82/m82_database.db
sqlite3 $DB "SELECT 'WEEKLY M82 DOSSIER '||date('now') as title; SELECT sector,COUNT(*),PRINTF('\$%.2fB',SUM(volume_notional)/1e9) FROM m82_all_sectors_telemetry GROUP BY sector ORDER BY SUM(volume_notional) DESC;" > ~/M82/logs/weekly_$(date +%Y-%W).log
python3 ~/M82/m82_master_dossier.py 2>/dev/null
bash ~/M82/scripts/m82_github_blindaje.sh
