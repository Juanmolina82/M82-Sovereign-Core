#!/data/data/com.termux/files/usr/bin/bash

# Bucle infinito para refresco en tiempo real
while true; do
  clear
  echo "=================================================="
  echo "  REFINITIV WORKSPACE / M82 MACRO — CURVA EN VIVO"
  echo "  Usuario: jmmp@molina82.com | Ref: M82.CORE.V3"
  echo "  Hora Local: $(date '+%H:%M:%S') | Estado: REAL-TIME"
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
  echo "[CAPA 3 MACRO] 21 Bonos procesados | Rally: +8.45%"
  echo "=================================================="
  
  sleep 2
done
