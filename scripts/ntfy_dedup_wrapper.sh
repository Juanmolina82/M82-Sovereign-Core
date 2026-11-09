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
