#!/bin/bash
BASE=/data/data/com.termux/files/home/M82
DESKS=$BASE/desks
LOGS=$BASE/logs
mkdir -p "$LOGS"

for D in m82_hormuz_centcom_sentinel_daemon.py m82_iea_supply_balance_daemon.py m82_refining_merey16_parity_daemon.py m82_macro_dossier_auditor_daemon.py m82_realtime_energy_feed_daemon.py; do
    if ! pgrep -f "$D" > /dev/null; then
        nohup python3 -u "$DESKS/$D" >> "$LOGS/${D%.py}.log" 2>&1 &
    fi
done
