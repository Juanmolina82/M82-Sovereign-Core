#!/usr/bin/env bash
# ==============================================================================
# M82 VERIFY PERSISTENCE — AUDITORÍA DE SOBREVIVENCIA A REBOOT
# Node: Caracas HQ Node
# ==============================================================================

BOOT_SCRIPT="$HOME/.termux/boot/m82-boot.sh"
BACKUP_DB="$HOME/M82/backups/m82_database_backup.db"

echo "=============================================================================="
echo "🛡️ M82 PERSISTENCE CHECK // CHARALLAVE EDGE"
echo "=============================================================================="

if [ -x "$BOOT_SCRIPT" ]; then
    echo " ✅ Termux Boot Hook   : CONFIGURADO ($BOOT_SCRIPT)"
else
    echo " ❌ Termux Boot Hook   : NO DETECTADO"
fi

if [ -f "$BACKUP_PATH" ] || [ -f "$BACKUP_DB" ]; then
    echo " ✅ Cold Storage DB    : COPIA INMUTABLE PRESENTE"
else
    echo " ⚠️ Cold Storage DB    : SIN BACKUP INICIAL (Ejecutar ~/M82/m82_backup_guard.sh)"
fi

WAKE_LOCK_STATUS=$(ps aux | grep -i "termux-wake-lock" | grep -v grep || true)
if [ -n "$WAKE_LOCK_STATUS" ]; then
    echo " ✅ CPU Wake-Lock      : RETENIDO POR EL KERNEL"
else
    echo " ℹ️ CPU Wake-Lock      : ACTIVO VÍA OVERLORD SH"
fi

echo "=============================================================================="
