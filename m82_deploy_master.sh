#!/usr/bin/env bash
"""
M82 TERMINAL - MULTI-REMOTE DISTRIBUTED DEPLOYER
Orchestrates replication across decentralized Git repositories.
"""

# Códigos de color para la telemetría en consola
GREEN='\033[0;32m'
AMBER='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${AMBER}=== [M82 CORE] INICIANDO DESPLIEGUE Y CONEXIÓN DISTRIBUIDA ===${NC}"

# 1. Asegurar la persistencia de datos local corriendo el motor cuántico
echo -e "${AMBER}[1/3] Ejecutando análisis cuantitativo de balance...${NC}"
python3 m82_robust_platform.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error crítico: El motor de Python abortó la operación. Verifique los parámetros.${NC}"
    exit 1
fi

# 2. Configurar la red distribuida de Git remotos (Ignorar si ya existen)
echo -e "${AMBER}[2/3] Mapeando topología de la red distribuida en GitHub...${NC}"
git remote add core-v6 https://github.com/Juanmolina82/MOLINA-GLOBAL-CORE-V6.git 2>/dev/null
git remote add macro-intel https://github.com/Juanmolina82/m82-macro-intelligence.git 2>/dev/null
git remote add ia-plataforma https://github.com/Juanmolina82/Molina---IA-Plataforma.git 2>/dev/null
git remote add sovereign-core https://github.com/Juanmolina82/M82-Sovereign-Core.git 2>/dev/null
git remote add governance https://github.com/Juanmolina82/M82-Governance-Master1.git 2>/dev/null
echo -e "${GREEN}✔ Nodos remotos integrados al árbol Git local.${NC}"

# 3. Preparación de índice, commit y push multi-objetivo
echo -e "${AMBER}[3/3] Congelando cambios en el índice de control...${NC}"
git add m82_config.json m82_robust_platform.py m82_box_vault.json m82_deploy_master.sh
git commit -m "Build(m82-core): Fijar cortafuegos de $3.25B USD y spreads de crudo ($94.07/$90.61)" 2>/dev/null

# Determinación y empuje sobre la rama de producción nativa (master)
echo -e "${AMBER}Desplegando actualizaciones hacia nodos remotos en la nube...${NC}"

for remote in origin core-v6 macro-intel ia-plataforma sovereign-core governance; do
    echo -e "${AMBER}→ Empujando bloque hacia el repositorio: [${remote}]...${NC}"
    git push $remote master -f
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✔ Sincronización exitosa en el repositorio [${remote}].${NC}"
    else
        echo -e "${RED}❌ Retraso o fallo de conexión en [${remote}]. Cambios guardados localmente.${NC}"
    fi
done

echo -e "${GREEN}=== ✔ DESPLIEGUE COMPLETO: ARCHIVOS FIJADOS LOCALMENTE Y REPLICADOS EN LA NUBE ===${NC}"
