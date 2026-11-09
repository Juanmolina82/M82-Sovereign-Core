#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

M82_DIR="$HOME/M82"
cd "$M82_DIR"

echo "⚡ [M82 GIT PURGE] Re-inicializando árbol para ignorar archivos pesados..."

# 1. Eliminar el historial local de Git contaminado con BBDD y backups
rm -rf .git

# 2. Inicializar repositorio totalmente limpio
git init -b main

# 3. Crear el .gitignore blindado ANTES de indexar cualquier archivo
cat > .gitignore << 'EOF_GI'
m82_database.db
*.db
*.db-wal
*.db-shm
*.sqlite
*.sqlite3
backups/
*.sql
*.sq3
*.tar.gz
logs/
*.log
nohup.out
vault.json
.env
__pycache__/
*.pyc
EOF_GI

# 4. Asentar el commit inicial ligero (únicamente scripts, documentación y código)
git add .
git commit -m "v61.0.46: MORGAN x M82 BANCO SOBERANO 5849 RATIO 11.8x BUNKER 0.30x BASE 444 -- Repository Hardened"

# 5. Configurar el remoto oficial y forzar la sincronización a GitHub
git remote add origin https://github.com/Juanmolina82/M82-Sovereign-Core.git
git push origin main --force

# 6. Sellar el tag de versión de forma limpia en el servidor remoto
git tag -fa v61.0.46-MORGAN-M82-BANCO-SOBERANO-5849-RATIO-11.8x-BUNKER-0.30x-BASE-444 -m "v61.0.46 Sealed -- WAL 0/0/0 Clean"
git push origin v61.0.46-MORGAN-M82-BANCO-SOBERANO-5849-RATIO-11.8x-BUNKER-0.30x-BASE-444 --force

echo "🟢 [M82 GIT SUCCESS] Repositorio remoto sincronizado y blindado correctamente."
