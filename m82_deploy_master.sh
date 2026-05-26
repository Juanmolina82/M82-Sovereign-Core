#!/usr/bin/env bash
# M82 TERMINAL - AUTOMATED REPLICATION & DISTRIBUTED DEPLOYER

GREEN='\033[0;32m'
AMBER='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${AMBER}=== [M82] INICIANDO RESPALDO MULTI-REMOTO DE SEGURIDAD ===${NC}"

# 1. Ejecutar el motor local para actualizar estados de la caja
python3 m82_robust_platform.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Abortado: El motor de Python detectó inconsistencias de datos.${NC}"
    exit 1
fi

# 2. Indexación total en Git
echo -e "${AMBER}Preparando empaquetado de componentes...${NC}"
git add m82_config.json m82_robust_platform.py m82_box_vault.json m82_deploy_master.sh
git commit -m "Build(m82-core): Integración fija de cortafuegos, commodities y telemetría de kernels" 2>/dev/null

# 3. Empuje forzado a la rama de producción nativa (master)
echo -e "${AMBER}Replicando infraestructura en GitHub (origin master)...${NC}"
git push origin master -f

if [ $? -eq 0 ]; then
    echo -e "${GREEN}=== ✔ RESPALDO EXITOSO: ENTORNO FUSIONADO E INTEGRADO ===${NC}"
else
    echo -e "${RED}❌ Error de red al sincronizar con GitHub. Los cambios quedan protegidos localmente.${NC}"
fi
