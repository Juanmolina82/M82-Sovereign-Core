#!/usr/bin/env bash
# ==============================================================================
# M82 BOOTSTRAP NODE — LANZAMIENTO Y VERIFICACIÓN
# Node: Caracas HQ Node
# ==============================================================================

touch "$HOME/M82/m82_overnight.log"
pkill -f m82_overlord || true
pkill -f m82_wal_sentinel || true

nohup bash "$HOME/M82/m82_overlord.sh" >/dev/null 2>&1 &
sleep 2

bash "$HOME/M82/m82_passive_status.sh"
