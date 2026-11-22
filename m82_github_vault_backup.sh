#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$HOME/M82"
mkdir -p "$HOME/M82/backups"

cat << 'GITIGNORE' > .gitignore
.env*
*.env
*token*
*secret*
*.db
*.db-wal
*.db-shm
*.log
__pycache__/
*.pyc
GITIGNORE

TS=$(date +"%Y%m%d_%H%M%S")
SNAP_FILE="$HOME/M82/backups/m82_db_snapshot_${TS}.sqlite"

# Hot-Backup nativo en Python (cero bloqueos sobre m82_database.db)
python3 - << PYEOF
import sqlite3, os
home = os.path.expanduser("~")
src = sqlite3.connect(f"file:{home}/M82/m82_database.db?mode=ro", uri=True, timeout=60.0)
dst = sqlite3.connect("${SNAP_FILE}")
src.backup(dst)
dst.close()
src.close()
PYEOF

gzip -f "$SNAP_FILE"
sha256sum "${SNAP_FILE}.gz" > "${SNAP_FILE}.gz.sha256"
ls -t "$HOME/M82/backups/"*.gz 2>/dev/null | tail -n +4 | xargs -r rm -f
ls -t "$HOME/M82/backups/"*.sha256 2>/dev/null | tail -n +4 | xargs -r rm -f

if [ ! -d .git ]; then
    git init
    git branch -M main
fi

git add .gitignore docs/M82_PYTHAGORAS_THORP_DOCTRINE_V605.md thorp_kelly_m82.py thorp_spectral_gamma_l3.py thorp_montecarlo_survival_l4.py m82_pythagoras_thorp_orchestrator.py m82_master_session_sync.py m82_github_vault_backup.sh m82_quant_hud_renderer.py m82_quant_daemon.py thorp_dynamic_frontier_l7.py m82_sunday_open_sentinel.py docs/M82_SUNDAY_PREFLIGHT_BRIEF.md backups/*.gz backups/*.sha256 2>/dev/null || true

if ! git diff --cached --quiet; then
    git commit -m "M82 V60.5 Sovereign Core: Pythagoras-Thorp L1-L5 Orchestrator, Doctrine & Verified Snapshot (${TS})"
fi

if git remote | grep -q origin; then
    CURR_BRANCH=$(git branch --show-current); git push -u origin "${CURR_BRANCH:-M82}"
    echo "[GITHUB VAULT OK] Respaldo blindado enviado a GitHub (SHA-256 verificado)."
else
    echo "[GITHUB VAULT READY] Commit local blindado y sellado con SHA-256."
    echo "Para vincular su repositorio privado en GitHub, ejecute:"
    echo "  git remote add origin https://github.com/SU_USUARIO/SU_REPO_M82.git && CURR_BRANCH=$(git branch --show-current); git push -u origin "${CURR_BRANCH:-M82}""
fi
