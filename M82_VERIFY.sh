#!/bin/bash
echo "=== AUDITORÍA DE SALUD Y TELEMETRÍA M82 ==="
curl -s http://127.0.0.1:8000/data.json | grep -E "source|wire|timestamp|BUNKER"
echo ""
ps aux | grep -E "http.server|m82_bus" | grep -v grep
