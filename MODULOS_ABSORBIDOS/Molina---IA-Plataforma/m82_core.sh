#!/bin/bash

# 1. Ejecutar el núcleo de análisis
echo "🚀 Ejecutando M82 Core Engine..."
python m82_v2_2_final.py

# 2. Verificar si el script de Python terminó sin errores
if [ $? -eq 0 ]; then
    echo "✅ Análisis completado. Sincronizando Arquitectura M82..."
    
    # 3. Automatización de Git
    git add .
    # El mensaje incluye la fecha y hora exacta del sistema
    git commit -m "M82 Auto-Update: Sovereign Metrics Integration - $(date '+%d/%m/%Y %H:%M')"
    git push origin main
    
    echo "🌐 Búnker Actualizado y Sincronizado en GitHub."
else
    echo "❌ Error detectado en el script de Python. Sincronización abortada para proteger el repositorio."
fi
