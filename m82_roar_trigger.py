#!/usr/bin/env python3
import time
from m82_sovereign_core_monolith import M82SovereignCoreMonolith

print("[⚡] CONFIGURANDO MOTOR M82 EN MODO RUGIDO (ALTA FRECUENCIA)...")
monolito = M82SovereignCoreMonolith()

try:
    ciclo = 1
    while True:
        print(f"\n[🔥][CICLO EN EJECUCIÓN #{ciclo}] Extrayendo datos de mercado en tiempo real...")
        monolito.procesar_ciclo_total()
        print(f"[✅][CICLO #{ciclo} COMPLETADO] Esperando 15 segundos para el siguiente rugido...")
        time.sleep(15)
        ciclo += 1
except KeyboardInterrupt:
    print("\n[*] Motor de alta frecuencia detenido por el General Partner.")
