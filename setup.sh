#!/data/data/com.termux/files/usr/bin/bash
# M82 QUANTUM TERMINAL — SETUP MAESTRO
# HQ: CARACAS — SOVEREIGN CORE (BUNKER MODE 0.30x LOCK)
# EDGE: CHARALLAVE L4/L5 — Termux Sovereign Edge
# Firmware: M82_DOSSIER_ROBUSTO_24OCT26 | PID 4692

set -e

echo "┌──────────────────────────────────────────────────┐"
echo "│ M82 SETUP — CARACAS HQ ⊗ CHARALLAVE EDGE        │"
echo "│ Chairman: Juan M. Molina — PID 4692             │"
echo "└──────────────────────────────────────────────────┘"

# 1. Base Termux & Herramientas
pkg update -y && pkg upgrade -y
pkg install -y python termux-api sqlite cronie nodejs-lts git curl gh

# 2. Estructura M82
mkdir -p ~/M82/{logs,cards,db,pwa,repo,scripts}
cd ~/M82

# 3. DB WAL con Topología Corregida (CARACAS HQ ⊗ CHARALLAVE EDGE)
cat > ~/M82/init_db.py << 'PY'
import sqlite3, os
db_path = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
conn.execute("""
CREATE TABLE IF NOT EXISTS m82_topology (
 id INTEGER PRIMARY KEY,
 hq TEXT DEFAULT 'CARACAS — SOVEREIGN CORE',
 edge TEXT DEFAULT 'CHARALLAVE L4/L5 — Sovereign Edge',
 bunker_lock REAL DEFAULT 0.30,
 exposure REAL DEFAULT 0.22,
 var REAL DEFAULT 1.68,
 warsh_spread REAL DEFAULT 102.0,
 last_sync DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")
conn.execute("INSERT OR REPLACE INTO m82_topology (id, hq, edge) VALUES (1, 'CARACAS — SOVEREIGN CORE', 'CHARALLAVE L4/L5 — Sovereign Edge')")

# Asegurar esquemas macro_dossier y m82_multi_stream
conn.execute("""
CREATE TABLE IF NOT EXISTS macro_dossier (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 source TEXT, category TEXT, headline TEXT, risk_score REAL,
 m82_tag TEXT, alpha_score REAL DEFAULT 0.0, created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS m82_multi_stream (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 daemon_source TEXT, headline TEXT UNIQUE, status TEXT DEFAULT 'PENDING',
 alpha_score REAL DEFAULT 0.0, asset_impact TEXT, event_trigger TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()
conn.close()
print("✅ DB WAL OK — HQ CARACAS ⊗ Edge Charallave — busy_timeout=60000ms")
PY
python3 ~/M82/init_db.py

# 4. Orquestador con Firma Institucional Correcta
cat > ~/M82/orch.py << 'PY'
import time, argparse, sqlite3, datetime, os

parser = argparse.ArgumentParser()
parser.add_argument('--card', default='IRAN_HORMUZ_RISK_NABEP_HEDGE')
parser.add_argument('--cadence', type=int, default=60)
parser.add_argument('--alpha-threshold', type=float, default=0.85)
parser.add_argument('--bunker-lock', type=float, default=0.30)
args = parser.parse_args()

CARD = args.card
HQ = "CARACAS — SOVEREIGN CORE"
EDGE = "CHARALLAVE L4/L5 — Sovereign Edge"
SIGNATURE = f"M82_DOSSIER_ROBUSTO_24OCT26 — HQ {HQ} — Edge {EDGE}"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

alpha = 0.99 if "IRAN_HORMUZ" in CARD else 0.70
if alpha < args.alpha_threshold:
    print(f"[M82 UNIFIED DISPATCHER] Anti-Daneka Filter Active - DISCARDED Alpha {alpha} < {args.alpha_threshold}")
else:
    log = f"{datetime.datetime.now()} | {SIGNATURE} | {CARD} | Alpha {alpha} | BUNKER {args.bunker_lock}x | PID4692"
    print(f"[M82 DISPATCH] {log}")
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA busy_timeout=60000;")
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES (?, ?, 'PROCESSED', ?, 'BRENT_MEREY_QATAR_BID_LOOP', ?)",
                     ("M82_ROBUST_MACRO_PID4692", SIGNATURE + " | " + CARD, alpha, CARD))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")
    
    with open(os.path.expanduser("~/M82/logs/pid4692.log"), "a") as f:
        f.write(log + "\n")
PY

# 5. Boot Script y Auto-start
cat > ~/M82/boot.sh << 'SH'
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
echo "⚡ M82 BOOT — CARACAS HQ ⊗ Edge Charallave"
cd ~/M82
pkill -f "orch.py" 2>/dev/null || true
nohup python3 ~/M82/orch.py --card IRAN_HORMUZ_RISK_NABEP_HEDGE --cadence 60 --alpha-threshold 0.85 --bunker-lock 0.30 > ~/M82/logs/orch.log 2>&1 &
echo "🟢 M82 SERVICIOS ACTIVOS — HQ CARACAS ⊗ Charallave L4/L5 — BUNKER 0.30x LOCK"
SH
chmod +x ~/M82/boot.sh ~/M82/setup.sh

echo "✅ SETUP COMPLETADO — HQ CARACAS ⊗ Edge Charallave"
