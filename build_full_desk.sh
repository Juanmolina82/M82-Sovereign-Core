#!/usr/bin/env bash
set -e
M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"

echo "⚡ [1/3] Verificando esquemas y tablas en la Base de Datos WAL..."
sqlite3 "$DB_PATH" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;"
python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_PATH')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS m82_multi_stream (id INTEGER PRIMARY KEY AUTOINCREMENT, daemon_source TEXT, headline TEXT UNIQUE, status TEXT DEFAULT 'PENDING', alpha_score REAL DEFAULT 0.0, asset_impact TEXT DEFAULT 'MACRO', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS price_ticks (asset TEXT PRIMARY KEY, bid REAL, ask REAL, last_price REAL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, stream_id INTEGER, asset TEXT, side TEXT, order_type TEXT DEFAULT 'MARKET', qty REAL, limit_price REAL, fill_price REAL, slippage REAL, status TEXT DEFAULT 'PENDING', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS positions (asset TEXT PRIMARY KEY, current_qty REAL DEFAULT 0.0, avg_entry_price REAL DEFAULT 0.0, unrealized_pnl REAL DEFAULT 0.0, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()
conn.close()
"

echo "🛡️ [2/3] Sincronizando Supervisor Guardián..."
cat << 'EOF_SUP' > "$M82_DIR/m82_supervisor.sh"
#!/usr/bin/env bash
cd ~/M82
DAEMONS=("m82_master_dossier.py" "price_feeder.py" "orch.py" "execution_engine.py")
while true; do
    for script in "${DAEMONS[@]}"; do
        if ! pgrep -f "$script" > /dev/null; then
            nohup python3 -u "$script" > "${script%.py}.log" 2>&1 &
            sleep 1
        fi
    done
    sleep 15
done
EOF_SUP

chmod +x "$M82_DIR"/*.py "$M82_DIR"/m82_supervisor.sh

echo "🚀 [3/3] Reiniciando la Mesa M82 Macro Dossier..."
pkill -9 -f "python3" || true
nohup "$M82_DIR/m82_supervisor.sh" > "$M82_DIR/supervisor.log" 2>&1 &
echo "🔥 MESA DE DINERO MACRO DOSSIER CONSOLIDADA Y OPERATIVA AL 100%"
