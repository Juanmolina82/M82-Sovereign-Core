#!/bin/bash

echo "[M82] Iniciando proceso de indexación masiva..."
python3 ~/M82/m82_ingestor.py

echo ""
echo "[M82] Últimos 5 registros indexados en m82_database.db:"
sqlite3 ~/M82/m82_database.db "SELECT id, daemon_source, alpha_score, status, asset_impact, substr(headline,1,55) FROM m82_multi_stream ORDER BY id DESC LIMIT 5;"

