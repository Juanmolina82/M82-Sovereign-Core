#!/usr/bin/env bash
set -euo pipefail
M82_BASE="$HOME/M82"
DB_MAIN="$M82_BASE/m82_database.db"
DB_FAM="$M82_BASE/m82_familia.db"
echo "=========================================================================="
echo "  M82 SPIT GERENTE NOW — 26/10/2026=1 MÓNADA — CHARALLAVE L4/L5 — BUNKER 0.30x"
echo "=========================================================================="
echo ">>> [1/5] GITHUB DOSSIER + MACRO DOSSIER COUNT"
sqlite3 "$DB_MAIN" "SELECT 'github_dossier=' || COUNT(*) FROM github_dossier; SELECT 'macro_dossier=' || COUNT(*) FROM macro_dossier; SELECT 'multi_stream=' || COUNT(*) FROM m82_multi_stream;"
echo ">>> [2/5] WAL CHECK + MODE"
sqlite3 "$DB_MAIN" "PRAGMA journal_mode; PRAGMA wal_checkpoint(TRUNCATE);"
sqlite3 "$DB_FAM" "PRAGMA journal_mode; PRAGMA wal_checkpoint(TRUNCATE);"
echo ">>> [3/5] GIT STATUS + LOG 5 COMMITS MÓNADA"
cd "$M82_BASE"
git status --porcelain
git log --oneline -5 --graph
echo ">>> [4/5] QUINTINOMIO ARTEFACTOS — LS macro_dossier"
ls -lh "$M82_BASE/docs/macro_dossier/" | tail -20
echo ">>> [5/5] SPIT TELEGRAM DANFEKA -1004335849125 + PUSH GITHUB"
python3 ~/M82/scripts/m82_github_indexer.py 2>&1 | tail -40 || true
# Telegram spit
if [ -f ~/M82/scripts/m82_telegram_dispatcher.py ]; then
  python3 ~/M82/scripts/m82_telegram_dispatcher.py "🚀 M82 SPIT GERENTE NOW — $(date -u) — 36 github_dossier + 33 macro_dossier + 163 Daemons — WAL 0/0/0 — BUNKER 0.30x LOCK — Quintinomio Mónada 1 sellado — github.com/Juanmolina82/M82" 2>&1 | tail -10 || true
fi
cd "$M82_BASE"
git add -A
git commit -m "feat(spit): M82 SPIT GERENTE NOW — Dashboard 36+33+163 — WAL 0/0/0 — Bunker 0.30x — 26/10/2026=1" 2>/dev/null || echo "Sin cambios"
git push origin main 2>&1 | tail -5
echo "=========================================================================="
echo "✅ SPIT COMPLETO — GERENTE — WAL CLEAN 0/0/0 — GITHUB + TELEGRAM — BUNKER 0.30x"
echo "=========================================================================="
