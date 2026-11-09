#!/data/data/com.termux/files/usr/bin/bash
set -e

CD_DIR="$HOME/M82"
cd "$CD_DIR"

echo "⚡ [DANEKA DEPLOY] Arrancando daemon en background y pusheando a GitHub..."

# 1. Matar instancias previas si existen
pkill -f "daneka_trump_rubio_tracker.py" 2>/dev/null || true

# 2. Iniciar Daemon en Background
nohup python3 ~/M82/daneka_trump_rubio_tracker.py > ~/M82/logs/daneka.log 2>&1 &
echo "✅ Daemon daneka_trump_rubio_tracker.py corriendo en background (Log: ~/M82/logs/daneka.log)."

# 3. Disparo inicial de sincronización BBDD WAL
sqlite3 ~/M82/m82_database.db "PRAGMA wal_checkpoint(TRUNCATE);"

# 4. Sincronización con Branch 'transicion-mcm'
git checkout transicion-mcm 2>/dev/null || git checkout -b transicion-mcm
git add daneka_trump_rubio_tracker.py README_TRANSICION_MCM.md 2>/dev/null || git add .
git commit -m "M82_DANEKA_AUTO_PUSH_24OCT26 — Trump/Rubio Tracker Active — Branch Transición" || echo "Sin cambios en git."

if command -v gh &> /dev/null && gh auth status &> /dev/null; then
    git push -u origin transicion-mcm
    echo "🚀 [GITHUB] Commit pusheado exitosamente a origin/transicion-mcm."
else
    git push origin transicion-mcm 2>/dev/null || echo "⚠️ Revisa credenciales git para push remoto."
fi

echo "✅ [SUCCESS] DANEKA AUTO-PUSH desplegado y acoplado."
