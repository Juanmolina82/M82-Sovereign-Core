#!/usr/bin/env bash
# ==============================================================================
# M82 RISK DESK — EMERGENCY KILL SWITCH & PARAMETER OVERRIDE
# Usage: ./m82_kill_switch.sh [SOURCE_NAME] [ACTION: DISABLE/ENABLE/SCORE] [VALUE]
# ==============================================================================

DB="$HOME/M82/m82_database.db"

if [ -z "$1" ]; then
    echo "📌 USO:"
    echo "  ./m82_kill_switch.sh FED_RATES_HAWK DISABLE       # Bloquea inmediatamente subiendo alpha_min a 100"
    echo "  ./m82_kill_switch.sh FED_RATES_HAWK ENABLE        # Restaura alpha_min a 60"
    echo "  ./m82_kill_switch.sh HOUTHI_SAUDI_MISSILE SCORE 95 # Sube el umbral de disparo"
    exit 1
fi

SOURCE="$1"
ACTION="$2"
VAL="$3"

case "$ACTION" in
    DISABLE)
        sqlite3 "$DB" "UPDATE m82_score_config SET alpha_min=100 WHERE source='$SOURCE';"
        echo "🛑 [KILL SWITCH] $SOURCE deshabilitado en tiempo real (alpha_min = 100)."
        ;;
    ENABLE)
        sqlite3 "$DB" "UPDATE m82_score_config SET alpha_min=60 WHERE source='$SOURCE';"
        echo "✅ [REESTABLECIDO] $SOURCE habilitado (alpha_min = 60)."
        ;;
    SCORE)
        if [ -n "$VAL" ]; then
            sqlite3 "$DB" "UPDATE m82_score_config SET alpha_min=$VAL WHERE source='$SOURCE';"
            echo "⚙️ [AJUSTE] $SOURCE umbral ajustado a $VAL."
        fi
        ;;
    *)
        echo "⚠️ Acción no válida. Usa DISABLE, ENABLE o SCORE."
        ;;
esac
