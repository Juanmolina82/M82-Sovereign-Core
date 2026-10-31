#!/usr/bin/env bash

termux-wake-lock

echo "🚀 [M82] Reiniciando entorno..."
pkill -f "m82_" || true

echo "🚀 [M82] Arrancando Orquestador Maestro..."
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/M82/m82_orchestrator.log 2>&1 &

echo "✨ Infraestructura M82 completamente activa."
