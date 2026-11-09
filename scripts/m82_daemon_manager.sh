#!/usr/bin/env bash

echo "======================================================"
echo "   M82 CHARALLAVE NODE // MULTI-DAEMON MONITOR"
echo "======================================================"

DAEMONS=(
    "m82_m82_macro_notebook_daemon.py"
    "m82_crypto_commodities_daemon.py"
    "m82_treasury_bonds_daemon.py"
    "m82_musk_empire_daemon.py"
    "m82_spacex_telecom_daemon.py"
    "m82_musk_daemon.py"
    "m82_geopolitical_events_daemon.py"
)

case "$1" in
    start)
        echo "[+] Iniciando todos los Daemons M82 en segundo plano..."
        for d in "${DAEMONS[@]}"; do
            if [ -f "$HOME/M82/$d" ]; then
                nohup python3 -u "$HOME/M82/$d" > /dev/null 2>&1 &
                echo "  ├─> $d: INICIADO"
            else
                echo "  ├─> $d: NO ENCONTRADO (Omitido)"
            fi
        done
        ;;
    status)
        echo "[*] Estado de los Procesos Activos:"
        ps aux | grep -E "m82_.*daemon\.py|http\.server|m82_api_server" | grep -v grep
        ;;
    stop)
        echo "[-] Deteniendo todos los Daemons M82..."
        pkill -f "m82_.*daemon\.py"
        echo "[✓] Daemons detenidos."
        ;;
    *)
        echo "Uso: $0 {start|status|stop}"
        ;;
esac
