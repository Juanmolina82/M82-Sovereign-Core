#!/usr/bin/env bash
set -euo pipefail

M82_DIR="$HOME/M82"
LOG_FILE="$M82_DIR/logs/git.log"
mkdir -p "$M82_DIR/logs"
cd "$M82_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# 1. Garantizar que el blindaje .gitignore esté siempre activo
if [ ! -f "$M82_DIR/.gitignore" ]; then
    cat << 'EOF_GI' > "$M82_DIR/.gitignore"
vault/
vault.json
.env
.env.*
*.pem
*.key
credentials.json
*.db
*.db-wal
*.db-shm
*.sqlite*
m82_database.db*
last_state.json
metrics.json
m82_fused_signal.json
__pycache__/
*.pyc
*.log
*.pid
runtime/
logs/
M82_Backups/
M82_Cards/
*.png
*.jpg
*.tar.gz
EOF_GI
fi

# 2. Asegurar que ningún archivo sensible entre al índice
git rm -r --cached vault/ vault.json *.db *.db-wal *.db-shm *.log *.png M82_Cards/ M82_Backups/ 2>/dev/null || true

# 3. Stage seguro del código fuente y scripts operativos
git add .gitignore *.py *.sh docs/ research/ 2>/dev/null || git add -A

# 4. Commit y Push atómico solo si hay cambios reales
if ! git diff --cached --quiet; then
    git commit -m "M82 AUTO-BACKUP $TIMESTAMP — BUNKER 0.30x LOCK — Charallave L4/L5 Edge" >> "$LOG_FILE" 2>&1
    if git push origin main >> "$LOG_FILE" 2>&1; then
        echo "[$TIMESTAMP] GITHUB PUSH OK — main (BUNKER 0.30x LOCK)" >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] GITHUB PUSH ERROR — revisar credenciales/red" >> "$LOG_FILE"
    fi
else
    echo "[$TIMESTAMP] GITHUB NO CHANGES — SKIP" >> "$LOG_FILE"
fi
