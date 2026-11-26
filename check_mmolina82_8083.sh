#!/usr/bin/env bash
set -u

echo "=== [1] DNS: mmolina82.com vs molina82.com ==="
python3 - << 'PY_DNS'
import socket
for host in ["mmolina82.com", "molina82.com"]:
    try:
        ips = sorted({x[4][0] for x in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)})
        print(f"OK_DNS   {host} -> {', '.join(ips)}")
    except Exception as exc:
        print(f"FAIL_DNS {host} -> {exc}")
PY_DNS

echo ""
echo "=== [2] HTTPS PUBLICO: https://mmolina82.com ==="
for route in "/manifest.json" "/.well-known/assetlinks.json"; do
  echo "--- ROUTE $route ---"
  curl -sS -i --max-time 12 "https://mmolina82.com${route}" 2>&1 | sed -n '1,18p' || true
done

echo ""
echo "=== [3] LOCAL 127.0.0.1:8083 ==="
pgrep -af "m82_api_server.py" || echo "[WARN] m82_api_server.py no aparece en pgrep"
for route in "/manifest.json" "/sw.js" "/.well-known/assetlinks.json"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://127.0.0.1:8083${route}" || echo "000")
  echo "LOCAL_8083 $route -> HTTP $code"
done
