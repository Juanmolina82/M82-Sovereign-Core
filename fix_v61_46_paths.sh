#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

M82_DIR="$HOME/M82"
SCRIPTS_DIR="$M82_DIR/scripts"
DB_PATH="$M82_DIR/m82_database.db"

mkdir -p "$SCRIPTS_DIR"
cd "$M82_DIR"

# 1. Crear el script físico m82_sovereign_core.sh en ~/M82/scripts/
cat << 'EOF_CORE' > "$SCRIPTS_DIR/m82_sovereign_core.sh"
#!/data/data/com.termux/files/usr/bin/bash
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ M82 SOVEREIGN CORE v61.0.46 :: MORGAN x M82 :: BANKS = NUMEROS ┃
# ┃ 5849 SIGLO 59 :: AÑO 18/19 LUNA MENGUANTE :: BUNKER 0.30x LOCK ┃
# ┃ OPERATOR D-34 :: PADRE 8 FINAL :: WAL 0/0/0 CLEAN              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
set -euo pipefail

DB="$HOME/M82/m82_database.db"
RATIO_TTF_HH=11.8
BUNKER_LOCK=0.30
BASE_TRUST=444
SIGLO=59
ANO_HEBREO=5849
ANO_METONICO=18
CICLO_METONICO=19

init_ledger(){
  sqlite3 "$DB" <<SQL
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;
CREATE TABLE IF NOT EXISTS m82_ledger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT DEFAULT (datetime('now','localtime')),
  siglo INTEGER,
  ano_hebreo INTEGER,
  ano_metonic TEXT,
  ratio REAL,
  bunker REAL,
  base INTEGER,
  tipo TEXT,
  nota TEXT,
  hash TEXT
);
SQL
  sqlite3 "$DB" "PRAGMA wal_checkpoint(TRUNCATE);"
}

case "${1:-status}" in
  init) init_ledger ;;
  *)
    echo "M82 SOVEREIGN CORE v61.0.46 :: OPERATOR D-34 :: WAL CLEAN"
    ;;
esac
EOF_CORE

chmod +x "$SCRIPTS_DIR/m82_sovereign_core.sh"

# 2. Ingesta atómica de la tag v61.0.46 en ~/M82/m82_database.db
python3 -c "
import sqlite3, os, json
from datetime import datetime, timezone

db = os.path.expanduser('~/M82/m82_database.db')
conn = sqlite3.connect(db, timeout=30)
conn.execute('PRAGMA journal_mode=WAL;')
conn.execute('PRAGMA busy_timeout=60000;')
cur = conn.cursor()

headline = '[M82 SOVEREIGN CORE v61.0.46] Morgan x M82 Banks = Numeros -- 5849 Siglo 59 Metonico 18/19 -- Ratio TTF/HH 11.8x -- Bunker 0.30x Lock -- Base 444 -- WAL 0/0/0 Clean'
tag = 'v61.0.46-MORGAN-M82-BANCO-SOBERANO-5849-RATIO-11.8x-BUNKER-0.30x-BASE-444'

meta = {
    'version': 'v61.0.46',
    'tag': tag,
    'ratio_ttf_hh': 11.8,
    'bunker_lock': 0.30,
    'operator': 'SECURE OPERATOR D-34',
    'node': 'SOVEREIGN EDGE CORE',
    'timestamp': datetime.now(timezone.utc).isoformat()
}

cur.execute('''
    INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('M82_SOVEREIGN_SCRIPT', 'GOVERNANCE_LEDGER_RATIO', ?, 1.00, ?, 0.99, ?, 'v61.0.46', 'SOVEREIGN_EDGE_CORE')
''', (headline, tag, json.dumps(meta)))

conn.commit()
cur.execute('PRAGMA wal_checkpoint(TRUNCATE);')
conn.close()
print('🔒 M82 v61.0.46 ASENTADO CORRECTAMENTE EN ~/M82/m82_database.db')
"

# 3. Verificación de archivo y registro en BBDD
echo "=== VERIFICACIÓN DE ARCHIVO FISICO ==="
ls -lh "$SCRIPTS_DIR/m82_sovereign_core.sh"

echo "=== VERIFICACIÓN EN BBDD MACRO_DOSSIER ==="
sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; SELECT id, m82_tag, ingestion_node FROM macro_dossier WHERE m82_tag LIKE 'v61.0.46%';"

# 4. Sello en Git
git add scripts/m82_sovereign_core.sh 2>/dev/null || git add .
git commit -m "v61.0.46: MORGAN x M82 BANCO SOBERANO 5849 RATIO 11.8x BUNKER 0.30x BASE 444" 2>/dev/null || echo "Commit registrado / Sin cambios pendientes."

echo "🟢 [FIX TOTAL COMPLETADO] Archivos y registros alineados en ~/M82/."
