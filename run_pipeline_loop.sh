#!/usr/bin/env bash
set -e
BASE="$HOME/M82"
DB="$BASE/m82_database.db"

while true; do
  echo "==== M82 LOOP $(date -Is) ===="

  # 1. INGESTAS CORE - precios que mueven físico
  python3 "$BASE/ingest_m82_macro_iran.py" 2>/dev/null || echo "m82_macro iran skip"
  python3 "$BASE/ingest_gas_troll.py" 2>/dev/null || echo "troll skip"
  python3 "$BASE/ingest_refinitiv_macro.py" 2>/dev/null || echo "macro skip"

  # 2. DAEMONS EQUITY + HEDGE + GEOPOL
  for d in daemon_nvidia_insiders.py daemon_citadel_tracker.py daemon_refinitiv_world.py daemon_ve_politics.py daemon_macro_yields.py daemon_m82_macro_trigger.py; do
    [ -f "$BASE/daemons/$d" ] && python3 "$BASE/daemons/$d" || echo "$d not found"
  done

  # 3. CALCULO FISICO VENEZUELA TIEMPO REAL
  sqlite3 "$DB" "
  INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
  SELECT 'PHYSICAL_VE_CALC',
         'FISICO VE ' || printf('%.2f', brent+13.18) || ' = Brent ' || brent || ' + squeeze 13.18 Dubai - Sargent 170k 0.16% no mueve - perdida audit $' || printf('%.2f', brent+13.18+40) || '/bbl vs -40 WTI 2020',
         'PENDING', datetime('now')
  FROM m82_iran_crisis ORDER BY id DESC LIMIT 1;
  "

  # 4. MOTOR MASTER RENDER
  python3 "$BASE/m82_engine_master.py" 2>/dev/null
  python3 "$BASE/m82_macro_final.py" 2>/dev/null

  # 5. AUDITORIA RAPIDA
  sqlite3 "$DB" "SELECT daemon_source, COUNT(*) FROM m82_multi_stream WHERE status='PENDING' GROUP BY daemon_source ORDER BY COUNT(*) DESC LIMIT 8;"

  echo "⏳ sleep 300s - proximo check $(date -d '+5 min' -Is)"
  sleep 300
done
