#!/data/data/com.termux/files/usr/bin/bash
# M82 Sovereign AI (:8285) & M82 Wire Unified Gateway (:8286) Watchdog

if ! pgrep -f "[m]82_sovereign_web.py" > /dev/null; then
  nohup python3 ~/M82/m82_sovereign_web.py >> ~/M82/sovereign_web.log 2>&1 &
fi

if ! pgrep -f "[r]un_gateway_8283.py" > /dev/null; then
  nohup python3 ~/M82/orchestrator/run_gateway_8283.py >> ~/M82/gateway_8283.log 2>&1 &
fi

if ! pgrep -f "[c]loudflared.*m82-sovereign-apex" > /dev/null; then

if ! pgrep -f "[c]loudflared tunnel --url http://127.0.0.1:8286" > /dev/null; then
  rm -f ~/M82/quick_tunnel_8286.log
  nohup cloudflared tunnel --url http://127.0.0.1:8286 > ~/M82/quick_tunnel_8286.log 2>&1 &
  for i in $(seq 1 15); do
    U=$(grep -hoE "https://[a-zA-Z0-9-]+\.trycloudflare\.com" ~/M82/quick_tunnel_8286.log 2>/dev/null | head -n 1)
    [ -n "$U" ] && echo "$U" > ~/M82/ACTIVE_TUNNEL_URL.txt && break
    sleep 1
  done
fi
pgrep -f "[m]82_auto_wire_daemon.py" >/dev/null || nohup python3 ~/M82/orchestrator/m82_auto_wire_daemon.py >> ~/M82/auto_wire.log 2>&1 &
