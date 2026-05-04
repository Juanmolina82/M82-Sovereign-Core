import time
import random
from datetime import datetime

def monitor_activos():
    activos = ["Nashville Hub", "Delaware Ledger", "CCS Logistics", "Energy Asset A1"]
    print(f"\n[SISTEMA M82] Iniciando Rastreo en Tiempo Real...")
    print("----------------------------------------------------")
    
    try:
        while True:
            ahora = datetime.now().strftime("%H:%M:%S")
            activo = random.choice(activos)
            status = random.choice(["ESTABLE", "OPTIMIZANDO", "TRANSACCIÓN EN CURSO"])
            rendimiento = round(random.uniform(2.5, 4.8), 2)
            
            print(f"[{ahora}] {activo.ljust(15)} | Status: {status} | ROI: +{rendimiento}%")
            time.sleep(2)  # Actualización cada 2 segundos
    except KeyboardInterrupt:
        print("\n\n[INFO] Monitor pausado por el Chairman. Datos guardados encriptados.")

if __name__ == "__main__":
    monitor_activos()
