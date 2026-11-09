#!/data/data/com.termux/files/usr/bin/bash
set -e
export TMPDIR=$PREFIX/tmp
LOCKFILE="$TMPDIR/m82_ntfy.lock"
DB="$HOME/M82/m82_earnings.db"

# Wrapper anti-bucle para ntfy.sh + tg — Solo 1 dispatch cada 8 min mínimo
# Evita duplicado 22:13 + 22:15
cat > ~/M82/scripts/ntfy_dedup_wrapper.sh <<'EWRAP'
#!/data/data/com.termux/files/usr/bin/bash
LOCK="$TMPDIR/m82_ntfy.lock"
# Si lock existe y tiene menos de 480s (8 min), skip duplicado
if [ -f "$LOCK" ]; then
  AGE=$(($(date +%s) - $(stat -c %Y "$LOCK" 2>/dev/null || echo 0)))
  if [ "$AGE" -lt 480 ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) NTFY DEDUP SKIP — age ${AGE}s < 480s — evita bucle" >> "$HOME/M82/logs/earnings.log"
    exit 0
  fi
fi
# Crear lock
touch "$LOCK"
# Dispatch real
cat | bash "$HOME/M82/scripts/ntfy.sh"
EWRAP
chmod +x ~/M82/scripts/ntfy_dedup_wrapper.sh

# Actualizar earnings_sector_alert.sh para usar wrapper
sed -i 's|\$NTFY|cat | bash $HOME\/M82\/scripts\/ntfy_dedup_wrapper.sh|g' ~/M82/scripts/m82_earnings_sector_alert.sh 2>/dev/null || true
sed -i 's|echo "\$MSG" | $NTFY|echo "$MSG" | bash $HOME\/M82\/scripts\/ntfy_dedup_wrapper.sh|g' ~/M82/scripts/m82_earnings_sector_alert.sh 2>/dev/null || true

echo "FIX NTFY DEDUP OK — Lock 8 min — Evita bucle 22:13+22:15"
ls -lh ~/M82/scripts/ntfy_dedup_wrapper.sh
cat ~/M82/scripts/m82_earnings_sector_alert.sh | grep -A2 -B2 "ntfy\|NTFY" | tail -20
