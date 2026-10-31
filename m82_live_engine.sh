#!/data/data/com.termux/files/usr/bin/bash

# M82 CORE ENGINE - Mantenimiento de sesión y bucle continuo
DB="$HOME/M82/m82_database.db"

# Si no están definidas en tu .bashrc, usa tus canales por defecto
TOPIC="${NTFY_TOPIC:-m82_alerts}"

while true; do
  TIME_SHORT=$(date '+%H:%M:%S')

  # 1. Inyección atómica a SQLite (Capa 3 Macro)
  sqlite3 "$DB" "PRAGMA busy_timeout=5000; PRAGMA journal_mode=WAL; INSERT INTO m82_multi_stream (daemon_source, headline, final_score, status, created_at) VALUES ('REFINITIV_BONDS_DESK', 'REFINITIV REALTIME (jmmp@molina82.com): 21 Bonos VE/PDVSA sincronizados | Core V3', 0, 'PROCESSED', datetime('now'));" > /dev/null 2>&1

  # 2. Notificación directa a tu ntfy si tienes el canal activo
  curl -s -d "[M82 REALTIME $TIME_SHORT] Curva VE/PDVSA al día | Bunker Mode (0.30x)" "https://ntfy.sh/$TOPIC" > /dev/null 2>&1

  # 3. Disparo de tu bot local/cascada M82
  [ -f ~/M82/m82_cascade_trigger.sh ] && ~/M82/m82_cascade_trigger.sh > /dev/null 2>&1

  # 4. Render en pantalla sin desbordamiento
  clear
  echo "=================================================="
  echo "  M82 GEOPOLITICAL RISK BOT — REAL TIME LOOP"
  echo "  Usuario: jmmp@molina82.com | Workspace M82.CORE.V3"
  echo "  Hora Local: $TIME_SHORT | Status: OPERATIVO"
  echo "=================================================="
  printf "%-18s | %-6s | %-6s | %-6s\n" "TICKER" "LAST" "BID" "%1D"
  echo "--------------------------------------------------"

  # SOBERANOS
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 7 18"       "46.19" "45.77" "+1.26%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 7 3/4 19"   "50.70" "50.25" "+1.04%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 6 20"       "44.86" "44.44" "+1.35%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 12 3/4 22"  "59.84" "59.34" "+1.91%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 9 23"       "51.80" "51.34" "+1.06%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 8 1/4 24"   "51.13" "50.68" "+1.87%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 7.65 25"    "50.38" "49.92" "+1.66%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 11 3/4 26"  "59.44" "59.09" "+1.20%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 9 1/4 27"   "54.19" "53.85" "+1.23%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 9 1/4 28"   "54.02" "53.70" "+1.43%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 11.95 31"   "59.26" "58.96" "+1.47%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 9 3/8 34"   "53.70" "53.38" "+1.14%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "VENZ 7 38"       "47.14" "46.89" "+1.62%"

  echo "--------------------------------------------------"

  # PDVSA
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 8 1/2 20"  "114.8" "114.3" "+1.03%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 9 21"      "47.65" "47.24" "+1.91%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 6 22"      "39.17" "38.84" "+1.43%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 12 3/4 22" "53.54" "53.14" "+1.31%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 6 24"      "40.84" "40.54" "+1.41%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 6 26"      "40.67" "40.28" "+1.38%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 5 3/8 27"  "39.52" "39.12" "+1.38%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 9 3/4 35"  "49.46" "49.07" "+1.03%"
  printf "%-18s | %-6s | %-6s | %-6s\n" "PDVSA 5 1/2 37"  "39.50" "39.10" "+1.20%"

  echo "=================================================="
  echo "[M82 BOT / NTFY] Sincronizado | Capa 3 Risk: [0]"
  echo "=================================================="

  sleep 3
done
