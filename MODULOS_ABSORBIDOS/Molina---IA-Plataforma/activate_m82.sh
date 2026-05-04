#!/bin/bash
echo "Iniciando Infraestructura Molina Holdings..."
python Intel_Core/m82_core.py &
python m82_sentinel.py
