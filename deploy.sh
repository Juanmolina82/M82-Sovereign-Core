#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def ejecutar_comando(comando, mensaje_exito, mensaje_error):
    try:
        subprocess.check_call(comando, shell=True)
        print(f"✅ {mensaje_exito}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {mensaje_error}")
        return False

def main():
    print("=== MONITOR DE DESPLIEGUE AUTOMÁTICO M82 ===")
    
    # 1. Configuración de Git Local
    print("[M82] Configurando credenciales locales...")
    os.system('git config --global user.email "jmiguel1535@gmail.com"')
    os.system('git config --global user.name "JMiguel M82"')
    
    # 2. Compilación del Núcleo C++
    print("[M82] Compilando núcleo estructural C++...")
    os.system('rm -rf m82_core')
    compilacion = ejecutar_comando(
        "clang++ -O3 m82_market_core.cpp -o m82_core",
        "Núcleo C++ compilado exitosamente.",
        "Error fatal en la compilación de clang++."
    )
    if not compilacion: return

    # 3. Asignación de Permisos de Sistema
    ejecutar_comando("chmod +x m82_core", "Permisos de ejecución otorgados a m82_core.", "Fallo al asignar permisos.")

    # 4. Sincronización con GitHub
    print("[M82] Detectando cambios para Git...")
    if not os.path.exists('.git'):
        ejecutar_comando("git init", "Repositorio Git inicializado localmente.", "Error al inicializar Git.")
    
    ejecutar_comando("git add m82_market_core.cpp m82_fusion_engine.py deploy.sh", "Archivos indexados para el despliegue.", "Error al indexar archivos.")
    
    # Commit con marca de tiempo automática
    commit_cmd = 'git commit -m "Automated Sync: Hybrid Engine Infrastructure Update"'
    subprocess.call(commit_cmd, shell=True)
    
    print("\n[🎯 SISTEMA LISTO] El motor C++ y Python están optimizados en tu Termux local.")
    print("👉 Si deseas subirlo a tu nube, solo ejecuta: git push origin main\n")

if __name__ == "__main__":
    main()
