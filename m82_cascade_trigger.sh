#!/data/data/com.termux/files/usr/bin/bash

DB="$HOME/M82/m82_database.db"
NTFY_URL="https://ntfy.sh/M82-Molina-Alerts-v2"

RAW_PHYS=$(sqlite3 "$DB" "SELECT COALESCE(MAX(final_score), 0) FROM m82_multi_stream WHERE daemon_source IN ('ADS-B_PTY_MONITOR', 'SOUTHCOM_ISR_P8') AND created_at >= datetime('now', '-2 hours');" 2>/dev/null)
SCORE_PHYS=$(echo "$RAW_PHYS" | tr -cd '0-9')
SCORE_PHYS=${SCORE_PHYS:-0}

RAW_REG=$(sqlite3 "$DB" "SELECT COALESCE(MAX(final_score), 0) FROM m82_multi_stream WHERE daemon_source IN ('OFAC_LICENSES', 'TREASURY_DISPATCH') AND status = 'DISPATCHED' AND created_at >= datetime('now', '-6 hours');" 2>/dev/null)
SCORE_REG=$(echo "$RAW_REG" | tr -cd '0-9')
SCORE_REG=${SCORE_REG:-0}

RAW_MACRO=$(sqlite3 "$DB" "SELECT COALESCE(MAX(final_score), 0) FROM m82_multi_stream WHERE daemon_source IN ('REFINITIV_BONDS_DESK', 'CDS_SPREAD_MONITOR') AND created_at >= datetime('now', '-1 hour');" 2>/dev/null)
SCORE_MACRO=$(echo "$RAW_MACRO" | tr -cd '0-9')
SCORE_MACRO=${SCORE_MACRO:-0}

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %z')

echo "------------------------------------------------------------"
echo "[DANEKA M82] EVALUANDO CASCADA GEOPOLITICA (3 CAPAS)"
echo "Timestamp: $TIMESTAMP"

if [[ $SCORE_PHYS -ge 85 ]]; then
  echo "1. Capa Fisica (P-8 + PTY Correlacion): ACTIVADA [$SCORE_PHYS]"
else
  echo "1. Capa Fisica (P-8 + PTY Correlacion): PASIVA (<85) [$SCORE_PHYS]"
fi

if [[ $SCORE_REG -eq 100 ]]; then
  echo "2. Capa Regulatoria (OFAC/Lic):        ACTIVADA [$SCORE_REG]"
else
  echo "2. Capa Regulatoria (OFAC/Lic):        PASIVA [$SCORE_REG]"
fi

if [[ $SCORE_MACRO -ge 75 ]]; then
  echo "3. Capa Macro (VE Oil/CDS):             ACTIVADA [$SCORE_MACRO]"
else
  echo "3. Capa Macro (VE Oil/CDS):             PASIVA [$SCORE_MACRO]"
fi

if [[ $SCORE_PHYS -ge 85 && $SCORE_REG -eq 100 ]]; then
    MULTIPLIER="1.00x"
    ACTION="LIBERACION TOTAL DE CAPITAL -> $MULTIPLIER"
    PRIORITY="max"
    TAGS="rotating_light,moneybag"
elif [[ $SCORE_PHYS -ge 85 ]]; then
    MULTIPLIER="0.60x"
    ACTION="CORRELACIÓN ISR/PTY DETECTADA -> Escalando a $MULTIPLIER"
    PRIORITY="high"
    TAGS="airplane,warning"
elif [[ $SCORE_REG -eq 100 ]]; then
    MULTIPLIER="0.60x"
    ACTION="LICENCIA OFAC CONFIRMADA -> Escalando a $MULTIPLIER"
    PRIORITY="high"
    TAGS="scroll,warning"
else
    MULTIPLIER="0.30x"
    ACTION="POSTURA CONSERVADORA: Manteniendo BUNKER MODE ($MULTIPLIER)."
    PRIORITY="low"
    TAGS="shield"
fi

echo "$ACTION"

if [[ "$MULTIPLIER" != "0.30x" ]]; then
    curl -s \
        -H "Priority: $PRIORITY" \
        -H "Title: M82 RISK GOVERNOR: Escalado $MULTIPLIER" \
        -H "Tags: $TAGS" \
        -d "$ACTION | Phys: $SCORE_PHYS | Reg: $SCORE_REG | Macro: $SCORE_MACRO" \
        "$NTFY_URL" > /dev/null
fi
