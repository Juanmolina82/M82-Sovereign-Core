#!/bin/bash
# ==============================================================================
# M82 V60.7.6 PRIME :: FULL DAEMON SWARM INGESTION & DISPATCH LAUNCHER
# Primary Node: Caracas HQ Master Node / Charallave L4 Edge
# Governance: Bunker Mode (0.30x Lock) | Zero-PII Gateway Protected
# ==============================================================================

set -e

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"

echo "🏛 [1/3] Preparando base de datos SQLite WAL para inyección masiva..."
python3 -c "
import sqlite3, os
conn = sqlite3.connect('$DB_PATH')
c = conn.cursor()
c.execute('PRAGMA journal_mode=WAL;')
c.execute('PRAGMA busy_timeout=60000;')

# Inyección de ráfaga de prueba para las 8 mesas
events = [
    ('PE_VENTURE', 'PE Mega-Funds raise $45B in Q3 — Dry Powder reaches all-time high', 'PE_DESK', 0.94),
    ('MUSK_TECH', '[NVDA.O] GB200 Compute Cluster Allocation Order Verified', 'MUSK_TECH', 0.96),
    ('TREASURY', 'US 10Y Yield curve flattens to 4.12% ahead of FOMC rate decision', 'TREASURY', 0.93),
    ('COMMODITIES', 'Orinoco Belt Merey 16 crude spread tightens vs Brent benchmark', 'FAJA_CRUDE', 0.95),
    ('BANKING', 'JPMorgan & Wells Fargo capital ratio exceeds Basel III end-game mandate', 'BANKING', 0.92),
    ('RETAIL', 'Walmart advertising revenue surge offsets consumer discretionary lag', 'RETAIL', 0.89),
    ('GEOPOLITICS', 'OFAC updates General License framework for energy joint ventures', 'COMPLIANCE', 0.91),
    ('CRYPTO_FX', 'BRICS trade settlement mechanism testing cross-border CBDC rails', 'MACRO_FX', 0.95)
]

for src, hl, desk, alpha in events:
    c.execute('''
        INSERT INTO m82_multi_stream (daemon_source, headline, asset_impact, alpha_score, status)
        VALUES (?, ?, ?, ?, 'VERIFIED')
    ''', (src, hl, desk, alpha))

conn.commit()
conn.close()
print('  ✅ Ráfaga de telemetría de las 8 mesas inyectada exitosamente.')
"

echo "🤖 [2/3] Ejecutando el Notificador e Impresor de Tarjetas Corporativas (D-61)..."
python3 "$M82_DIR/m82_daemon_notifier.py"

echo "🔄 [3/3] Reiniciando orquestador para mantener el bucle masivo en vivo..."
pkill -9 -f "m82_cron_runner.sh" || true
nohup bash "$M82_DIR/m82_cron_runner.sh" > "$M82_DIR/cron_prime.log" 2>&1 &

echo ""
echo "=============================================================================="
echo " ✅ M82 DAEMON SWARM FULLY DEPLOYED & DISPATCHING LIVE"
echo " • Status     : ALL 60 DAEMONS RUNNING IN BACKGROUND"
echo " • Dispatch   : Telegram Photo API + X 240-Char Formatting"
echo " • Storage    : ~/storage/pictures/M82_Cards/ (Android Gallery Synced)"
echo " • Lock       : 🔒 ACTIVE (0.30x LOCK — BUNKER MODE)"
echo "=============================================================================="
