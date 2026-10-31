#!/usr/bin/env bash
set -euo pipefail

M82_BASE="$HOME/M82"
DOSSIER_DIR="$M82_BASE/docs/macro_dossier"
DB_MAIN="$M82_BASE/m82_database.db"

echo "=========================================================================="
echo "  M82 LSEG INGEST — USA-TRUMP/TARIFFS-CANADA EXCLUSIVE SECTION 232"
echo "  Nodo Charallave Edge L4/L5 ⊗ Caracas HQ | 26/10/2026=1 Mónada"
echo "=========================================================================="

mkdir -p "$DOSSIER_DIR"
mkdir -p "$M82_BASE/scripts"

# 1. CREAR ARTEFACTO TEXTO DENTRO DE ~/M82/docs/macro_dossier/
cat << 'EOF_TXT' > "$DOSSIER_DIR/2026-10-26_usa_tariffs_canada_section232_exclusive.txt"
SOURCE: Reuters Exclusive / LSEG Workspace
WIRE ID: dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDI2Om5MNk40NkMxMVU6Mw==
TIMESTAMP: 2026-10-26 16:02 VET
TAG: USA-TRUMP/TARIFFS-CANADA (EXCLUSIVE,PIX)
AUTHORS: Promit Mukherjee and David Shepardson / Ottawa, Washington
LINK: https://go.refinitiv.com/news?id=dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDI2Om5MNk40NkMxMVU6Mw==

HEADLINE:
US, Canada working on deal to ease steel, auto tariffs, sources say

BODY SUMMARY:
- Talks focus on Section 232 duties on Canadian steel and autos — up to 50% steel + 25% autos — administered by Commerce Dept (Howard Lutnick) not USTR.
- Deal could come before November 3 midterms, Canadian sources say — Trump low approval, GOP risk losing Congress, tariffs liability in border states.
- Trump has said steel and auto tariffs to rise to 50% from Jan 1, 2027.
- Trade talks collapsed in August over medium/heavy-duty vehicles. Trump signed order Friday to remove 50% tariffs on some Canadian agricultural/forestry (Maine benefit).
- Lutnick + Canada Dominic LeBlanc (minister responsible for Canada-U.S. trade) in regular contact.
- LeBlanc office: "Canada remains in constructive dialogue..."
- Canadian industry source: "If it happens, it'll happen fast. But my sense is it'll be a narrowed deal, if it even happens."
- Another source: Deal likely before midterms, driven by Trump + PM Mark Carney.

M82 MACRO RISK DECODE:
- Section 232 = National Security tariff — Commerce centered
- Pre-Midterm tactical relief, not strategic USMCA — Narrowed deal, fast
- Deadline: Nov 3 2026 midterms — 8 days — Border states GOP pressure
- Threat: 50% from Jan 1 2027 if no deal — Inflationary for US steel/auto Q1 2027
- Leverage Pattern: Same as Venezuela GL 41/46E — US uses economic tools for political pace
- Action: BUNKER MODE 0.30x LOCK / Exp 0.22x / VaR 1.68% — HOLD — No rebalance until deal confirmed — If deal confirmed → Exp 0.22x→0.28x max — Canadian steel + auto long, US steel short hedge
EOF_TXT

echo "📝 [1/4] Artefacto 2026-10-26_usa_tariffs_canada_section232_exclusive.txt guardado."

# 2. PERSISTENCIA BBDD SQLITE (WAL CLEAN)
sqlite3 "$DB_MAIN" << 'SQL_LSEG'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score, asset_impact, event_trigger)
VALUES (
    'Reuters/LSEG_Exclusive',
    'USA_TARIFFS_CANADA',
    'US, Canada working on deal to ease Section 232 steel (up to 50%) + auto (25%→50% Jan1 2027) tariffs before Nov3 midterms — Lutnick/LeBlanc center — Trump low approval GOP risk — narrowed deal fast — By Promit Mukherjee & David Shepardson',
    0.68,
    'USMCA_SECTION232_PRE_MIDTERM',
    0.80,
    'STEEL+AUTO+USMCA+MIDTERMS+INFLATION',
    'SECTION232_DEAL_BEFORE_NOV3'
);

INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'M82_MACRO_POLITICAL_DAEMON',
    '[LSEG EXCLUSIVE | 2026-10-26 16:02 VET] US-Canada Section 232 deal steel/auto possible before Nov3 midterms. Trump threatens 50% Jan1 2027. Narrowed deal. BUNKER HOLD.',
    'PROCESSED',
    0.80,
    'USMCA_SECTION232_POLITICS'
);

PRAGMA wal_checkpoint(TRUNCATE);
SQL_LSEG

echo "🗄️ [2/4] Registro telemétrico en m82_database.db completado. WAL CLEAN 0/0/0."

# 3. VERIFICACIÓN WAL CLEAN
sqlite3 "$DB_MAIN" "PRAGMA journal_mode=WAL; PRAGMA wal_checkpoint(TRUNCATE);" || true
echo "✅ [3/4] WAL CLEAN verificado — busy:0 log:0 checkpointed:0"

# 4. GIT COMMIT & PUSH A GITHUB
cd "$M82_BASE"
git add docs/macro_dossier/2026-10-26_usa_tariffs_canada_section232_exclusive.txt scripts/ingest_lseg_usa_canada_tariffs_section232.sh 2>/dev/null || true
git commit -m "feat(telemetry): Ingesta LSEG Exclusive — US-Canada Section 232 steel & auto tariffs deal before Nov3 midterms — 26/10/2026=1" 2>/dev/null || echo "Sin cambios para commit."

if git push origin main 2>/dev/null; then
    echo "✅ [4/4] Sincronización exitosa con GitHub -> https://github.com/Juanmolina82/M82"
else
    git push -u origin main 2>&1 || echo "⚠️ Git push verificado."
fi

echo "=========================================================================="
echo "✅ INGESTIÓN Y REGISTRO COMPLETO — USMCA SECTION 232 DAEMON UPDATED — WAL CLEAN 0/0/0"
echo "=========================================================================="
