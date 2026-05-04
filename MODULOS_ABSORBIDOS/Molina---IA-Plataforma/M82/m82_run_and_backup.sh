#!/bin/bash
echo "--- INICIANDO PROTOCOLO M82: MODO AUTOMÁTICO ---"

# 1. Ejecutar la lógica del Hedge Fund
python m82_v2_2_final.py

# 2. Respaldar TODO en GitHub de inmediato
git add .
git commit -m "M82 Update: Macro Structure Integration - April 2026"
git push origin main

# 3. Despliegue de infraestructura y núcleo
./deploy.sh
./m82_core.sh

echo "--- OPERACIÓN COMPLETADA Y RESPALDADA EN GITHUB ---"
