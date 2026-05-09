#!/bin/bash

# M82 HOLDINGS - AUTO-BACKUP PROTOCOL
echo "------------------------------------------"
echo "INICIANDO RESPALDO SOBERANO EN GITHUB..."
echo "------------------------------------------"

# 1. Navegar a la carpeta del Core
cd ~/M82_HOLDINGS_LLC/M82-Sovereign-Core

# 2. Agregar todos los cambios (scripts, reportes csv, pdfs)
git add .

# 3. Commit con marca de tiempo
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "M82 Update: Energy Pivot & Intel Harvest [$TIMESTAMP]"

# 4. Push a la rama principal
git push origin main

echo "------------------------------------------"
echo "RESPALDO COMPLETADO EXITOSAMENTE."
echo "OPERACIÓN SEGURA."
echo "------------------------------------------"
