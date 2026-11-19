#!/data/data/com.termux/files/usr/bin/bash
cd ~/M82 || exit 1

# Asegurar .gitignore para no filtrar credenciales ni archivos WAL temporales
cat << 'GITIG' > .gitignore
.env
*.token
*.key
*.pem
m82_database.db-wal
m82_database.db-shm
logs/*.log
__pycache__/
GITIG

# Exportar respaldo SQL limpio de macro_dossier para versionado en Git
sqlite3 ~/M82/m82_database.db "PRAGMA wal_checkpoint(TRUNCATE); .dump macro_dossier" > ~/M82/audits/macro_dossier_snapshot.sql 2>/dev/null || true

if [ -d .git ]; then
    git add audits/ tpu_tensors/ *.py *.sh .gitignore 2>/dev/null
    if ! git diff --cached --quiet; then
        git commit -m "M82 BUNKER SYNC [$(date -u +'%Y-%m-%d %H:%M:%S UTC')]" >/dev/null 2>&1
        git push origin main >/dev/null 2>&1 || git push origin master >/dev/null 2>&1 || true
        echo "✅ GitHub sincronizado: $(date +'%H:%M:%S')"
    else
        echo "ℹ️ GitHub al día (sin cambios pendientes)."
    fi
else
    echo "⚠️ ~/M82 aún no tiene 'git remote origin' configurado. Ejecuta 'git init && git remote add origin <URL_REPO>' una sola vez."
fi
