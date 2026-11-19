#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
export PYTHONUNBUFFERED=1
while true; do
    if ! python3 -c "import socket; s=socket.create_connection(('127.0.0.1',8282),1.5); s.close()" 2>/dev/null; then
        pkill -9 -f "m82_mobile_gateway.py" 2>/dev/null || true
        sleep 1
        nohup python3 -u "/data/data/com.termux/files/home/M82/orchestrator/m82_mobile_gateway.py" >> "/data/data/com.termux/files/home/M82/logs/server_8282.log" 2>&1 &
        sleep 3
    fi
    sleep 5
done
