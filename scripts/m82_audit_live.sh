#!/data/data/com.termux/files/usr/bin/bash
while true; do
 clear
 echo "M82 LIVE AUDIT — CARACAS LIBRE ⊗ CHARALLAVE L4/L5 — MCM"
 echo "Firmware: M82_DOSSIER_MCM_TRANSICION_24OCT26 — MEIB Nashville"
 sqlite3 ~/M82/db/m82_database.db "PRAGMA wal_checkpoint(TRUNCATE); SELECT 'busy='||(SELECT busy FROM pragma_stats) UNION SELECT 'COUNT macro='||COUNT(*) FROM macro_dossier UNION SELECT 'COUNT stream='||COUNT(*) FROM m82_multi_stream;"
 echo ""
 sqlite3 ~/M82/db/m82_database.db "PRAGMA wal_checkpoint;"
 echo ""
 echo "Last 3 cards:"
 sqlite3 ~/M82/db/m82_database.db "SELECT datetime(ts), daemon_source, alpha_score FROM m82_multi_stream ORDER BY id DESC LIMIT 3;"
 sleep 2
done
