import time
import random
from datetime import datetime
import os

def logger_institucional(mensaje):
    with open("m82_audit_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")

def m82_gerente_robust():
    MOODYS_THRESHOLD = 2.0
    print(f"\n[M82 EXECUTIVE SHIELD] - SISTEMA DE AUDITORÍA ACTIVO")
    print("---------------------------------------------------------")
    
    activos = {"Nashville Hub": 1.2, "Delaware Ledger": 0.8, "CCS Logistics": 2.1}
    
    try:
        ciclos = 0
        while True:
            ciclos += 1
            print(f"\n>> CICLO DE AUDITORÍA #{ciclos}")
            for nombre, riesgo_base in activos.items():
                riesgo = round(riesgo_base + random.uniform(-0.3, 0.5), 2)
                
                if riesgo > MOODYS_THRESHOLD:
                    msg = f"ALERTA CRÍTICA: {nombre} con riesgo {riesgo}% (Umbral: {MOODYS_THRESHOLD}%)"
                    color = '\033[91m'
                    logger_institucional(msg) # Guardar en log para GitHub
                    print(f"{color}[!] {msg}\033[0m")
                else:
                    print(f"[*] {nombre}: {riesgo}% - Operación Normal")
            
            time.sleep(4)
    except KeyboardInterrupt:
        print("\n\n[INFO] Auditoría pausada. Reporte guardado en 'm82_audit_log.txt'")

if __name__ == "__main__":
    m82_gerente_robust()
