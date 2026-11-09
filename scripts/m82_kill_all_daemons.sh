#!/bin/bash
echo "🔍 [1/3] Auditando procesos Python en ejecución..."
ps aux | grep python3 | grep -v grep

echo -e "\n🛑 [2/3] Aniquilando todos los daemons y procesos Python en background..."
pkill -9 -f "python3" || true
pkill -9 -f "m82" || true
pkill -9 -f "sudeban" || true
pkill -9 -f "refinitiv" || true

echo -e "\n🧹 [3/3] Limpiando logs temporales acumulados..."
rm -f ~/M82/*.log
rm -f ~/M82/dashboard/*.log

echo "✅ Todos los daemons y bucles fueron exterminados."
