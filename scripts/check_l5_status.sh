#!/usr/bin/env bash
echo "=========================================================="
echo "      M82 V60.3 EDGE NODE :: HEALTH CHECK & STATUS        "
echo "=========================================================="
echo "--- PROCESOS ACTIVOS EN SEGUNDO PLANO ---"
ps aux | grep -E "orch.py|refinitiv_bridge" | grep -v grep

echo ""
echo "--- ULTIMAS ENTRADAS EN MULTI STREAM (WAL) ---"
sqlite3 ~/M82/m82_database.db "SELECT id, daemon_source, status, created_at FROM m82_multi_stream ORDER BY id DESC LIMIT 5;" 2>/dev/null || echo "Error leyendo base de datos."
echo "=========================================================="
