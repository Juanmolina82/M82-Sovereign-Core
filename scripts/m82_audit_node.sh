#!/data/data/com.termux/files/usr/bin/bash
DB="$HOME/M82/m82_database.db"
echo "========================================================="
echo " 🏛️ M82 SOVEREIGN NODE AUDIT :: $(date)"
echo "========================================================="
echo "🔍 Integridad SQLite: $(sqlite3 "$DB" "PRAGMA integrity_check;")"
echo "📊 Eventos Totales: $(sqlite3 "$DB" "SELECT COUNT(*) FROM m82_multi_stream;")"
echo "⚡ Procesos Activos: $(ps aux | grep -E "python3|m82" | grep -v grep | wc -l)"
API=$(curl -s http://127.0.0.1:8083/health | grep -o '"status":"ACTIVE"')
if [ -n "$API" ]; then echo "🌐 API Server (:8083): 🟢 ONLINE"; else echo "🌐 API Server (:8083): ⚠️ OFFLINE"; fi
echo "========================================================="
echo "🔒 GOVERNANCE: CUSTODIA_PASIVA_0.30X_LOCK APPROVED"
echo "========================================================="
