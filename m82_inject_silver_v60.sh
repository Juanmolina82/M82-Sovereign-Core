#!/usr/bin/env bash
# ==============================================================================
# M82 SOVEREIGN CORE :: SILVER FUTURES (COMEX 1D) TECHNICAL VECTOR INJECTION
# Locus: Nodo Charallave L4/L5 Edge ⊗ Caracas HQ Central
# Authority: Chairman & CEO Juan M. Molina | Molina Holdings LLC
# Governance: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK (NO TRADE)
# ==============================================================================
set -euo pipefail

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;
PRAGMA synchronous=NORMAL;

INSERT OR IGNORE INTO macro_dossier (
    source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score, msi_index
) VALUES (
    'TRADINGVIEW_COMEX_1D',
    'METALS_LME_PRECIOUS',
    '[SILVER_COMEX_V60] Silver Futures 1D at $52.240 (-3.90%) below $56.705 neckline; Bear Flag targeting 400/MA ($46.005-$46.085) and Fib Ext Cluster ($37.840-$39.600) | BUNKER 0.30x LOCK',
    1.62,
    'BUNKER_HOLD_030X',
    -0.68,
    '{"ticker":"SI1!","exchange":"COMEX","timeframe":"1D","price":52.240,"broken_support":56.705,"ma_400":46.005,"ma_600":41.025,"fib_ext_cluster":[37.840,39.600],"ma_900":34.810,"governance":"BUNKER_030X_NO_TRADE"}',
    0.88,
    1500.0
);

INSERT OR IGNORE INTO m82_multi_stream (
    daemon_source, headline, status, alpha_score, asset_impact, event_trigger
) VALUES (
    'METALS_LME_DESK',
    '[SILVER 1D COMEX] $52.240 Bear Flag below $56.705 -> Watch Fib Ext Cluster $37.840-$39.600 (Custodia Pasiva 0.30x LOCK)',
    'VERIFIED',
    0.88,
    'METALS_SILVER_COMEX',
    'SILVER_BEAR_FLAG_V60'
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT id, source, category, m82_tag, risk_score, alpha_score, substr(headline, 1, 75) AS snippet
FROM macro_dossier ORDER BY id DESC LIMIT 2;
EOF_SQL

# Despacho opcional de tarjeta HUD si orch.py está disponible
if [ -f "$M82_DIR/orch.py" ]; then
    python3 "$M82_DIR/orch.py" --card M82_SILVER_COMEX_V60 --tag "SILVER 1D $52.240 | Bear Flag -> Fib Cluster $37.84-$39.60 | BUNKER 0.30x" 2>/dev/null || true
fi

echo "✅ VECTOR SILVER COMEX V60 SELLADO EN SQLITE WAL (0/0/0 CLEAN) // BUNKER 0.30x INTACTO"
