#!/usr/bin/env bash
set -e

echo "=================================================="
echo "⚙️ ACTUALIZANDO DAEMONS EN M82 (NVIDIA & CITADEL)"
echo "=================================================="

BASE_DIR="$HOME/M82"
DAEMONS_DIR="$BASE_DIR/daemons"
mkdir -p "$DAEMONS_DIR"

# ----------------------------------------------------
# 1. DAEMON: NVIDIA INSIDER TRANSACTIONS
# ----------------------------------------------------
cat << 'PYEOF' > "$DAEMONS_DIR/daemon_nvidia_insiders.py"
#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "NVDA_INSIDER", "headline": "NVDA: Mark Stevens sells indirect shares via Form 4 filings"},
    {"source": "NVDA_INSIDER", "headline": "NVDA: Colette Kress executes scheduled option exercise and Open Market sale"},
    {"source": "NVDA_INSIDER", "headline": "NVDA: Insider Model shows Net Selling pressure over last 12 months"},
    {"source": "NVDA_CORPORATE", "headline": "Nvidia sets biggest-ever buyback plan amidst AI chip market competition"}
]

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    count = 0
    for item in feeds:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["headline"], now))
        if c.rowcount > 0: count += 1
        
    conn.commit()
    conn.close()
    print(f"🟢 [DAEMON NVDA]: Inyectadas {count} alertas de insiders.")

if __name__ == "__main__":
    run()
PYEOF

# ----------------------------------------------------
# 2. DAEMON: CITADEL INSTITUTIONAL TRACKER
# ----------------------------------------------------
cat << 'PYEOF' > "$DAEMONS_DIR/daemon_citadel_tracker.py"
#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "CITADEL_DESK", "headline": "CITADEL ENTERPRISE AMERICAS: Directory scan mapped (Data Operations / Multi-Asset)"},
    {"source": "CITADEL_DESK", "headline": "CITADEL SECURITIES: Institutional holdings update registered"}
]

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    count = 0
    for item in feeds:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["headline"], now))
        if c.rowcount > 0: count += 1
        
    conn.commit()
    conn.close()
    print(f"🏢 [DAEMON CITADEL]: Inyectadas {count} trazas institucionales.")

if __name__ == "__main__":
    run()
PYEOF

chmod +x "$DAEMONS_DIR"/*.py

# ----------------------------------------------------
# EJECUCIÓN Y PROCESAMIENTO GENERAL
# ----------------------------------------------------
echo "⚡ Ejecutando Daemons integrados..."
python3 "$DAEMONS_DIR/daemon_nvidia_insiders.py"
python3 "$DAEMONS_DIR/daemon_citadel_tracker.py"
python3 "$DAEMONS_DIR/daemon_refinitiv_world.py"
python3 "$DAEMONS_DIR/daemon_ve_politics.py"
python3 "$DAEMONS_DIR/daemon_macro_yields.py"

echo "🎨 Ejecutando Motor Master de Renderizado..."
python3 "$BASE_DIR/m82_engine_master.py"

echo "=================================================="
echo "✅ TODOS LOS DAEMONS INTEGRADOS CORRECTAMENTE"
echo "=================================================="
