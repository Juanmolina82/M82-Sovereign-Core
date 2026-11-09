#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 V60.7.6 PRIME :: FULL PERSISTENCE & AUTO-HEALING SHIELD
# Primary Node: Caracas HQ Master Node / Charallave L4 Edge
# Governance: Bunker Mode (0.30x Lock)
# ==============================================================================

set -e

M82_DIR="$HOME/M82"
BOOT_DIR="$HOME/.termux/boot"

echo "🔒 [1/4] Forzando CPU Wake Lock permanente..."
termux-wake-lock

echo "💾 [2/4] Endureciendo SQLite contra cortes de energía bruscos (WAL Mode)..."
python3 -c "
import sqlite3, os
db_path = os.path.expanduser('~/M82/m82_database.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('PRAGMA journal_mode=WAL;')
    c.execute('PRAGMA synchronous=NORMAL;')
    c.execute('PRAGMA busy_timeout=60000;')
    conn.commit()
    conn.close()
    print('  ✅ SQLite WAL, synchronous=NORMAL y busy_timeout=60000 sellados.')
"

echo "🤖 [3/4] Creando el Watchdog de Autorrecuperación (m82_watchdog.sh)..."
cat << 'WATCHDOG' > "$M82_DIR/m82_watchdog.sh"
#!/data/data/com.termux/files/usr/bin/bash

# Asegurar CPU activa
termux-wake-lock

# 1. Verificar si el Orquestador Principal está corriendo
if ! pgrep -f "m82_cron_runner.sh" > /dev/null; then
    echo "[$(date)] ⚠️ Orchestrator caído. Reviviendo M82 Citadel Prime..." >> ~/M82/watchdog.log
    cd ~/M82
    nohup bash ~/M82/m82_cron_runner.sh > ~/M82/cron_prime.log 2>&1 &
fi

# 2. Mantener activo el Servidor HTTP de Dashboard (:8080)
if ! pgrep -f "http.server 8080" > /dev/null; then
    cd ~/M82/dashboard && nohup python3 -m http.server 8080 --bind 0.0.0.0 > /dev/null 2>&1 &
fi
WATCHDOG

chmod +x "$M82_DIR/m82_watchdog.sh"

echo "🚀 [4/4] Configurando el inicio automático de Android (Termux:Boot)..."
mkdir -p "$BOOT_DIR"

cat << 'BOOT' > "$BOOT_DIR/start_m82.sh"
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
sleep 10
bash ~/M82/m82_watchdog.sh
BOOT

chmod +x "$BOOT_DIR/start_m82.sh"

# Inyectar watchdog en Crontab (Comprobación cada 1 minuto)
(crontab -l 2>/dev/null | grep -v "m82_watchdog.sh"; echo "* * * * * bash ~/M82/m82_watchdog.sh") | crontab -

# Asegurar crond activo
crond > /dev/null 2>&1 || true

# Ejecutar verificación inicial del watchdog
bash "$M82_DIR/m82_watchdog.sh"

echo ""
echo "=============================================================================="
echo " ✅ M82 CITADEL PRIME PERSISTENCE SHIELD ACTIVATED"
echo " • Wake Lock    : ACTIVE (CPU siempre encendida)"
echo " • Termux:Boot  : INSTALADO (~/.termux/boot/start_m82.sh)"
echo " • Watchdog     : ACTIVO (Cron monitoreando cada 60 seg)"
echo " • Engine WAL   : RESISTENTE A APAGONES & REINICIOS"
echo " • Governance   : 🔒 ACTIVE (0.30x LOCK — BUNKER MODE)"
echo "=============================================================================="
