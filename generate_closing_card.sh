#!/usr/bin/env bash
# ==============================================================================
# M82 MACRO DOSSIER — DAILY DOSSIER CLOSING CARD GENERATOR (FIXED TIMEOUT)
# Platform: Termux / Android Linux
# Node: Caracas HQ Node -> Caracas HQ
# ==============================================================================

set -e

DB_PATH="$HOME/M82/m82_database.db"
BOT_SCRIPT="$HOME/M82/m82_telegram_bot.py"

echo "🗄️ [1/3] Liberando bloqueos WAL e inyectando lectura de cierre..."

python3 -c "
import sqlite3, os

DB_PATH = os.path.expanduser('$DB_PATH')

# Conexión con timeout robusto de 60 segundos
conn = sqlite3.connect(DB_PATH, timeout=60.0)
conn.execute('PRAGMA journal_mode=WAL;')
conn.execute('PRAGMA busy_timeout=60000;')

c = conn.cursor()

headline = 'DAILY DOSSIER CLOSING 10-OCT: Hormuz \$1.2M/day freight | SPR 4M Isaias Exchange | NIMageddon \$79B Savings Repricing | Brent \$103.74. BUNKER 0.30x LOCK CONFIRMED.'
source = 'CARACAS_HQ_DIRECTIVE'
category = 'DAILY_DOSSIER_CLOSING'
tag = 'DOSSIER_CLOSING'
risk_score = 9.9

c.execute('''
    INSERT INTO macro_dosier 
    (timestamp, source, category, headline, risk_score, metadata_json, m82_tag, sentiment, entities) 
    VALUES (datetime('now'), ?, ?, ?, ?, '{\"node\":\"CHARALLAVE_EDGE\",\"dossier_date\":\"2026-10-10\"}', ?, -0.85, 'Hormuz,DOE,SPR,JPM,BofA,Brent')
''', (source, category, headline, risk_score, tag))

c.execute('''
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
    VALUES (?, ?, 'PENDING', 0.95, 'BRENT_WTI')
''', (source, headline))

conn.commit()
conn.close()
print('  ✓ Registro de cierre inyectado con éxito (WAL Timeout 60s).')
"

echo "🎨 [2/3] Generando tarjeta Cyberpunk HUD (1000x1250 px)..."
if [ -f "$BOT_SCRIPT" ]; then
    python3 "$BOT_SCRIPT"
else
    echo "❌ Error: No se encontró $BOT_SCRIPT"
    exit 1
fi

echo "=============================================================================="
echo "🎯 DAILY DOSSIER CARD (10-OCT) GENERADO Y TRANSMITIDO CON ÉXITO"
echo "=============================================================================="
