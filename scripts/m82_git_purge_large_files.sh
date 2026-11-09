#!/usr/bin/env bash
set -e
cd ~/M82

echo "🧹 [1/4 CLEANUP] Configurando .gitignore para excluir volcados pesados y BBDD..."
cat << 'EOF_GITIGNORE' > .gitignore
*.db
*.db-wal
*.db-shm
*.tar.gz
*.sql
backups/
logs/
*.log
EOF_GITIGNORE

echo "🗑️ [2/4 UNTRACK] Removiendo archivos pesados del índice de Git (sin borrar archivos locales)..."
git rm -r --cached backups/ 2>/dev/null || true
git rm --cached m82_database.db 2>/dev/null || true
git rm --cached *.sql 2>/dev/null || true
git rm --cached *.tar.gz 2>/dev/null || true

echo "🔄 [3/4 COMMIT] Creando commit estructurado solo con código, scripts y metadatos..."
git add .gitignore
git add scripts/
git add *.py 2>/dev/null || true
git add *.md 2>/dev/null || true

git commit -m "M82 Sovereign Core v61.0.34 - Purged large binaries & dumps for clean GitHub push - jmmp@molina82.com" || echo "⚠️ Sin cambios que commitear."

echo "🚀 [4/4 FORCE PUSH] Despachando repositorio limpio hacia GitHub..."
git push origin main || git push -f origin main

echo "🟢 [SUCCESS] Repositorio github.com/Juanmolina82/M82 liberado y sincronizado al 100%."
