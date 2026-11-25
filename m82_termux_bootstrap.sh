#!/usr/bin/env bash
set -e

echo "=================================================================="
echo "🛡️ M82 SOVEREIGN CORE :: TERMUX EDGE BOOTSTRAP (CHARALLAVE L4/L5)"
echo "🔒 GOBERNANZA: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK | NO TRADE"
echo "=================================================================="

# 1. Mantener CPU activa en Termux (evita Doze Mode de Android)
if command -v termux-wake-lock >/dev/null 2>&1; then
    termux-wake-lock
    echo "[OK] termux-wake-lock activado."
fi

mkdir -p "$HOME/M82/scripts" "$HOME/M82/logs" "$HOME/M82/docs"

# 2. Verificar/Inicializar SQLite3 en WAL Mode sin contencion
python3 - << 'EOF_DB_INIT'
import sqlite3, os

db_path = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(db_path, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA synchronous=NORMAL;")
conn.execute("PRAGMA busy_timeout=60000;")

conn.execute("""
CREATE TABLE IF NOT EXISTS macro_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    category TEXT,
    headline TEXT,
    risk_score REAL DEFAULT 0.0,
    m82_tag TEXT UNIQUE,
    sentiment REAL DEFAULT 0.0,
    metadata_json TEXT,
    alpha_score REAL DEFAULT 0.0,
    msi_index REAL DEFAULT 0.0,
    hash_sha256 TEXT,
    validated INTEGER DEFAULT 1,
    version INTEGER DEFAULT 1
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS m82_ledger_seals_v2 (
    seal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prev_hash TEXT,
    record_id INTEGER,
    operation TEXT,
    payload_hash TEXT,
    timestamp TEXT,
    node_id TEXT DEFAULT 'CHARALLAVE-L4L5-EDGE',
    version INTEGER DEFAULT 1
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_source TEXT,
    headline TEXT,
    status TEXT DEFAULT 'PENDING',
    alpha_score REAL DEFAULT 0.0,
    asset_impact TEXT,
    event_trigger TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    version INTEGER DEFAULT 1
)
""")

for tbl in ("macro_dossier", "m82_ledger_seals_v2", "m82_multi_stream"):
    cols = [c[1] for c in conn.execute(f"PRAGMA table_info({tbl})").fetchall()]
    if "version" not in cols:
        conn.execute(f"ALTER TABLE {tbl} ADD COLUMN version INTEGER DEFAULT 1;")

conn.commit()
conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
conn.close()
print("[OK] Base de datos SQLite3 verificada en WAL Mode (busy_timeout=60000).")
EOF_DB_INIT

# 3. Generar/Blindar Watchdog Singleton (m82_watchdog.sh)
cat << 'EOF_WD' > "$HOME/M82/m82_watchdog.sh"
#!/usr/bin/env bash
LOCKFILE="$HOME/M82/logs/m82_watchdog.pid"
mkdir -p "$HOME/M82/logs"

if [ -f "$LOCKFILE" ]; then
    OLD_PID=$(cat "$LOCKFILE" 2>/dev/null)
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null && [ "$OLD_PID" != "$$" ]; then exit 0 fi fi echo "$$" > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT INT TERM

while true; do
    if [ -f "$HOME/M82/scripts/m82_refinitiv_realtime_bridge.py" ]; then
        if ! pgrep -f "m82_refinitiv_realtime_bridge.py" >/dev/null 2>&1; then
            setsid nohup nice -n 5 python3 -u "$HOME/M82/scripts/m82_refinitiv_realtime_bridge.py" >> "$HOME/M82/logs/m82_refinitiv_realtime_bridge.log" 2>&1 < /dev/null &
        fi
    fi
    if [ -f "$HOME/M82/orch.py" ]; then
        if ! pgrep -f "orch.py" >/dev/null 2>&1; then
            setsid nohup python3 -u "$HOME/M82/orch.py" >> "$HOME/M82/logs/orch.log" 2>&1 < /dev/null &
        fi
    fi
    sleep 30
done
EOF_WD
chmod +x "$HOME/M82/m82_watchdog.sh"

# 4. Reiniciar limpio el Watchdog Singleton y verificar enjambre
pkill -f "m82_watchdog.sh" 2>/dev/null || true
sleep 1
setsid nohup bash "$HOME/M82/m82_watchdog.sh" >> "$HOME/M82/logs/watchdog.log" 2>&1 < /dev/null &
sleep 2

echo "=== [ESTADO DE PROCESOS ACTIVOS EN TERMUX] ==="
pgrep -af "m82_watchdog.sh|m82_refinitiv_realtime_bridge.py|orch.py|m82_master_dossier.py" || true
echo "[OK] Despliegue finalizado en Nodo Charallave L4/L5 Edge."
