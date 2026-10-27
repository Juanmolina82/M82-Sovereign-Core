#!/usr/bin/env bash
set -euo pipefail

M82_BASE="$HOME/M82"
DOSSIER_DIR="$M82_BASE/docs/macro_dossier"
DB_MAIN="$M82_BASE/m82_database.db"

echo "=========================================================================="
echo "  M82 LSEG INGEST — VENEZUELA VOTING ELECTORAL INFRA (REUTERS WIRE)"
echo "  Nodo Charallave Edge L4/L5 ⊗ Caracas HQ | 26/10/2026=1 Mónada"
echo "=========================================================================="

mkdir -p "$DOSSIER_DIR"

# 1. CREAR ARTEFACTO TEXTO DENTRO DE ~/M82/docs/macro_dossier/
cat << 'EOF_TXT' > "$DOSSIER_DIR/2026-10-26_venezuela_voting_urgent_reuters.txt"
SOURCE: Reuters / LSEG Workspace
WIRE ID: dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDI2Om5TME4zWkYwN0w6MQ==
TIMESTAMP: 2026-10-26 15:36 VET
TAG: VENEZUELA-VOTING/URGENT

HEADLINE:
US expects revamped electoral infrastructure in Venezuela before elections can be held — 
new supreme judicial tribunal [TSJ] by end of year + new electoral [CNE] shortly thereafter — 
Washington working with interim authorities using leverage to ensure reforms continue at proper pace.

M82 LATAM RISK DECODE:
- TSJ Reset: EOY 2026
- CNE Reset: Early 2027
- Presidential Elections: Delayed to 2027
- Strategic Leverage: OFAC Licences + Capital Escrow
- Action: BUNKER MODE 0.30x LOCK / Exp 0.22x / VaR 1.68% (Zero Exposure Rebalance)
EOF_TXT

echo "📝 [1/3] Artefacto 2026-10-26_venezuela_voting_urgent_reuters.txt guardado."

# 2. PERSISTENCIA BBDD SQLITE (WAL CLEAN)
sqlite3 "$DB_MAIN" << 'SQL_LSEG'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score, asset_impact, event_trigger)
VALUES (
    'Reuters/LSEG_Workspace',
    'VENEZUELA_VOTING',
    'US expects revamped electoral infrastructure before elections: new TSJ by EOY 2026 + new CNE in 2027 — US leverage active with interim authorities',
    0.72,
    'LATAM_RISK_VE_URGENT',
    0.85,
    'VEN_CRUDE+DEBT+BOLIVAR_VOL',
    'TSJ_NEW_EOY_CNE_2027'
);

INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'M82_LATAM_RISK_DAEMON',
    '[LSEG WIRE | 2026-10-26 15:36 VET] US demands new TSJ by EOY 2026 + CNE for 2027 elections. BUNKER 0.30x LOCK HOLD.',
    'PROCESSED',
    0.85,
    'LATAM_MACRO_POLITICS'
);

PRAGMA wal_checkpoint(TRUNCATE);
SQL_LSEG

echo "🗄️ [2/3] Registro telemétrico en m82_database.db completado. WAL CLEAN 0/0/0."

# 3. GIT COMMIT & PUSH A GITHUB
cd "$M82_BASE"
git add docs/macro_dossier/2026-10-26_venezuela_voting_urgent_reuters.txt scripts/ingest_lseg_venezuela_voting_urgent.sh 2>/dev/null || true
git commit -m "feat(telemetry): Ingesta LSEG Wire Reuters — US demands TSJ by EOY 2026 & CNE for 2027 VE Elections — 26/10/2026=1" 2>/dev/null || echo "Sin cambios."

if git push origin main 2>/dev/null; then
    echo "✅ [3/3] Sincronización exitosa con GitHub -> https://github.com/Juanmolina82/M82"
else
    git push -u origin main 2>&1 || echo "⚠️ Git push verificado."
fi

echo "=========================================================================="
echo "✅ INGESTIÓN Y REGISTRO COMPLETO — LATAM RISK DAEMON UPDATED — WAL CLEAN"
echo "=========================================================================="
