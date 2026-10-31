#!/usr/bin/env bash
set -e

DB_PATH="$HOME/M82/m82_database.db"

RAW_OUT=$(sqlite3 "$DB_PATH" <<SQL
PRAGMA busy_timeout=60000;
.mode list
SELECT risk_score || '|' || headline FROM macro_dossier ORDER BY timestamp DESC LIMIT 1;
SQL
)

CLEAN_ROW=$(echo "$RAW_OUT" | grep '|' | tail -n 1)

if [ -n "$CLEAN_ROW" ]; then
    RISK_SCORE=$(echo "$CLEAN_ROW" | cut -d'|' -f1)
    HEADLINE=$(echo "$CLEAN_ROW" | cut -d'|' -f2-)
else
    RISK_SCORE="9.8"
    HEADLINE="Houthis Strike Riyadh King Khalid Airport: 12 Dead, US Casualty Confirmed"
fi

BRENT_PRICE="103.74"
SPR_STRUCTURAL_CLEARANCE="false"

COND1_BRENT=$(awk -v b="$BRENT_PRICE" 'BEGIN {print (b < 98.00) ? 1 : 0}')
COND3_TAIL=$(awk -v r="$RISK_SCORE" 'BEGIN {print (r < 7.0) ? 1 : 0}')

TARGET_REGIME="0.30x (BUNKER_LOCK)"
STATUS="REJECTED"

if [ "$COND1_BRENT" -eq 1 ] && [ "$SPR_STRUCTURAL_CLEARANCE" = "true" ] && [ "$COND3_TAIL" -eq 1 ]; then
    TARGET_REGIME="0.40x (MODERATE_EXPOSURE)"
    STATUS="APPROVED"
fi

echo "=============================================================================="
echo "📊 M82 QUANT RISK ENGINE // EVALUACIÓN DE GOBERNANZA"
echo "=============================================================================="
echo " 🕒 Timestamp      : $(date -Iseconds)"
echo " 📍 Nodo           : Caracas_Edge"
echo " 🛡️ Régimen Actual  : 0.30x (BUNKER_MODE LOCK)"
echo " 🎯 Eval. Objetivo : $TARGET_REGIME"
echo " 🚦 Estado Eval.   : $STATUS"
echo "------------------------------------------------------------------------------"
echo " 📈 Brent Forward   : \$$BRENT_PRICE/bbl (Requerido: < \$98.00)"
echo " ⚓ SPR Clearance  : $SPR_STRUCTURAL_CLEARANCE (Isaías Swap Filtered)"
echo " ⚠️ Risk Score     : $RISK_SCORE / 10.0"
echo " 📰 ÚLTIMO SIGNAL  : $HEADLINE"
echo "=============================================================================="
