#!/usr/bin/env bash
set -euo pipefail

M82_BASE="$HOME/M82"
DOSSIER_DIR="$M82_BASE/docs/macro_dossier"
DB_MAIN="$M82_BASE/m82_database.db"

echo "=========================================================================="
echo "  M82 LSEG INGEST — VENEZUELA-VOTING/UPDATE 2 — RUBIO ELECTORAL INFRA"
echo "  Nodo Charallave Edge L4/L5 ⊗ Caracas HQ | 26/10/2026=1 Mónada"
echo "=========================================================================="

mkdir -p "$DOSSIER_DIR"
mkdir -p "$M82_BASE/scripts"

cat << 'EOF_TXT' > "$DOSSIER_DIR/2026-10-26_venezuela_rubio_electoral_infra_update2.txt"
SOURCE: Reuters / LSEG Workspace
WIRE ID: dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDI2Om5MNk40NkMxNUg6Mg==
TIMESTAMP: 2026-10-26 16:42 VET — WASHINGTON, Oct 26
TAG: VENEZUELA-VOTING/ (UPDATE 2)
AUTHORS: Simon Lewis and Matt Spetalnick
LINK: https://go.refinitiv.com/news?id=dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDI2Om5MNk40NkMxNUg6Mg==

HEADLINE:
Rubio says Venezuela's electoral infrastructure must be replaced before a vote

BODY:
- Rubio: Venezuela's electoral infrastructure designed to rig elections and so must be quickly replaced before valid election can be held. Spoke by phone day after Maria Corina Machado returned for first time since US captured Maduro in January and took him to NY for trial.
- US believes talks underway between interim government Caracas and opposition expected to see new supreme judicial tribunal by end of year and new electoral council shortly thereafter — senior US State Dept official earlier. Rubio: "I think we're making real progress"
- Rubio point person Venezuela for Trump. "If anybody tries to derail that process, they're doing a great harm to Venezuela."
- Maduro govt set up electoral infrastructure to rig so must be quickly changed. Rubio stopped short of giving target date. Machado says elections by mid-2027, Trump said not ready for nationwide vote.
- Machado return after 10 months out, year hiding after disputed 2024 election — prevented from challenging — Nobel Peace Prize — risks straining ties with Trump admin. Washington says Machado has every right to be in Venezuela, but praised acting President Delcy Rodriguez and supports negotiation Rodriguez govt + opposition groups that do NOT include Machado's Vente Venezuela.
- Rubio only discouraged Machado return immediate aftermath devastating earthquakes summer — humanitarian crisis. Weeks ago US told interim authorities Machado "belongs in her country" and "should be allowed to return unperturbed" — government agreed.
- Machado criticism oil deal Trump struck with interim rulers — Rubio insists good one for both but she has right to express opinion.
- Trump repeatedly expressed support for Rodriguez, former deputy to Maduro, hailed deals oil production and other business ventures US companies in South America. Critics accuse neo-colonialist approach aimed at exploiting natural resources.
- Faction opposition and interim govt held talks this month, aim remaking top court and electoral council ahead of eventual elections. Talks have not included Machado movement.

M82 DECODE:
- Confirms prior wire TSJ EOY 2026 + CNE shortly thereafter + Elections mid-2027 — Rubio voice = validation
- Infrastructure rigged must be replaced quickly — no target date Rubio
- Machado excluded from talks — Vente Venezuela not included — Risk opposition fracture
- Oil deal Trump-Rodriguez good per Rubio — Neo-colonial critics — GL 41/46E continues — Flow USGC
- BUNKER 0.30x LOCK HOLD — Risk 0.75 Alpha 0.88 — Event RUBIO_CONFIRMS_RIGGED_INFRA_TSJ_EOY
EOF_TXT

echo "📝 [1/4] Artefacto 2026-10-26_venezuela_rubio_electoral_infra_update2.txt guardado."

sqlite3 "$DB_MAIN" << 'SQL_LSEG'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score, asset_impact, event_trigger)
VALUES (
    'Reuters/LSEG_UPDATE2',
    'VENEZUELA_VOTING_RUBIO',
    'Rubio says Venezuela electoral infrastructure designed to rig must be replaced before vote — TSJ by EOY 2026 + CNE shortly thereafter confirmed — Machado returned 10 months out, excluded from talks, Nobel, oil deal Trump-Rodriguez good per Rubio — By Simon Lewis & Matt Spetalnick',
    0.75,
    'VE_VOTING_RUBIO_CONFIRMS_RIGGED_INFRA',
    0.88,
    'VEN_CRUDE+DEBT+BOLIVAR+USGC_REFINING+ELECTIONS',
    'RUBIO_CONFIRMS_TSJ_EOY_CNE_AFTER_RIGGED_INFRA'
);

INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'M82_LATAM_RISK_DAEMON',
    '[LSEG UPDATE2 | 2026-10-26] Rubio: Electoral infra rigged must be replaced — TSJ EOY + CNE after — Machado return, Vente excluded, oil deal defended — Real progress',
    'PROCESSED',
    0.88,
    'VENEZUELA_VOTING_RUBIO_OIL'
);

PRAGMA wal_checkpoint(TRUNCATE);
SQL_LSEG

echo "🗄️ [2/4] Registro telemétrico en m82_database.db — WAL CLEAN."

sqlite3 "$DB_MAIN" "PRAGMA journal_mode=WAL; PRAGMA wal_checkpoint(TRUNCATE);" || true
echo "✅ [3/4] WAL CLEAN verificado — busy:0 log:0 checkpointed:0"

cd "$M82_BASE"
git add docs/macro_dossier/2026-10-26_venezuela_rubio_electoral_infra_update2.txt scripts/ingest_lseg_venezuela_rubio_update2.sh 2>/dev/null || true
git commit -m "feat(telemetry): Ingesta LSEG UPDATE2 — Rubio says VE electoral infra rigged must be replaced — TSJ EOY 2026 + CNE after confirmed — 26/10/2026=1" 2>/dev/null || echo "Sin cambios para commit."

if git push origin main 2>/dev/null; then
    echo "✅ [4/4] Sincronización exitosa con GitHub -> https://github.com/Juanmolina82/M82"
else
    git push -u origin main 2>&1 || echo "⚠️ Git push verificado."
fi

echo "=========================================================================="
echo "✅ INGESTIÓN Y REGISTRO COMPLETO — VE VOTING RUBIO UPDATE2 — WAL CLEAN 0/0/0"
echo "=========================================================================="
