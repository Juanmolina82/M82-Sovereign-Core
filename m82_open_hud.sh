#!/data/data/com.termux/files/usr/bin/bash
M82_DIR="$HOME/M82"
mkdir -p "$M82_DIR/static" "$M82_DIR/logs"

# 1. Evitar suspensión de sockets en Android
command -v termux-wake-lock >/dev/null 2>&1 && termux-wake-lock

# 2. Actualizar telemetría maestra
python3 "$M82_DIR/m82_quant_api_bridge.py"

# 3. Reiniciar servidor :8080 totalmente desacoplado (setsid)
pkill -f "http.server 8080" 2>/dev/null || true
setsid python3 -m http.server 8080 --bind 0.0.0.0 --directory "$M82_DIR/static" </dev/null >"$M82_DIR/logs/pwa_8080.log" 2>&1 &
sleep 1

# 4. Verificar respuesta HTTP 200 antes de abrir navegador
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/m82_quant_hud.html)
echo "[M82 PWA :8080] HTTP Status: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
  if command -v termux-open-url >/dev/null 2>&1; then
    termux-open-url "http://127.0.0.1:8080/m82_quant_hud.html"
  else
    am start -a android.intent.action.VIEW -d "http://127.0.0.1:8080/m82_quant_hud.html" >/dev/null 2>&1
  fi
else
  echo "[ERR] Revisa $M82_DIR/logs/pwa_8080.log"
  cat "$M82_DIR/logs/pwa_8080.log"
fi
