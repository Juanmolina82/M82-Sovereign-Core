#!/usr/bin/env bash
set -e
cd ~/M82

echo "🔄 [M82 GITHUB FORCE SYNC] Sincronizando BBDD y scripts..."
git add -f m82_database.db
git add scripts/
git add *.py 2>/dev/null || true

COMMIT_MSG="M82 Sovereign Core v61.0.34 Sync - Gas Commodities Swarm 149 Records - jmmp@molina82.com"
git commit -m "$COMMIT_MSG" || echo "⚠️ [GIT] No hay cambios nuevos que commitear."

echo "🚀 [GIT PUSH] Despachando a origin main..."
git push origin main || git push -f origin main

echo "🟢 [GITHUB SYNC SUCCESS] Repositorio github.com/Juanmolina82/M82 actualizado exitosamente."
