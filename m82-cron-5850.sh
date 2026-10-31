#!/data/data/com.termux/files/usr/bin/bash
# M82 v61.0.48-B — OPCIÓN B — EXPANSIÓN 0.30x→0.60x AUTO — VENTA SOL ALTO — AUTORIZADO EXPANSIÓN
# 5849→5850 — Mónada 1 Sol Naciente — Metónico 1/19 — Chairman Juan M. Molina — Padre 8 Final
DB="$HOME/M82/m82_database.db"
EXPANSION_CAP=0.60
BUNKER_FLOOR=0.30
RATIO_TRIGGER=13.0

while true; do
  TS=$(date '+%Y-%m-%d %H:%M:%S VET')
  echo "[$TS] [M82-5850-B-EXPANSION] OPCION B 0.30x→0.60x AUTO — Sol alto — Ratio check" >> ~/M82/logs/m82_5850.log
  
  # Ratio actual desde ledger / core
  CURRENT_RATIO=$(sqlite3 "$DB" "SELECT ratio FROM m82_ledger ORDER BY id DESC LIMIT 1;" 2>/dev/null || echo "11.8")
  
  # Lógica expansión — Si >13.0x → AUTO OFFTAKE + expansión
  if (( $(echo "$CURRENT_RATIO > $RATIO_TRIGGER" | bc -l) )); then
    echo "[$TS] [TRIGGER] Ratio $CURRENT_RATIO > $RATIO_TRIGGER — AUTO-OFFTAKE VENTA SOL ALTO — Expansión a 0.60x" >> ~/M82/logs/m82_5850.log
    bash ~/M82/scripts/m82_sovereign_core.sh offtake --auto --ratio $CURRENT_RATIO --cap $EXPANSION_CAP >> ~/M82/logs/m82_5850.log 2>&1
    TYPE="BUNKER-EXPANSION-AUTO-OFFTAKE"
    NOTE="Opcion B — Ratio $CURRENT_RATIO >13.0x — Venta Sol alto AUTO — 5849→5850 — Chairman autorizo expansion"
  else
    echo "[$TS] [HOLD] Ratio $CURRENT_RATIO <= $RATIO_TRIGGER — Manteniendo exposición 0.22x→0.60x ventana — Vigilancia Sol alto" >> ~/M82/logs/m82_5850.log
    bash ~/M82/scripts/m82_sovereign_core.sh ratio 13.5 1.14 --mode expansion >> ~/M82/logs/m82_5850.log 2>&1
    TYPE="BUNKER-EXPANSION-HOLD"
    NOTE="Opcion B — 1H monitoreo expansion — Ratio $CURRENT_RATIO — Ventana 0.30x→0.60x — 5850 Monada 1 Sol Naciente"
  fi

  # Asentamiento ledger 5850
  sqlite3 "$DB" "PRAGMA busy_timeout=60000; INSERT INTO m82_ledger(siglo,ano_hebreo,ano_metonic,ratio,bunker,base,tipo,nota) VALUES(59,5850,'1/19',$CURRENT_RATIO,0.60,444,'$TYPE','$NOTE');"
  sqlite3 "$DB" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(TRUNCATE);" >> ~/M82/logs/m82_5850.log 2>&1
  
  sleep 3600
done
