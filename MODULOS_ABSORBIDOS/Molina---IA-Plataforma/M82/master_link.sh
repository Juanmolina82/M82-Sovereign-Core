#!/bin/bash
clear
echo -e "\033[1;93m█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█"
echo -e "█  \033[1;97mMOLINA HOLDINGS - SISTEMA DE ROBUSTEZ\033[1;93m  █"
echo -e "█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█\033[0m"

# Enlace de Inteligencia
echo -e "\n\033[1;96m[1] INTEGRANDO CAPA IA (AGI)...\033[0m"
if [ -d "~/MOLINA---IA-Plataform/molina-agi" ]; then
    echo "    -> Arquitectura Verificada en Plataforma IA."
fi

# Enlace de Motores
echo -e "\033[1;92m[2] INTEGRANDO MOTORES DE DATOS (M82)...\033[0m"
echo "    -> Magnitud Vectorial v14.3 Activa."

# Lanzamiento
echo -e "\033[1;97m[3] INICIANDO FLUJO ESTRATÉGICO...\033[0m"
sleep 2
cd ~/M82 && python ia_engine.py
