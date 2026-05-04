#!/bin/bash

# 1. Ejecutar el núcleo M82
echo "🚀 Iniciando Núcleo M82..."
python m82_governance_final.py

# 2. Verificar si el script de Python terminó bien
if [ $? -eq 0 ]; then
    echo "✅ Verificación exitosa. Sincronizando con la Nube de Molina Holdings..."
    
    # 3. Proceso de Git Automatizado
    git add .
    git commit -m "M82 Auto-Update: Sovereign Metrics Integration - $(date +'%Y-%m-%d %H:%M')"
    git push origin main
    
    echo "🌐 Sincronización Completa. Búnker Actualizado."
else
    echo "❌ Error en el núcleo. Sincronización abortada para proteger la integridad de los datos."
fi
