#!/data/data/com.termux/files/usr/bin/bash
set +e
mkdir -p /data/data/com.termux/files/usr/tmp
ln -sf /data/data/com.termux/files/usr/tmp /tmp 2>/dev/null || true
CRON_TMP="$HOME/M82/logs/cron.tmp"
mkdir -p "$HOME/M82/logs"
crontab -l > "$CRON_TMP" 2>/dev/null || echo "" > "$CRON_TMP"
# Limpiar entradas earnings viejas
grep -v "earnings_sector" "$CRON_TMP" > "${CRON_TMP}.clean" 2>/dev/null || cp "$CRON_TMP" "${CRON_TMP}.clean"
# Añadir nueva cadencia 10 min alterna sin colisión con 5 min principal (0,5,10,15...)
echo "3,13,23,33,43,53 * * * 1-5 bash $HOME/M82/scripts/m82_earnings_sector_alert.sh" >> "${CRON_TMP}.clean"
crontab "${CRON_TMP}.clean"
echo "CRON FIX OK:"
crontab -l | grep -E "dual_5min|earnings|github|weekly"
rm -f "$CRON_TMP" "${CRON_TMP}.clean"
