#!/usr/bin/env bash
cd ~/M82 || exit 1

cat << 'EOF_GIT' > .gitignore
*.db
*.db-wal
*.db-shm
*.db_backup*
__pycache__/
*.pyc
.env
*.log
EOF_GIT

git add .gitignore *.py *.sh 2>/dev/null
git commit -m "feat(v63): Integrated m82 CLI alias and multi-asset harvester suite (DELL, NVDA, XAU, WTI, HG)"
git push origin main

echo -e "\n[M82_GIT_SHIELD] -> REPOSITORIO GITHUB BLINDADO Y SINCRONIZADO EXITOSAMENTE."
