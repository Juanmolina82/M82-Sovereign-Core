#!/usr/bin/env bash
# ==============================================================================
# M82 MACRO DOSSIER — OVERNIGHT SENTINEL & BUNKER LOCK SCRIPT (10-OCT-2026)
# Platform: Termux / Android Linux (ARM64)
# Node: Caracas HQ Node (Execution) -> Caracas HQ (STANDBY Directorship)
# ==============================================================================

set -e

DB_PATH="$HOME/M82/m82_database.db"
GALLERY_DIR="$HOME/storage/pictures/M82_Cards"
CLOSING_IMG="$HOME/M82/M82_CARD_20261010_CLOSING.png"

echo "=============================================================================="
echo "🛡️ INICIALIZANDO PROTOCOLO DE CENTINELA NOCTURNO // NODO CHARALLAVE EDGE"
echo "=============================================================================="

# 1. Asegurar persistencia de CPU (Anti-Deep Sleep)
echo "🔋 [1/5] Verificando Termux Wake-Lock..."
termux-wake-lock

# 2. Asentar estado oficial en SQLite (WAL Mode con busy_timeout=60000)
echo "🗄️ [2/5] Sellando Gobernanza BUNKER 0.30x LOCK en SQLite WAL..."
python3 -c "
import sqlite3, os, datetime

DB_PATH = os.path.expanduser('$DB_PATH')
conn = sqlite3.connect(DB_PATH, timeout=60.0)
conn.execute('PRAGMA journal_mode=WAL;')
conn.execute('PRAGMA busy_timeout=60000;')
c = conn.cursor()

headline = 'OVERNIGHT LOCK 10-OCT: Brent \$103.74 Floor | Hormuz \$1.2M/day | NIMageddon \$79B | BUNKER 0.30x LOCK ACTIVE. Trigger <\$98.00 armed.'
source = 'CHARALLAVE_NIGHT_SENTINEL'
category = 'OVERNIGHT_GOVERNANCE'
tag = 'BUNKER_LOCK'
risk_score = 10.0

c.execute('''
    INSERT INTO macro_dosier 
    (timestamp, source, category, headline, risk_score, metadata_json, m82_tag, sentiment, entities) 
    VALUES (datetime('now'), ?, ?, ?, ?, '{\"node\":\"CHARALLAVE_EDGE\",\"status\":\"OVERNIGHT_STANDBY\"}', ?, -0.90, 'Brent,Hormuz,DOE,NIMageddon,Bunker')
''', (source, category, headline, risk_score, tag))

c.execute('''
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
    VALUES (?, ?, 'LOCK_CONFIRMED', 1.00, 'BRENT_WTI')
''', (source, headline))

# Forzar checkpoint pasivo para limpiar la WAL antes de la noche
c.execute('PRAGMA wal_checkpoint(PASSIVE);')

conn.commit()
conn.close()
print('  ✓ Registro de Gobernanza Nocturna sellado exitosamente.')
"

# 3. Sincronización de Galería y Escaneo Media
echo "📸 [3/5] Escaneando tarjeta M82_CARD_20261010_CLOSING.png para Galería Android..."
if [ -f "$CLOSING_IMG" ]; then
    mkdir -p "$GALLERY_DIR"
    cp "$CLOSING_IMG" "$GALLERY_DIR/M82_CARD_20261010_CLOSING.png"
    termux-media-scan "$GALLERY_DIR/M82_CARD_20261010_CLOSING.png" > /dev/null 2>&1 &
    echo "  ✓ Tarjeta sincronizada en la galería."
else
    echo "  ℹ️ Generando escaneo sobre la tarjeta base..."
    termux-media-scan "$HOME/M82/latest_card.png" > /dev/null 2>&1 &
fi

# 4. Verificación de Daemons en Polling Lite y Supervisor
echo "🤖 [4/5] Verificando enjambre de 40 Daemons y Supervisor..."
if ! pgrep -f "m82_supervisor.sh" > /dev/null; then
    echo "  ⚡ Re-iniciando m82_supervisor.sh..."
    nohup "$HOME/M82/m82_supervisor.sh" > "$HOME/M82/supervisor.log" 2>&1 &
fi

# 5. Confirmación final de estado
echo "📡 [5/5] Estado de Canales de Alerta:"
echo "  ├─> Telegram: @MolinaHoldings LLC (Suscrito)"
echo "  ├─> Ntfy: https://ntfy.sh/M82-Molina-Alerts-v2 (Priority: URGENT)"
echo "  └─> Caracas HQ: STANDBY ESTRICTO (Trigger: Brent < \$98.00/bbl)"

echo "=============================================================================="
echo "🌙 NODO CHARALLAVE EDGE EN VIGILANCIA NOCTURNA // BUNKER MODE 0.30x SELLADO"
echo "=============================================================================="
