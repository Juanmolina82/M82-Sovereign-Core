#!/data/data/com.termux/files/usr/bin/bash
python3 ~/M82/m82_master_dossier.py --monthly 2>/dev/null
sqlite3 ~/M82/m82_database.db "SELECT strftime('%Y-%m',timestamp) as mes, sector, SUM(volume_notional)/1e9 as B, COUNT(*) FROM m82_all_sectors_telemetry GROUP BY mes,sector ORDER BY mes DESC, B DESC;" > ~/M82/logs/monthly_$(date +%Y-%m).log
bash ~/M82/scripts/m82_github_blindaje.sh
~/M82/scripts/ntfy.sh "📊 M82 MONTHLY DOSSIER $(date +%Y-%m) — $20.12B total — Warriors Three — BUNKER 0.30x — MM82 blindado GitHub"
