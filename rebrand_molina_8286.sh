#!/usr/bin/env bash
set -e

M82_DIR="$HOME/M82"
SERVER_FILE="$M82_DIR/m82_unified_8286.py"
DB_PATH="$M82_DIR/m82_database.db"

# 1. Re-branding institucional en el servidor unificado (:8286)
if [ -f "$SERVER_FILE" ]; then
    sed -i 's/SOVEREIGN_CHARALLAVE_L4_L5/M82_CO2_MOLINA_HOLDINGS_L4_L5/g' "$SERVER_FILE"
    sed -i 's/CHARALLAVE L4\/L5/M82 \/ CO2 — MOLINA HOLDINGS LLC/g' "$SERVER_FILE"
    sed -i 's/NODO OPERATIVO/ENTIDAD & CORE OPERATIVO/g' "$SERVER_FILE"
    sed -i 's/M82 SOVEREIGN CORE v50 — UNIFIED HUB (:8286)/M82 \/ CO2 — MOLINA HOLDINGS LLC :: SOVEREIGN CORE (:8286)/g' "$SERVER_FILE"
    sed -i 's/M82 SOVEREIGN CORE :: UNIFIED QUANTUM HUB (:8286)/M82 \/ CO2 — MOLINA HOLDINGS LLC :: SOVEREIGN CORE (:8286)/g' "$SERVER_FILE"
fi

# 2. Saneamiento de etiquetas en SQLite3 (WAL Mode + busy_timeout=60000)
python3 - << 'PY_CLEAN'
import sqlite3, os

db_path = os.path.expanduser("~/M82/m82_database.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    cur.execute("""
        UPDATE m82_multi_stream
        SET daemon_source = 'M82_CO2_HOLDINGS_CORE'
        WHERE UPPER(daemon_source) LIKE '%CHARALLAVE%'
    """)
    cur.execute("""
        UPDATE m82_multi_stream
        SET headline = REPLACE(headline, 'CHARALLAVE_NODE', 'M82_CO2_MOLINA_HOLDINGS')
        WHERE headline LIKE '%CHARALLAVE%'
    """)
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.commit()
    conn.close()
PY_CLEAN

# 3. Reinicio limpio del servidor en :8286
pkill -f "m82_unified_8286.py" 2>/dev/null || true
sleep 1
nohup python3 "$SERVER_FILE" >> "$M82_DIR/hub_8286.log" 2>&1 &
sleep 2

curl -s http://127.0.0.1:8286/health | python3 -m json.tool
